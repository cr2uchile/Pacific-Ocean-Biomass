#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:49:00 2020

@author: menares
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import netCDF4  as netCDF4
from matplotlib.offsetbox import AnchoredText

fh = Dataset('o3_monthly_ts.nc', mode='r')
names = fh.variables['names'][:]
# lat = fh.variables['lat'][:]
# lon = fh.variables['lon'][:]
# time = fh.variables['time'][:]
conc = fh.variables['conc'][:]

fechas_obs = pd.date_range('1980-01-01', '2017-11-30', freq='M') 

def o3_aux(lvl,names,conc):
    
    conc_stn = conc[:,lvl,np.arange(20),np.arange(20)]
    df_o3 = pd.DataFrame(conc_stn, index= fechas_obs, columns = names)
    return df_o3

df_o3 = o3_aux(0,names,conc)


# df_o3.plot(figsize=(12,15.5),color='black',subplots=True,layout=(5, 4),ylim=[0,55]) ; plt.tight_layout()


fh_d = Dataset('sondes_data_tm4.nc', mode='r')
(fh_d.variables.keys())

o3 = fh_d.variables['O3'][:][:][:]
time = fh_d.variables['time'][:]


fh_n = Dataset('meta.nc', mode='r')
(fh_n.variables.keys())

stn = fh_n.variables['name'][:]




def pd_o3_obs(stn,lvl):
    
    o3_lv = o3[stn,:,lvl]
    
    a = o3_lv.data.astype(float)
    a[np.where(o3_lv.mask!=0)] = np.nan
    a[a>350] = np.nan
    
    t = time.data.astype(float)
    t[np.where(time.mask!=0)] = np.nan

    fechas = pd.date_range('1994-01-01-00','2014-12-23-23',freq='H')
    pd_a = pd.Series(a,index= fechas)
  
    
    return pd_a 

def obs_all(lvl):
    
    Lauder_obs        = pd_o3_obs(0,lvl).resample('M').mean()
    Easter_Island_obs = pd_o3_obs(4,lvl).resample('M').mean()
    Papeete_obs       = pd_o3_obs(5,lvl).resample('M').mean()
    Suva_obs          = pd_o3_obs(6,lvl).resample('M').mean()
    Hilo_obs          = pd_o3_obs(9,lvl).resample('M').mean()
    Watukosek_obs     = pd_o3_obs(8,lvl).resample('M').mean()
    
    frame_obs = { 'Lauder': Lauder_obs.values , 'Easter_Island': Easter_Island_obs
                 , 'Papeete': Papeete_obs , 'Suva': Suva_obs, 'Hilo': Hilo_obs,
                 'Watukosek': Watukosek_obs}
    
    obs = pd.DataFrame(frame_obs)
    return(obs)



def mod_all(lvl):
       
    df_o3 = o3_aux(lvl,names,conc)
    Lauder_mod        = df_o3['Lauder'].resample('M').mean().loc['1994':'2014']
    Easter_Island_mod = df_o3['Christmas_Island'].resample('M').mean().loc['1994':'2014']
    Papeete_mod       = df_o3['Papeete'].resample('M').mean().loc['1994':'2014']
    Suva_mod          = df_o3['Suva'].resample('M').mean().loc['1994':'2014']
    Hilo_mod          = df_o3['Hilo'].resample('M').mean().loc['1994':'2014']
    Watukosek_mod     = df_o3['Watukosek'].resample('M').mean().loc['1994':'2014']
    
    frame_mod = { 'Lauder': Lauder_mod.values , 'Easter_Island': Easter_Island_mod
                 , 'Papeete': Papeete_mod , 'Suva': Suva_mod, 'Hilo': Hilo_mod,
                 'Watukosek': Watukosek_mod}

    mod = pd.DataFrame(frame_mod)
    return mod


names_stm = { 'Lauder', 'Easter_Island', 'Papeete', 'Suva', 'Hilo',
             'Watukosek'}


fig, ax = plt.subplots(1,1)
Lauder_mod.plot(ax = ax)
Lauder_obs.plot(ax = ax)

# from datetime import date, timedelta, datetime

# days = int(time.data[time.data>0][-1]) # remplazar 0 para conocer el primero en len(time.data)
# start = datetime(1950, 1, 1, 0) 
# delta = timedelta(hours= days)  
# offset = start + delta     
# print(offset)               
# print(type(offset))      






###########3