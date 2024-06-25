# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from urllib.parse import quote

def get_glider():
    glider = pd.read_csv('line80-satellitequery.csv')
    glider = glider.drop(index = 0)
    #select only surface depths (10m)
    glider = glider[glider.get('depth') == '10.0']
    glider['time'] = glider['time'].apply(str)
    glider['depth'] = pd.to_numeric(glider['depth'], errors='coerce')
    glider['chlorophyll'] = pd.to_numeric(glider['chlorophyll'], errors='coerce')
    glider['latitude'] = pd.to_numeric(glider['latitude'], errors='coerce')
    glider['longitude'] = pd.to_numeric(glider['longitude'], errors='coerce')
    glider['profile'] = pd.to_numeric(glider['profile'], errors='coerce')
    #get rid of chl NaN values
    glider = glider[(glider.get('chlorophyll') >= 0) | (glider.get('chlorophyll') < 0)]
    return glider