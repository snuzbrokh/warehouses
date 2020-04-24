import numpy as np 
import pandas as pd 
import re
from ast import literal_eval as make_tuple
from collections import defaultdict

def rate_clean(rate):

# '''
# Takes a price string and removes dollar signs, price ranges, and units
# Uses the range average for the case of prices.
# Also substitutes rates denominated in SQ/Yr with an adjusted rate in
# SQ/Mo. 
# '''
	lst = re.split('[- /]+',rate)
	l = len(lst)

	if lst[-1] in ['Mo','MO','Month']:
		if l == 4:
			return (float(lst[0][1:]) + float(lst[1][1:]))/2
		elif l == 3:
			return float(lst[0][1:])

	if lst[-1] in ['Yr','YR','Year']:
		if l == 4:
			return (float(lst[0][1:]) + float(lst[1][1:]))/24
		elif l == 3:
			return float(lst[0][1:])/12
	return

def amenities_clean(amen):
	if type(amen) == float:
		return 'None'
	else:
		return amen.split(',')

def size_clean(size):
	try:
		return int(size.replace(',','').replace(' SF',''))
	except:
		pass

def spaceAvail_clean(space):
	space = space.replace(' SF','').replace(',','').split(' - ')
	if len(space) == 2:
		return int(space[1])
	else:
		return int(space[0])

def space_clean(space):
	if type(space) == float:
		return
	else:
		return int(space.split()[0])

def sub_clean(sub):
	if type(sub) == float:
		return 'None'
	else:
		return [x.strip() for x in re.split('/|,',sub)]

def transport_clean(transport):
	'''
	Take in str representing tuples of nearby transport options.
	Transform into dictionary, indexed by transport option with list of
	values corresponding to distance and time to that option as well as 
	the calculated speed of travel. 
	transport[option] = [distance (mi), time (min), speed (mph)]
	'''

	# Check if value equal to np.NaN, return empty dictionary if so
	tran_dic = defaultdict()
	if type(transport) == float:
		return tran_dic

	# Initialize default dictionary
	tran_dic = defaultdict()

	# Use make_tuple function to transform imported string to list of tuples
	for tup in make_tuple(transport):
		
		try:
			trans,time,dist = tup

			# ignore most urban public transportation options
			if re.findall('walk',time):
				continue
			else:
				dist = float(dist.replace(' mi',''))
				time = float(time.replace(' min drive',''))
				# Calculate speed. Time in listing is always presented in minutes. 
				speed = round(dist/time*60,1)
				# Filter out wrong information. Top truck speed limit is 75MPH on some rural highways
				if speed <= 75.0:
					tran_dic[trans] = [dist,time, speed]
				else:
					continue
			
		except:
			continue
	return tran_dic


def util_clean(l):
	try:
		l = set(l.replace(' - ',' ').replace(',',' ').split(r' '))
		stopwords = ['City','Water','Natural','Electric','Field','County','Metal']
		l = [e for e in l if e not in stopwords]
		return l
	except:
		return []

def parse_years(x):
	try:
		num = re.findall(r'\d{4}',x)
		if len(num) == 2:
			return (int(num[0]),int(num[1]))
		elif len(num) == 1:
			return (int(num[0]),int(num[0]))
		else:
			return (1900,1900)
	except:
		return (1900,1900)


def find_height(text):
	# Patterns that ceiling heights have been found in
    height_patterns = [r'([1-3][0-9])\' [Ee]ave', \
            r'([1-3][0-9])\' [Hh]eight',\
            r'([1-3][0-9]) foot',\
            r'([1-3][0-9])\' [Cc]lear', \
            r'([1-3][0-9])\'\s?-([1-3][0-9])\''\
            r'([1-3][0-9])\''
           ]
    # Check every pattern in the text, break when found. 
    for pattern in height_patterns:
        g = re.findall(pattern,text)
        if g:
        	# For cases when listing has a range of heights, pick the highest
            if type(g[0]) == tuple:
                return int(g[0][1])
            else:
                return int(g[0])
        # If no ceiling found, use default ceiling height of 10 foot. 
        return 10
            
def find_driveIn(text):
    drive_patterns = [r'(\d+) [Dd]rive [Ii]n']
    for pattern in drive_patterns:
        g = re.findall(pattern,text)
        if g:
            return int(g[0])
    return 1

            
def find_loading(text):
    drive_patterns = [r'(\d+) [Ll]oading']
    for pattern in drive_patterns:
        g = re.findall(pattern,text)
        if g:
            return int(g[0])
    return 1


def clean(df):
	df.drop_duplicates(inplace=True, keep=False)


	#amenities
	df['amenities'] = df['amenities'].map(lambda amen: amenities_clean(amen))
	#buildingSize
	df['buildingSize'] = df['buildingSize'].map(lambda size: size_clean(size))


	df['price'] = df['price'].map(lambda rate: rate_clean(rate))
	#extraInfo
	# drop for now
	#listingDate:
	df['listingDate'] = pd.to_datetime(df['listingDate'])

	#spaceAvailable
	df['spaceAvailable'] = df['spaceAvailable'].map(lambda space: spaceAvail_clean(space))

	#spaces:
	df['spaces'] = df['spaces'].map(lambda space: space_clean(space))


	#subType:
	#df['subType'] = df['subType'].map(lambda sub: sub_clean(sub))
	#transport:
	df['transport'] = df['transport'].map(lambda transport: transport_clean(transport))
	#utilities:
	df['utilities'] = df['utilities'].map(lambda util: util_clean(util))

	df['yearBuilt'] = df['extraInfo'].apply(lambda x: parse_years(x)[0])
	df['yearRenovated'] = df['extraInfo'].apply(lambda x: parse_years(x)[1])

	# Section for data derived from scraped data
	# Create a temporary total summary column
	df_ = df[['highlights','hoodMarket','spaceSummary','spaceBullets','propOverview']]
	df_ = df_.fillna('')
	df_['total'] = df_['highlights'] + '\n' + df_['spaceSummary'] + '\n' \
						+ df_['spaceBullets'] + '\n' + df_['propOverview'] + \
						'\n' + df_['hoodMarket']

	df['ceilingHeight'] = df_.total.apply(lambda text: find_height(text))

	df['numDriveIns'] = df_.total.apply(lambda text: find_driveIn(text))
	df['numLoadingDocks'] = df_.total.apply(lambda text: find_loading(text))
	df['propInfo'] = df_['total'].replace('\n','')
	df['address'] = df['address'] + ' ' + df['city'] + ', ' + df['state'] + ' USA'


	to_drop = ['listingID', 'status','extraInfo', 'highlights','hoodMarket','spaceSummary','spaceBullets','propOverview']
	df.drop(columns = to_drop, inplace = True)

	# df.columns = ['Address','Amenities','BuildingSize','City','ListingDate',\
	# 			'Rate','PropertyType','AvailableSpace','NumSpaces','State','SubType', \
	# 			'Transport','Utilities','YearBuilt','YearRenovated']



	# df = df[['Address','City','State','Rate','BuildingSize','AvailableSpace','NumSpaces',\
	# 		'ListingDate','YearBuilt', 'YearRenovated','PropertyType','SubType','Transport', \
	# 		'Utilities','Amenities']]



	return df.reset_index(drop=True)