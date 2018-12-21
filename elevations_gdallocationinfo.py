#!/usr/bin/env python3

import os
import pandas as pd 
import time

fires = pd.read_pickle('./historic_by_month_done.pkl')
alaska = fires[fires['STATE'] == 'AK']
print(len(alaska))

# print(alaska[['LONGITUDE', 'LATITUDE']])

def get_elevation(row):
    '''return elevation from coordinates
    Requires gdallocation tool https://www.gdal.org/gdallocationinfo.html'''
    lon = row['LONGITUDE']
    lat = row['LATITUDE']
    try: 
        if row.name % 100 == 0:
            print(row.name, row['FOD_ID'])
        return os.popen(f'gdallocationinfo -valonly -wgs84 ./alaska/elevaki0100a.tif {lon} {lat}').read().strip()
    except:
        print('error', lon, lat, row['STATE'], row['FOD_ID'])
        return ''

start = time.time()
alaska['Elevation'] = alaska.apply(get_elevation, axis=1)
end = time.time()
print('Apply execution time=', end - start)
start = time.time()
alaska.to_pickle('alaska_with_elevation.pkl')
end = time.time()
print('Pickling execution time=', end - start)

# NEXT STEPS
# 1. make dict with state: list of stations coordinates

# 2. look up df['STATE'] and calc min(cdist(XA, XB, 'euclidean')) # scipy.spatial.distance.cdist

# SEE make_dict_stations_by_state.py
