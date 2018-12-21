import pandas as pd
from collections import defaultdict
from scipy.spatial.distance import cdist
import numpy as np
import time
import pickle

## WORKING ON 10k subset in 15 seconds on 10/31/18

### paths
csv_path = 'us_only_stations.csv'
pickled_fire_data_path = 'fire_subset.pkl'

### CREATE STATE-TO-LIST-OF-STATIONS DICTIONARY

start=time.time()
# read in csv of available weather stations
all_stations = pd.read_csv(csv_path, header=None,
                           names=['USAF', 'WBAN', 'STATION NAME', 'CTRY', 'ST',
                                  'CALL', 'LAT', 'LON', 'ELEV(M)', 'BEGIN',  'END'])

# keep only those that have relevant dates and valid coordinates
stations_has_data_beyond_1992 = all_stations[all_stations['END'] // 10000 > 1992]
drop_nulls = stations_has_data_beyond_1992.dropna(axis=0,
                                                  subset=['LAT', 'LON', 'BEGIN', 'END'])
# print(len(stations_has_data_beyond_1992) - len(drop_nulls), 'stations with nulls') {64} stations

# create state-to-list-of-stations dictionary
station_locs = defaultdict()
for group in drop_nulls.groupby('ST'):
    station_locs[group[0]] = group[1][[
        'LAT', 'LON', 'USAF', 'BEGIN', 'END']].values
# with open('state_to_stations_dict.pkl', 'wb') as picklefile:
#     pickle.dump(station_locs, picklefile)
end = time.time()
print('Time to create state->station dictionary', end - start)


# get distances to each station from fire location and return a sorted list of stations

def get_sorted_stations(row, station_locs):
    location = row[['LATITUDE', 'LONGITUDE']].values.reshape(1, 2)
    # print(row['STATE'])
    state_stations = station_locs[row['STATE']]
    dists = cdist(location, state_stations[:, :2])
    return state_stations[np.argsort(dists)]


def find_closest_station(row, station_locs):
    sorted_stations = get_sorted_stations(row, station_locs).reshape(-1,5)    
    fire_date = row['date_as_int']
    # print(fire_date)
    # i=0
    # for station in np.nditer(sorted_stations, flags=['external_loop', 'refs_ok']):
    for station in sorted_stations: # np array already is an iterator?
        # idx {'start date':3, 'end date':4}
        # i += 1
        # print(i)
        # print(station[3], station[4])
        if fire_date > station[3] and fire_date < station[4]:
            return station[2]  # 2 = USAF idx
        else:
            continue
    print("No matching station found for fire", row['FOD_ID'])
    return None


# load in sample data
# for subset in pickled_fire_data_paths:
sample = pd.read_pickle(pickled_fire_data_path)
# sample = fire_subset.sample(n=100, random_state=1)

# prep data
sample['DISCOVERY_DATE'] = pd.to_datetime(
sample['DISCOVERY_DATE'], origin='julian', unit='D')

sample['date_as_int'] = (10000 * sample['DISCOVERY_DATE'].dt.year + 100 *
                         sample['DISCOVERY_DATE'].dt.month + sample['DISCOVERY_DATE'].dt.day)

# apply
start = time.time()
sample['weather_station'] = sample.apply(
    find_closest_station, args=(station_locs,), axis=1)
end = time.time()
print('Apply time:', end - start)
print(sample.head())
