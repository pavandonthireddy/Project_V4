# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 15:54:07 2020

@author: Pavan
"""

import pandas  as pd
import hypothesisEngine.fitness.utilities as ut
import numpy as np

def get_clean_index(start_date,end_date):
    sample_address = ".\\Data\\"+"sample.feather"
    sample = pd.read_feather(sample_address)
    sample.set_index('index',inplace=True)
    sample.index = pd.to_datetime(sample.index)
    sample = sample[sample.index.isin(pd.date_range(start=start_date,end=end_date))]
    sample = sample.dropna(axis=0,how='all')
    
    diff_dates = pd.DataFrame(index=sample.index)
    diff_dates['index']= diff_dates.index.astype('datetime64[ns]') 
    diff_dates['Diff'] = (diff_dates['index'] - diff_dates['index'].shift())
    tickers_universe = list(sample.columns)
    return sample.index, diff_dates['Diff'].values, tickers_universe



def get_portfolio(portfolio,tickers_universe):
    df = pd.read_excel(".\\Data\\"+'sector_list_updated.xlsx', sheet_name=0)
    ticker = list(df['Ticker'])
    sector = list(df['Sector'])
    cap      = list(df['Cap'])
    
    unique_sector = list(set(sector))
    unique_cap = list(set(cap))
    
    portfolio_dict = {}
    portfolio_dict['US_TOP_500_LIQUID']=tickers_universe
    portfolio_dict['Dummy']=tickers_universe[50:55]
    
    sector_dict = dict()
    for sec in unique_sector:
        sector_list = list()
        for i in range(len(ticker)):
            if sector[i]==sec:
                sector_list.append(ticker[i])
        sector_dict[sec]=sector_list
    
    portfolio_dict.update(sector_dict)

    cap_dict = dict()
    for capit in unique_cap:
        cap_list = list()
        for i in range(len(ticker)):
            if cap[i]==capit:
                cap_list.append(ticker[i])
        cap_dict[capit]=cap_list
        
    portfolio_dict.update(cap_dict)
    return portfolio_dict[portfolio]
    

def load_datasets(variable_list,clean_index,portfolio,tickers_universe):
    datasets_dict = {}
    for var in variable_list:
        var_address=".\\Data\\"+var+".feather"
        var_df=pd.read_feather(var_address)
        var_df.set_index('index',inplace=True)       
        if var not in ['benchmark','rf_rate','Fama_French']:
            var_df.columns = tickers_universe #white spaces issues; hence this
            var_df = var_df[portfolio]
        var_df.index = pd.to_datetime(var_df.index)
        var_df = var_df[var_df.index.isin(clean_index)]
        var_df.fillna(method='ffill',axis=0,inplace=True)
        var_array=var_df.values
        if var in ['benchmark','rf_rate','Fama_French'] and var !='Fama_French':
            var_array = var_array[:,6]
        datasets_dict[var]=var_array
    return datasets_dict


def data_for_bets(datasets_dict,delay=1):  
    O = ut.shift(datasets_dict['Open'],-1*delay,np.nan)
    H= ut.shift(datasets_dict['High'],-1*delay,np.nan)
    L= ut.shift(datasets_dict['Low'],-1*delay,np.nan)
    C = ut.shift(datasets_dict['Close'],-1*delay,np.nan) 
    V= ut.shift(datasets_dict['Volume'],-1*delay,np.nan)
    Liq= datasets_dict['ADV']
    data = [O,H,L,C,V,Liq]
    return data