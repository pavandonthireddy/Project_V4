# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 08:23:24 2019

@author: Pavan
"""

import numpy as np
import pandas as pd 
from hypothesisEngine.fitness.expression import *
import math as mth
import os

from hypothesis_engine import hypothesis_params
import hypothesisEngine.fitness.load_data as data
import hypothesisEngine.fitness.utilities as ut



variable_list    = ut.excel_list('Variable_list.xlsx')   
clean_index,diff_dates,tickers_universe = data.get_clean_index(hypothesis_params['START DATE'] ,hypothesis_params['END DATE'] )    
portfolios = data.get_portfolio(hypothesis_params['PORTFOLIO'], tickers_universe)    
datasets_dict = data.load_datasets(variable_list,clean_index,portfolios,tickers_universe)    

base_data = data.data_for_bets(datasets_dict) 


for key, val in datasets_dict.items():
    vars()[key] = val