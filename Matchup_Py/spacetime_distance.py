# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from geopy.distance import geodesic

def spacetime_distance(lat, lon, time, matched):
    """
    Distance function that returns the matched chla of the 'closest' matched
    satellite point.

    Parameters
    ----------
    lat : float
        glider latitude of surface chla measurement
    lon : float
        glider longitude
    time : string
        glider time
    matched : pandas DataFrame
        four columns - sat_time, matched_lat, matched_lon, matched_chla
    Returns
    -------
    closest : np.array
        matched time,lat,lon,chla

    """ 
    # TIME FILTER
    # Sometimes more than one time is returned.
    # If more than one time is returned, filter to only use the closest
    # Chlorophyll is daily and highly variable per day
    # It would be reasonable to test impact of filtering time first or location first.
    
    #time if more than one returned
    time_dt = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")             
    # filter to closest timestamp
    def to_datetime(string):
        return datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
    
    matched = matched.assign(sat_time = matched.get('sat_time').apply(to_datetime))
    time_diffs = [abs(time_dt - time) for time in matched['sat_time']]
    which_time_diffs = [i for i,v in enumerate(time_diffs) if 
                        v == min(time_diffs)]
    min_time_diff = min(time_diffs)
    closest = matched.loc[which_time_diffs]
    closest = closest.assign(time_diff = pd.Series([min_time_diff] * closest.shape[0]))

    # DISTANCE FILTER
    # Calculate spatial distances
    glider_loc = (lat, lon)
    dists = np.zeros(closest.shape[0])
    for j in range(0, closest.shape[0]):
        satellite_loc = (closest['matched_lat'].iloc[j], 
                         closest['matched_lon'].iloc[j])
        dist = geodesic(glider_loc, satellite_loc).km
        dists[j] = dist
        
    closest['spatial_dist'] = dists

    # Filter to closest cell
    closest = closest.loc[closest['spatial_dist'] == min(dists)]

    if closest.shape[0] > 1:
        print('ERROR: Multiple rows, only one allowed. Number of rows: ' +
              str(len(closest)))
        print(closest)
        closest = closest.head(1)
    # new df should be a single row now.
    # Note: This may not be the best matchup choice, need to make plots/analyze
    
    return closest