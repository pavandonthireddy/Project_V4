# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:15:16 2020

@author: Pavan
"""

import numpy as np

def get_valid_index(strategy_weights,delay=1):
    valid_index = ~np.isnan(strategy_weights).all(axis=1)
    valid_index[-1*delay]=False
    return valid_index


def bets_to_pnl(starting_value,strategy_weights,clean_values,base_data,long_lev, short_lev, ADV_threshold_percentage,costs_threshold_bps,commissions_bps):

    cleaned_weights       = strategy_weights[clean_values]

    O  = (base_data[0])[clean_values]
    C = (base_data[3])[clean_values]
    Liq   = (base_data[5])[clean_values]
    H  = (base_data[1])[clean_values]
    L   = (base_data[2])[clean_values]
       
    dollars_at_open  = np.empty(cleaned_weights.shape)
    dollars_at_open_calc  = np.empty(cleaned_weights.shape)
    dollars_at_close = np.empty(cleaned_weights.shape)
    purchased_shares = np.empty(cleaned_weights.shape)
    costs            = np.empty(cleaned_weights.shape)
    commissions        = np.empty(cleaned_weights.shape)
    value_at_open    = np.empty(cleaned_weights.shape[0])
    value_at_open[0] = starting_value
    value_at_close   = np.empty(cleaned_weights.shape[0])
    pnl              = np.empty(cleaned_weights.shape)
    daily_pnl        = np.empty(cleaned_weights.shape[0])
    long_pnl        = np.empty(cleaned_weights.shape[0])
    short_pnl        = np.empty(cleaned_weights.shape[0])
    
    def tc_Q_vss_bps(pct_adv, minutes=1.0, minutes_in_day=60*6.5):
        day_frac = minutes / minutes_in_day
        tc_pct = 0.1 * abs(pct_adv/day_frac)**2
        return tc_pct*10000
    
    for i in range(dollars_at_open.shape[0]):
        dollars_at_open[i,:] = value_at_open[i]*cleaned_weights[i,:]       
        purchased_shares[i,:]= dollars_at_open[i,:]/O[i,:]
        threshold = np.minimum(abs(dollars_at_open[i,:]/O[i,:]), Liq[i,:]*ADV_threshold_percentage/100)
        purchased_shares[i,:]=np.sign(purchased_shares[i,:])*threshold        
        dollars_at_open_calc[i,:]=O[i,:]*purchased_shares[i,:]      
        dollars_at_close[i,:]= C[i,:]*purchased_shares[i,:]
        
#        costs_bps[i,:]       = tc_Q_vss_bps(purchased_shares[i,:]/Liq[i,:],5,60*6.5)
        costs[i,:]           = (np.abs(purchased_shares[i,:])*(H[i,:]-L[i,:])*costs_threshold_bps)/10000               
        commissions[i,:]     = (np.abs(purchased_shares[i,:])*commissions_bps/10000)*(H[i,:]+H[i,:])       
        pnl[i,:]             = (dollars_at_close[i,:]-dollars_at_open_calc[i,:]-costs[i,:]-commissions[i,:])
        daily_pnl[i]         = np.nansum(pnl[i,:])
        long_pnl[i]         = np.nansum(pnl[i,:][cleaned_weights[i,:]>0])
        short_pnl[i]        = np.nansum(pnl[i,:][cleaned_weights[i,:]<0])
        value_at_close[i]    = np.nansum(np.abs(dollars_at_open[i,:])/(long_lev+short_lev))+np.nansum(pnl[i])
        if i != dollars_at_open.shape[0]-1:
            value_at_open[i+1]=value_at_close[i]
    
    strategy_daily_returns = daily_pnl/value_at_open
    long_contribution = long_pnl/value_at_open
    short_contribution = short_pnl/value_at_open
    
    strategy_log_returns = np.log(1+strategy_daily_returns)

    return strategy_log_returns, strategy_daily_returns, long_contribution, short_contribution, costs, purchased_shares,dollars_at_open, dollars_at_close, value_at_open, value_at_close, pnl, daily_pnl
  