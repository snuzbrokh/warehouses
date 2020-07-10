import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=3958.8):
    if to_radians:
        lat1, lon1, lat2, lon2 = map(np.radians,[lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))


def n_nearest(df,n=25):
    '''
    Pass in a distance dataframe where each entry is the calculated
    great circle distance between a column index and a row index
    
    Returns a dataframe of:
    1. Name of origin. 
    2. Mean distance to the n closest locations
    3. Distances used in calculating the mean.
    4. List of the neightbors by name.
    
    '''
    #df.index = df.columns
    nodes = df.columns
    
    neighbors = pd.DataFrame()
    lst = []
    for node in nodes:
        list_ = df[node].sort_values()[1:].head(n)
        
        dists = list_.values
        neigh = list_.index.values
        avg = dists.mean()
        lst.append([node, avg, dists, neigh])
    return pd.DataFrame(lst, columns = ['name','mean_dist','distToNeighbors',\
                                        'neighbors'])

def num_nearest(df, d=20.0):
    '''
    Pass in a distance dataframe where each entry is the calculated
    great circle distance between a column index and a row index
    '''
    #df.index = df.columns
    nodes = df.columns
    lst = []
    for node in nodes:
        mask = df[node].values <= d
        num_nearest = max(mask.sum()-1,0) #remove self
        #neigh = df[node][mask].index.values
        lst.append([node, num_nearest])
    return pd.DataFrame(lst, columns=['name','num_nearest'])

def distance_matrix(places):
    
    places = pd.concat(places, ignore_index=True)
    lats = places['lat']
    lons = places['lon']
    names = places['name']
    
    L = len(names)
    
    mat = pd.DataFrame()
    for i in range(L):
        node = names[i]
        t = []
        for j in range(L):
            t.append(haversine(lats[i],lons[i],lats[j],lons[j]))
        mat[node] = t
    #mat.index = mat.columns
    return mat

def nearest_hubs(cities, hubs, d):
    city_to_hubs = distance_matrix([cities,hubs])
    a = city_to_ports.iloc[cities.shape[0]:,0:cities.shape[0]]

    return nearest(a,d)