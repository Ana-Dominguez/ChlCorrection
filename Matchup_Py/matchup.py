# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from urllib.parse import quote

def matchup(lat, lon, time, dlat, dlon, dtime, start_url):
    """
    Finds all matchups to glider surface chl measurements within 
    given spatial and temporal constraints. Must complete the errdap url
    begun before 'matchup' is called.

    Parameters
    ----------
    lat : float
        latitude of glider value
    lon : float
        longitude
    time : string
        time of surfacing (10m)
        format: "%Y-%m-%dT%H:%M:%SZ"
    dlat : float
        search radius in latitude
    dlon : float
        search radius in longitude
    dtime : float
        search radius time-wise

    Returns
    -------
    time : np.array
        array of times from matched chl
    lat : np.array
        array of matched lat values
    lon : np.array
        array of matched lon values
    chl : np.array
        array of matched non-NaN chl values

    """

    # Time bounds
    dtime = timedelta(days = dtime) 
    time_dt = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    timemin_dt = time_dt - dtime
    timemax_dt = time_dt + dtime
    # String format for request
    timemin = timemin_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    timemax = timemax_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Spatial bounds
    latmin = str(lat - dlat)
    latmax = str(lat + dlat)
    lonmin = str(lon - dlon)
    lonmax = str(lon + dlon)
    
    # Complete query url
    query_url = ''.join(['[(' + timemin + '):1:(' + timemax + ')]',
                         '[(' + latmin + '):1:(' + latmax + ')]', 
                         '[(' + lonmin + '):1:(' + lonmax + ')]'])
    encoded_query = quote(query_url, safe='')
    # join the start and query parts of the url
    url = start_url + encoded_query
    # query ERDDAP
    print(datetime.now())
    matched = pd.read_csv(url, skiprows=1)
    print(datetime.now())
    matched.columns = ["sat_time", "matched_lat", 
                       "matched_lon", "matched_chla"]
    
    # filter for successful results
    matched = matched[matched.get('matched_chla') >= 0]
    matched = matched.reset_index().drop(columns = 'index')
    
    return matched
