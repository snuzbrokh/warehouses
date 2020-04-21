import numpy as np 
import pandas as pd 
import re
from ast import literal_eval as make_tuple
from collections import defaultdict



#buildingSize:
#city:
#extraInfo:

#price:
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
	return int(size.replace(',','').replace(' SF',''))

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

def transport_clean(transport):
	'''
	Take in str representing tuples of nearby transport options.
	Transform into dictionary, indexed by transport option with list of
	values corresponding to distance and time to that option as well as 
	the calculated speed of travel. 
	transport[option] = [distance (mi), time (min), speed (mph)]
	'''

	# Check if value equal to np.NaN, return empty dictionary if so
	if type(transport) == float:
		return {}

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

			tran_dic[trans] = [dist,time, round(dist/time*60,1)]
			
		except:
			continue
	return tran_dic if tran_dic else {}


def util_clean(util):
	if type(util) == float:
		return 'None'
	else:
		return util.split(',')


def clean(df):
	df.drop_duplicates(inplace=True)
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
	#transport:
	df['transport'] = df['transport'].map(lambda transport: transport_clean(transport))
	#utilities:
	df['utilities'] = df['utilities'].map(lambda util: util_clean(util))


	to_drop = ['listingID','propType','status','extraInfo']
	df.drop(columns = to_drop, inplace = True)

	return df.dropna()