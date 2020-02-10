# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 18:26:11 2020

@author: Pavan
"""

import hypothesisTest.utilities as ut
import hypothesisTest.load_data as data
from hypothesisTest.expression import *
import hypothesisTest.weights as weights
import numpy as np
import pandas as pd
import hypothesisTest.weights_to_bets as wb
import hypothesisTest.performance as pf
import warnings
warnings.filterwarnings("ignore")
    
def backtester(params):   
  
    variable_list    = ut.excel_list('Variable_list.xlsx')   
    clean_index,diff_dates,tickers_universe = data.get_clean_index(params['START DATE'] ,params['END DATE'] )    
    portfolios = data.get_portfolio(params['PORTFOLIO'], tickers_universe)    
    datasets_dict = data.load_datasets(variable_list,clean_index,portfolios,tickers_universe)    

    base_data = data.data_for_bets(datasets_dict) 

    for key, val in datasets_dict.items():
        vars()[key] = val
    strategy = eval(params['STRATEGY EXPRESSION'] )
    strategy_weights = weights.weights(datasets_dict['Sectors'],strategy,params['NEUTRALIZATION'] ,params['LONG LEVERAGE'] ,params['SHORT LEVERAGE'] )
    clean_values_from_weights = wb.get_valid_index(strategy_weights)
    cleaned_index_weights = (clean_index.values)[clean_values_from_weights]
    cleaned_strategy_weights       = strategy_weights[clean_values_from_weights]  
    

    strategy_log_returns,strategy_daily_returns, long_contribution, short_contribution, costs, \
    purchased_shares, dollars_at_open, dollars_at_close, value_at_open, \
    value_at_close, pnl, daily_pnl = wb.bets_to_pnl(params['STARTING VALUE'] ,strategy_weights,clean_values_from_weights,base_data,params['LONG LEVERAGE'] , params['SHORT LEVERAGE'] , params['ADV THRESHOLD PERCENTAGE'],params['COST THRESHOLD BPS'],params['COMMISSION BPS']) 

    underlying_daily_returns = np.nanmean(np.log(base_data[3][clean_values_from_weights]/base_data[0][clean_values_from_weights]),axis=1)  
    return pf.metrics(datasets_dict,clean_values_from_weights,cleaned_index_weights, \
                   daily_pnl,pnl,strategy_log_returns,dollars_at_open, \
                   purchased_shares,underlying_daily_returns,cleaned_strategy_weights, \
                   params['STARTING VALUE'] ,long_contribution,short_contribution, \
                   strategy_daily_returns)