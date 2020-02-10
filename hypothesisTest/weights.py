# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:10:07 2020

@author: Pavan
"""

import numpy as np

def weights(Sectors,strategy,neutral='DOLLAR',long_leverage=0.5,short_leverage=0.5):
    if neutral == 'DOLLAR':
        exp_ls = strategy-np.nanmean(strategy,axis=1)[:,np.newaxis]
    elif neutral =='SECTOR':
        exp_ls = strategy.copy()
        unique_sectors = list(range(1,12))
        for i in range(strategy.shape[0]):
            for sector in unique_sectors:
                idx = np.where(Sectors[i,:]==sector,True,False)
                if sum(idx)>=2:
                    exp_ls[i,:][idx] = strategy[i,:][idx]-np.nanmean(strategy[i,:][idx])
                else:
                    exp_ls[i,:][idx] = 0
    else:
        exp_ls = strategy

    exp_norm = (exp_ls/np.nansum(abs(exp_ls),axis=1)[:,np.newaxis])
    exp_norm = np.where(exp_norm>=0,2*long_leverage*exp_norm,2*short_leverage*exp_norm)
    return exp_norm