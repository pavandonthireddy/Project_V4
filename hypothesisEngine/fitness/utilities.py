# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 15:44:58 2020

@author: Pavan
"""

import pandas as pd
import numpy as np


        
def excel_list(file_name,sheet=0):
    List = pd.read_excel(".\\Data\\"+file_name,sheet_name=sheet)
    List = List['Variable'].tolist()
    return List

def shift(array, n,fill):
    shifted_array = np.empty_like(array)
    if n >= 0:
        shifted_array[:n,:] = fill
        shifted_array[n:,:] = array[:-n,:]
    else:
        shifted_array[n:,:] = fill
        shifted_array[:n,:] = array[-n:,:]
    return shifted_array



def shift_array(array,n,fill):
    shifted_array = np.empty_like(array)
    if n >= 0:
        shifted_array[:n] = fill
        shifted_array[n:] = array[:-n]
    else:
        shifted_array[n:] = fill
        shifted_array[:n] = array[-n:]
    return shifted_array
    

def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x * 1e-6)

def to_datetime(date):
    from datetime import datetime
    """
    Converts a numpy datetime64 object to a python datetime object 
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)


def millions_fmt(x):
    'The two args are the value and tick position'
    return '$%1.1f M' % (x * 1e-6)

def print_results(results):
    for key,value in results.items():
        if key not in ["CLASSIFICATION_DATA","FACTOR_RES","SHARPE_BS","SHARPE_BS_GEOM_AVG","PLOT_CURVES_DATA"]:
            print("{:<40}{:^5}{:<20}".format(key," :\t", value))
            
    print("Classification Metrics : \n")
    print(results['CLASSIFICATION_DATA'],"\n")
    print("Factor Analysis : \n")
    print(results['FACTOR_RES'])