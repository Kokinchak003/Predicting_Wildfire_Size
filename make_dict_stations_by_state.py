import pandas as pd 

all_stations = pd.read_csv('us_only_stations.csv', header=None, 
                names=['USAF', 'WBAN', 'STATION NAME', 'CTRY', 'ST', 
                'CALL', 'LAT', 'LON', 'ELEV(M)', 'BEGIN',  'END'])

stations_has_data_beyond_1992 = all_stations[all_stations['END'] // 10000 < 1992]
drop_nulls = stations_has_data_beyond_2012.dropna(axis=0, 
                    subset=['LAT', 'LON', 'BEGIN', 'END']) #57 nulls


# df.to_dict('list')

#state_to_stations dictionary lookup
#pseudo code
# station_locs = state_stations[df['STATE']] => df['LAT', 'LON'].values
from collections import defaultdict
station_locs = defaultdict()
for group in df.groupby('ST'):
    station_locs[group[0]] = group[1][['LAT', 'LON', 'USAF', 'BEGIN', 'END']].values
    #tuple version - not good for calculating distances
# for state, coor in zip(df['ST'], df['lat,lon']):
#     ...:     if state not in sd:
#     ...:         sd[state] = [coor]
#     ...:     else:
#     ...:         sd[state] += [coor]


# get date as int for comparison - vectorize
# pseudo: df['date_as_int'] = df['year']*10000 + df['month']*100 + day
gfires['date_as_int'] = 10000 * gfires['DISCOVERY_DATE'].dt.year + 100
     ...:  * gfires['DISCOVERY_DATE'].dt.month + gfires['DISCOVERY_DATE'].dt.day


from scipy.spatial.distance  import cdist

# get distances to each station from fire location
location = row[['LAT', 'LON']].values # should be a 1x2 np array
dists = cdist(location, station_locs[row['STATE']][:2]) 

cdist(gfires[['LATITUDE', 'LONGITUDE']].values[0].reshape(1,2), sd[gfi
     ...: res['STATE'].values[0]].iloc[:,:2])

def get_sorted_stations(row, station_locs):
    location = row[['LATITUDE', 'LONGITUDE']].values.reshape(1,2)
    state_stations = station_locs[row['STATE']]
    dists = cdist(location, state_stations.iloc[:,:2])
    return state_stations[np.argsort(dists)]                
# rearrange df by distance ascending
stations_sorted = station_locs[np.argsort(dists)] 



def find_closest_station(row, station_locs):
    sorted_stations = get_sorted_stations(row, station_locs)
    fire_date = row['date_as_int']
    for station in sorted_stations.itertuples():
        # idx {'start date':3, 'end date':4}
        if fire_date > station[3] and fire_date < station[4]:
            return station[2] # 2 = USAF idx
        else:
            continue
    print("No matching station found for fire", row['FOD_ID'])
    return None



### GOT CLOSEST STATION

### START BIG QUERY 



# Extra snippets
# {a:b for a,b, in zip(df[a], df[b])}
# d = {coor:usaf for coor, usaf in zip(df['lat,lon'], df['USAF'])}
#make dic coordinates to xcz

# list(map(divide, df['A'], df['B']))
