import pandas as pd
from collections import defaultdict
from scipy.spatial.distance import cdist
import numpy as np
import time

# read in csv of available weather stations
all_stations = pd.read_csv('us_only_stations.csv', header=None,
                           names=['USAF', 'WBAN', 'STATION NAME', 'CTRY', 'ST',
                                  'CALL', 'LAT', 'LON', 'ELEV(M)', 'BEGIN',  'END'])

# keep only those that as relevant dates and valid coordinates
stations_has_data_beyond_1992 = all_stations[all_stations['END'] // 10000 < 1992]
drop_nulls = stations_has_data_beyond_1992.dropna(axis=0,
                                                  subset=['LAT', 'LON', 'BEGIN', 'END'])  # 57 nulls

# create state-to-list-of-stations dictionary
station_locs = defaultdict()
for group in drop_nulls.groupby('ST'):
    station_locs[group[0]] = group[1][[
        'LAT', 'LON', 'USAF', 'BEGIN', 'END']].values

# get distances to each station from fire location and return a sorted list of stations


def get_sorted_stations(row, station_locs):
    location = row[['LATITUDE', 'LONGITUDE']].values.reshape(1, 2)
    state_stations = station_locs[row['STATE']]
    dists = cdist(location, state_stations[:, :2])
    return state_stations[np.argsort(dists)]


def find_closest_station(row, station_locs):
    sorted_stations = get_sorted_stations(row, station_locs)
    fire_date = row['date_as_int']
    for station in sorted_stations.itertuples():
        # idx {'start date':3, 'end date':4}
        if fire_date > station[3] and fire_date < station[4]:
            return station[2]  # 2 = USAF idx
        else:
            continue
    print("No matching station found for fire", row['FOD_ID'])
    return None


# load in sample data
gfires = pd.read_pickle('Gfires.pkl')
sample = gfires.sample(n=20, random_state=1)

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
