# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import quote
from matchup import matchup
import time
from spacetime_distance import spacetime_distance
from get_glider import get_glider

# create variables for the unchanging parts of the ERDDAP data-request URL. 
base_url = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/'
dataset_id = "pmlEsaCCI60OceanColorDaily"
file_type = '.csv'
query_start = '?'
erddap_variable = 'chlor_a'
start_url = ''.join([base_url, dataset_id, file_type, 
                     query_start, erddap_variable])

def to_datetime(string):
        return datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")

# define spatial and temporal constraints
dlat = 0.1
dlon = 0.1
dtime = 0.5

# get glider data
glider = get_glider();

# create matchups
print('total number of glider points: ' + str(glider.shape[0]))
total_start = datetime.now()
col_names = ["sat_time", "matched_lat", "matched_lon", "matched_chla",
             "spatial_dist", "time_diff", "glider_time"]
closest = pd.DataFrame(columns = col_names)
all_matchups = pd.DataFrame(columns = ["sat_time", "matched_lat", 
                                       "matched_lon", "matched_chla"])
day_or_night = pd.DataFrame(columns = ['day_or_night'])
for i in np.arange(glider.shape[0]):
   my_matchup = matchup(glider['latitude'].iloc[i], glider['longitude'].iloc[i], 
                        glider['time'].iloc[i], dlat, dlon, dtime, start_url)
   all_matchups = pd.concat([all_matchups, my_matchup])
   time.sleep(0.5)
   if (my_matchup.empty):
       my_closest = pd.DataFrame(pd.Series([None]*len(col_names), index=col_names)).T
   else:
       my_closest = spacetime_distance(glider['latitude'].iloc[i], glider['longitude'].iloc[i], 
                                       glider['time'].iloc[i], my_matchup)
   closest = closest.assign(glider_time = pd.Series([glider['time'].iloc[i]] * closest.shape[0]))
   closest = closest.assign(glider_lat = pd.Series([glider['latitude'].iloc[i]] * closest.shape[0]))
   closest = closest.assign(glider_lon = pd.Series([glider['longitude'].iloc[i]] * closest.shape[0]))
   closest = pd.concat([closest, my_closest], axis = 0)
sat_end = datetime.now()
print('time_of_day, total_time')
print(total_start)
print(sat_end - total_start)
#x_index = np.array(np.arange(closest.shape[0]))