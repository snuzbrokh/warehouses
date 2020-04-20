import numpy as np 
import pandas as pd 

def clean(df):

	df['rate'] = df['price'].map(lambda rate: rate_adjust(rate))






	
	to_drop = ['listingID','propType','status','price']
	df.drop(columns = to_drop, inplace = True)
	return(df)

#address:
#amenities:
#buildingSize:
#city:
#extraInfo:
#listingDate:
#listingID:
#price:
def rate_adjust(rate):
	'''
	Takes a price string and removes dollar signs, price ranges, and units
	Uses the range average for the case of prices.
	Also substitutes rates denominated in SQ/Yr with an adjusted rate in
	SQ/Mo. 
	'''
    lst = re.split('[- /]+',price)
    l = len(lst)

    if lst[-1] in ['Mo','MO','Month']:
        if l == 4:
            return (float(lst[0][1:]) + float(lst[1][1:]))/2
        elif l == 3:
            return float(lst[0][1:])
        else:
            return np.NaN
    if lst[-1] in ['Yr','YR','Year']:
        if l == 4:
            return (float(lst[0][1:]) + float(lst[1][1:]))/24
        elif l == 3:
            return float(lst[0][1:])/12
        else:
            return np.NaN
#propType:
#spaceAvailable:
#spaces:
#state:
#status:
#subType:
#transport:
#utilities:

