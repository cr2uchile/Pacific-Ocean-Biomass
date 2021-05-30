#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 01:04:04 2021

@author: cmenares
"""

import numpy as np
#from Data_config_Sinca import * # mutear si es cargado dataframe
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from scipy.optimize import leastsq
import pandas as pd







####################### Regressions #####################################
#####################################################################

from scipy.optimize import leastsq
from PyEMD import EMD


def Linear_trend_lastq(s):

    def model(t, coeffs):
       return  coeffs[0] + coeffs[1]*t
    
    
    def residuals(coeffs, y, t):
        return y - model(t, coeffs)
    
    
    x0 = np.array([1, 1 ], dtype=float)
    
    t = np.arange(len(s))
    x, flag = leastsq(residuals, x0, args=(s, t))
    y = model(t,x)
    trend = (y[-1] - y[0])/len(y)
    
    return y , trend
    

def emd_trend(s):

    IMF = EMD().emd(s)
    N = IMF.shape[0]+1
    
    y = IMF[N-2,:]
#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))
    
    return y , trend



def lamsal_trend(s):

    
    def model(t, coeffs):
       return  (coeffs[0] + coeffs[1]*t + coeffs[2]*np.sin(2*np.pi*t/12) + coeffs[3]*np.cos(2*np.pi*t/12) +
                coeffs[4]*np.sin(4*np.pi*t/12) + coeffs[5]*np.cos(4*np.pi*t/12) + 
                coeffs[6]*np.sin(6*np.pi*t/12) + coeffs[7]*np.cos(6*np.pi*t/12) +
                coeffs[8]*np.sin(8*np.pi*t/12) + coeffs[9]*np.cos(8*np.pi*t/12) +
                coeffs[10]*np.sin(10*np.pi*t/12) + coeffs[11]*np.cos(10*np.pi*t/12) +
                coeffs[12]*np.sin(12*np.pi*t/12) + coeffs[13]*np.cos(12*np.pi*t/12) +
                coeffs[14]*np.sin(14*np.pi*t/12) + coeffs[15]*np.cos(14*np.pi*t/12) +
                coeffs[15]*np.sin(16*np.pi*t/12) + coeffs[16]*np.cos(16*np.pi*t/12) +
                coeffs[17]*np.sin(18*np.pi*t/12) + coeffs[18]*np.cos(18*np.pi*t/12) 
    )
    
    def residuals(coeffs, y, t):
        return y - model(t, coeffs)
    
    
    
    x0 = np.array([1, 1 ,1, 1,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=float)
    
    t = np.arange(len(s))
    x, flag = leastsq(residuals, x0, args=(s, t))
    y = model(t,x)
#    y = x[0] + x[1]*t 
    trend = x[1]
    intercep  = x[0]
    
    return y , trend , intercep , residuals
 

def stl_trend(s_df):

    from statsmodels.tsa.seasonal import STL
    stl = STL(s_df, seasonal=15)
    res = stl.fit()

    y = res.trend
#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))

    return res.trend , trend


from sklearn.linear_model import LinearRegression, TheilSenRegressor

def TheillSen_trend(s) :
    t = np.arange(len(s))
    X = t[:, np.newaxis]
    
    reg = TheilSenRegressor(random_state=0).fit(X, s)
    y =  reg.predict(X)

#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))

    return y , trend



def linear_trend(s) :
    t = np.arange(len(s))
    X = t[:, np.newaxis]
    
    reg = LinearRegression().fit(X, s)
    y =  reg.predict(X)

#    trend = (y[-1] - y[0])/len(y)
    trend = np.nanmean(np.diff(y))

    return y , trend

def tiao(mod,obs) : 
    """
    Tiao et al 1990 https://doi.org/10.1029/JD095iD12p20507
    http://stackoverflow.com/q/14297012/190597
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    """
    
    def autocorr(x):
        x = pd.Series(x)
        n = len(x)
        variance = x.var()
        x = x-x.mean()
        r = np.correlate(x, x, mode = 'full')[-n:]
        result = r/(variance*(np.arange(n, 0, -1)))
        return result

    
    residuo = obs - mod
    Tiao  = (1-autocorr(mod)[1])**(-1/2)*np.std(residuo)*0.023/12      
    
    return Tiao


