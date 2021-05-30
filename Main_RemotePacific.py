#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 22:17:47 2020

@author: Camilo Menares; Modified by Laura Gallardo (LGK)
"""
import matplotlib.pyplot as plt #Imports math and graph library
# Libreria para graficos 
import pandas as pd  #Imports time seres handling library
# Libreria para Serie de datos indexa fechas, genera estadisticos rapidos .. etc
import info_RemotePacific  #Import key settings for the following graphs and data
# Libreria creada para definir las rutas, string y graficos de los Modelos
from info_RemotePacific import FHISTOG
from info_RemotePacific import FScatter
from info_RemotePacific import boxplot_ENSO
from info_RemotePacific import ENSO_mei
import numpy as np  


#################### Cargar Datos en Dataframe ##############################
# Dataframe es un formato de pandas tipo obejtos que permine manipular datos

mod_CO, name  = info_RemotePacific.leerModel()                                            # Carga los datos y los nombres del Modelo en un Datafame 
obs_CO   , name  = info_RemotePacific.leerObs()                                              # Carga los datos y los nombres de las Obs en un Dataframe 


################### Genera plot para todas las estacion desde Dataframe #############################
# De forma sencilla el plots para todos los datos es mod_CO.plot() 
# la siguientes linea de codigo da un formato mas limpio


######## Plot model config
axes = mod_CO.plot(figsize=(9,15), kind='line', subplots=True,layout=(7, 2), # Parametros para pandas PLOT
                    grid=True,sharex = True, ylim=(40,150))
plt.suptitle('Model CO',fontsize=18)                                           # Titulo para toso los plot "Suptitie"                                
plt.subplots_adjust(top=0.94,bottom=0.05,left=0.115,right=0.91,hspace=0.2,
                    wspace=0.2)                                                # Aregla los parametros del tamaño plot
for i in range(7):  axes[i,0].set_ylabel('CO [ppbv]')                          # atiqueta los 7 labels del eje Y 


######## Plot model config
axes= obs_CO.plot(figsize=(9,15), kind='line', subplots=True,layout=(7, 2)
                  ,grid=True,sharex = True, ylim=(40,150))
plt.suptitle('Observation CO',fontsize=18)  
plt.subplots_adjust(top=0.94,bottom=0.05,left=0.115,right=0.91,hspace=0.2,
                    wspace=0.2)                                                # Aregla los parametros del tamaño plot
for i in range(7):  axes[i,0].set_ylabel('CO [ppbv]')                          # atiqueta los labels del eje Y 






################### Genera plot modelos vs observaciones #############################
# De forma sencilla el plots para todos los datos es plot_vs('RAP','1994-01-31','2014-12-31',[40,150])
# el siguente ciclo es para tas las estaciones

indice_name = ['CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05',
       'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM']

for i,j in zip(indice_name,name):
    
    plt.rcParams["font.family"] = "Times New Roman"    
    print(i)
#    plt.figure()
#    FScatter(i,'1994-01-01','2014-12-31')
#    FHISTOG(i,'1994-01-01','2014-12-31')
    plt.figure(figsize=(12,9.5))
    plt.suptitle(j,fontsize=20)
    plt.subplot(211)
    ENSO_mei(i,'obs',rest_trend=True,show_trend=False)
    plt.subplot(212)
    ENSO_mei(i,'mod',rest_trend=True,show_trend=False)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('FIG-SCATTER-ENSO/Scatter_MEI_'+i+'.png',dpi=600)
    
    
    
############################# TREND

    
from __toolsTrend import *

# reading new data

mod_rap = pd.read_csv('Data 2021/rapanui.txt')
mod_rap = mod_rap.set_index(pd.to_datetime(mod_rap['Unnamed: 0']))
mod_rap = mod_rap['md']

mod_samoa = pd.read_csv('Data 2021/samoa.txt')
mod_samoa = mod_samoa.set_index(pd.to_datetime(mod_samoa['Unnamed: 0']))
mod_samoa = mod_samoa['md']

# Lamsal trend test 

print('Trend Obs in RapaNui is:')
print(lamsal_trend(obs_CO.RAP.interpolate(method='spline', order=2).loc['1994':'2014'])[1]*10*12)
print('Trend Model in RapaNui is:')
print(lamsal_trend(mod_rap.loc['1994':'2014'])[1]*10*12)

# Mann kendall test

import pymannkendall as mk

result = mk.original_test(mod_samoa.loc['1994':'2017'])
result2 = mk.original_test(obs_CO.SMO.interpolate(method='spline', order=2).loc['1994':'2017'])

print('MK test model Samoa :' + str(result))
print('MK test Obs Samoa :' + str(result2))

# Functions for plot lamsal

def plot_trend_obs(obs= obs_CO.RAP,sc= 'Observation',zone = 'Rapa Nui'):
    
    fig , ax =  plt.subplots(3,1, figsize=(18,20))
    
        
    trend_rap = lamsal_trend(obs.interpolate(method='spline', order=2).loc['1994':'2014'])
    lineal_rap = trend_rap[1]*np.arange(len(trend_rap[0])) 
    res_rap =  obs_CO.RAP.loc['1994':'2014'] - trend_rap[0]
    numeric_trend = trend_rap[1]*12*10
        
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 28
    plt.rcParams['ytick.labelsize'] = 28
    
    ax[0].plot(obs.loc['1994':'2014'],'o',color='black',label='Data')
    ax[0].plot(obs.loc['1994':'2014'].index ,trend_rap[0],
               color='red' , linewidth=3,label='Fourier')
    ax[1].plot(obs.loc['1994':'2014'].index, lineal_rap,'-',color='black',label= 'Trend =' + str(round(numeric_trend,1)) + '±'  + str(round(tiao(obs.interpolate(method='spline', order=2).loc['1994':'2014'],trend_rap[0])*12,1) ) 
               +  ' ppbv/decade')
    ax[2].plot(res_rap,'o',color='gray',label='Noise')
    
    ax[0].set_ylim(40,80) , ax[1].set_ylim(-10,2) ,  ax[2].set_ylim(-40,40)
    ax[0].set_ylabel('CO [ppbv]',fontsize=30) , ax[1].set_ylabel('CO [ppbv]',fontsize=30) ,  ax[2].set_ylabel('CO [ppbv]',fontsize=30)
    
    ax[0].legend(fontsize=28,loc=1) , ax[1].legend(fontsize=28,loc=1) , ax[2].legend(fontsize=28,loc=1)
    ax[0].set_title(zone + ' ('+sc+')',fontsize=34,fontweight='bold')


def plot_trend_mod(obs= obs_CO.RAP,sc= 'Model',zone = 'Rapa Nui'):
    
    fig , ax =  plt.subplots(3,1, figsize=(18,20))
    
        
    trend_rap = lamsal_trend(obs.loc['1994':'2014'])
    lineal_rap = trend_rap[1]*np.arange(len(trend_rap[0])) 
    res_rap =  obs['1994':'2014'] - trend_rap[0]
    numeric_trend = trend_rap[1]*12*10
        
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 28
    plt.rcParams['ytick.labelsize'] = 28
    
    ax[0].plot(obs.loc['1994':'2014'],'o',color='black',label='Data')
    ax[0].plot(obs.loc['1994':'2014'].index ,trend_rap[0],
               color='red' , linewidth=3,label='Fourier')
    ax[1].plot(obs.loc['1994':'2014'].index, lineal_rap,'-',color='black',label= 'Trend =' + str(round(numeric_trend,1)) + '±'  + str(round(tiao(obs.loc['1994':'2014'],trend_rap[0])*12,1) )  +  ' ppbv/decade')
    ax[2].plot(res_rap,'o',color='gray',label='Noise')
    
    ax[0].set_ylim(40,80) , ax[1].set_ylim(-10,2) ,  ax[2].set_ylim(-40,40)
    ax[0].set_ylabel('CO [ppbv]',fontsize=30) , ax[1].set_ylabel('CO [ppbv]',fontsize=30) ,  ax[2].set_ylabel('CO [ppbv]',fontsize=30)
    
    ax[0].legend(fontsize=28,loc=1) , ax[1].legend(fontsize=28,loc=1) , ax[2].legend(fontsize=28,loc=1)
    ax[0].set_title(zone  + '( '+sc+')',fontsize=34,fontweight='bold')

    
# Lamsal trend plot
plot_trend_obs(obs_CO.RAP,sc= 'Observation',zone = 'Rapa Nui (27.16S,109.4W)')
plt.savefig('obs_trend_rap.png',dpi=600)
plot_trend_mod(mod_rap,sc= 'Model',zone = 'Rapa Nui (27.16S,109.4W)' )
plt.savefig('obs_mod_rap.png',dpi=600)

plot_trend_obs(obs_CO.SMO,sc= 'Observation',zone = 'Samoa (14.25S,170.6W)')
plt.savefig('obs_trend_samoa.png',dpi=600)

plot_trend_mod(mod_samoa,sc= 'Model',zone = 'Samoa (14.25S,170.6W)')
plt.savefig('obs_mod_samoa.png',dpi=600)
