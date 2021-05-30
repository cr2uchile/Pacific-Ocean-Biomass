#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 23:41:01 2020

@author: menares
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import netCDF4  as netCDF4
from matplotlib.offsetbox import AnchoredText
from O3_main import obs_all , mod_all


names_stm = { 'Lauder', 'Easter_Island', 'Papeete', 'Suva', 'Hilo',
             'Watukosek'}


def plot_vs(nombre,lvl,fecha_inical,fecha_final,lim,ext=None):
    """ Esta funcion genera plot entre mod y obs, calculando algunos estadisticos
    las variables de entrada son:
    nombre=  Un string por ej:
        'Rapa_Nui', 'Suva', 'Samoa', 'Papeete', 'Watukosek',
       'San_Cristobal
    fechaa_inicial: Fecha string desde por ej:
        '1989-01-31' 
    fecha_final   : Fecha string desde por ej: '2017-12-31
    lim = Una lista con el valor inicial y final ej:
        [40,120]
    ext = al tipo de imagen a guardar por ej:
        'png' 'tiff' 'jpg' 'pdf'...
    asi por ej  plot_vs('RAP','1994-01-31','2014-12-31',[40,150].png) plotena Rapanui   '"""
    
    model_O3    = o3_mod_lvl(lvl)                                             # Carga los datos y los nombres del Modelo en un Datafame 
    obs_O3      = o3_obs_lvl(lvl)                                               # Carga los datos y los nombres de las Obs en un Dataframe 
    

    aux = ['Rapa_Nui', 'Suva', 'Samoa', 'Papeete', 'Watukosek',
       'San_Cristobal']

    nm_aux = ['Rapa Nui (27.16S, 109.4W)','Suva (19S,  178.5E)',
               'Samoa (14.25S, 170.6W)', 'Papeete (17S, 148.5W)',
               'Watukosek (7S, 112E)', 'San Cristobal']

    aux = ['0.1', 'X', 'X', 'X', 'X', '1.3'
       'San_Cristobal']

    indice = aux.index(nombre)                                                 # Este es pora llamar los plots con el nombre lat lon completo


    ax= plt.subplot(1,1,1)
    
    ####### Define Variables    
    var_model =  model_O3[nombre].loc[fecha_inical : fecha_final]              # Esto busca las fechas para plotiar
    var_obs = obs_O3[nombre].loc[fecha_inical : fecha_final]                   # Esto busca las fechas para plotiar 
    
    
    ####### Parametros para estilo del Plot
    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    
    plt.plot(var_model,'-',color='black',linewidth=1,markersize=5)             # Plot del modelo
    plt.plot(var_obs,'ob',color='red',linewidth=2,markersize=3)                # Plot de la obs
    plt.xlabel('Months', fontsize=14) ; plt.ylabel('O$_3$ [ppbv]', fontsize=14 )  # label x "meses"
    plt.title(nm_aux[indice] + ' station, Ozone in '+str(km[indice_2]) +'km', fontsize=15)                                       # Titulo busca el nombre con las ids CHR,RAP,SOMO.. 
    plt.legend(['Mod','Obs'],loc='upper center',ncol=3,frameon=False
               , fontsize=12 )                                                 # Legend
    plt.ylim(lim)                                                              # lim es definido en la funcion pone los extremos del eje y
    

    
    ####### Define de Estadisticos según Borrego et al 2008 (https://doi.org/10.1016/j.envint.2007.12.005)

    df = pd.DataFrame()                               
    df['obs'] = var_obs
    df['mod'] = var_model                                                      #Se define en un solo Dataframe para facilitar calculo 
    
    # Corellacion Pearson
    Corr = df.corr(method ='pearson') ; Corr = Corr.values[0,1]
    
    # Error Cuadratico Medio
    Rms = ((df['obs'] - df['mod']) ** 2).mean() ** .5
    
    #Indice de coincidencia
    Index = 1-np.sum(((df['obs']-df['mod'])**2)) / np.sum((abs(df['obs'] -np.mean(df['mod']))+ abs(df['mod']-np.mean(df['mod'])))**2 )
    
    #Added by LGK: Fractional Bias (Sesgo fraccional)
    aa=df['obs'].mean()
    bb=df['mod'].mean()
    FB=((aa-bb)/((aa+bb)*0.5))
    # Cuadro de texto modo String para enmcaren en el plot
    anchored_text = AnchoredText( " R="+str(round(Corr,2))+ 
                                 "\n RMS=" + 
                                 str(round(Rms,1)) + 
                                 "\n FB=" + 
                                 str(round(FB,2))
                                 + "\n Index=" 
                                 + str(round(Index,2)),
                                 prop=dict(size=12), loc=1)                    
    ax.add_artist(anchored_text)
    
#    plt.savefig(nombre+'_modelVsObs.'+ ext,dpi=600)                              # Guardar figura eslilo nombre def por RAP SMO etc.. puedes cambiar 
    
        
    return(plt.show())      




######################## Function scatter plot ##############################
def FScatter(stnname,lvl,fecha1,fecha2,obs,mod):
    '''
    
    Parameters
    ----------
    stnname : Name of station: stnname
     fecha1: inititial date of data
     fecha2: final date of data
     
        DESCRIPTION.
        Makes scatter plof obs monthly averaged model and observations for CO in the Remote Pacific
        by LGK with a whole lot of help from Camilo Menares

    Returns
    -------
    Figure for each station and saves it in a directory
    None.

    '''
    from pylab import rcParams
    rcParams['figure.figsize'] = 7, 7
    
    mod_O3    = mod                                             # Carga los datos y los nombres del Modelo en un Datafame 
    obs_O3    = obs                                               # Carga los datos y los nombres de las Obs en un Dataframe 


    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    vmod=mod_O3[stnname].loc[fecha1 : fecha2]
    vobs=obs_O3[stnname].loc[fecha1 : fecha2]
    mino=min(min(vmod),min(vobs))
    maxo=max(max(vmod),max(vobs))
    plt.scatter(vobs,vmod,  c="black", alpha=0.5, marker='o')
    plt.axes().set_aspect('equal', 'box')
    lino=[mino,maxo]
    plt.plot(lino,lino,'-k')
    plt.plot(vmod,vmod,'-k')
    plt.xlabel('Observation (ppbv)',fontsize=18) 
    plt.ylabel('Model (ppbv)', fontsize=18)
    plt.xlim([mino,maxo])
    plt.ylim([mino,maxo])
    plt.title(stnname+' station, Ozone lvl='+ str(lvl), fontsize=18) 
    plt.tight_layout()#    if ext ==None:
#        ext='png'
#    plt.savefig('FIG-SCATTER-CO//'+stnname +'.'+ext, dpi=600)    
    return(plt.show())            


################### Histograms of model and observations #########################


def FHISTOG(stnname,lvl,fecha1,fecha2,obs,mod,ext=None):
    '''
    
    
    Parameters
    ----------
    stnname : String with station name, e.g.,  RAP
        DESCRIPTION.
    fecha1 : Start date 'yyyy-mm-dd'
        DESCRIPTION.
    fecha2 : Final date 'yyyy-mm-dd'
        DESCRIPTION.

    Returns
    Two subplots for hostograms of model and observation data
    -------
    None.

    '''
#    from matplotlib.pyplot import figure    
    from pylab import rcParams
    rcParams['figure.figsize'] = 10, 5
    mod_O3 = mod                                            # Carga los datos y los nombres del Modelo en un Datafame 
    obs_O3 = obs                                              # Carga los datos y los nombres de las Obs en un Dataframe 

#    indice = aux.index(stnname)     
    vmod=mod_O3[stnname].loc[fecha1 : fecha2]
    vobs=obs_O3[stnname].loc[fecha1 : fecha2]

    mino=min(min(vmod),min(vobs)) ; mino = mino*0.8
    maxo=max(max(vmod),max(vobs)) ; maxo=maxo*1.2
    nbins=30
#    figure(figsize(8,5))
    ax1=plt.subplot(1,2,1)    
    plt.hist(vmod, bins=nbins,color ='black',alpha=1.0) 
    plt.title("Model Histogram ",fontsize=18) 
    plt.xlabel('Model (ppbv)',fontsize=18) 
    plt.ylabel('Frequency', fontsize=18)
    plt.xlim(mino,maxo)
    plt.ylim(0,20)
    
    ax2=plt.subplot(1,2,2)    
    plt.hist(vobs, bins=nbins,color ='black',alpha=1.0)  
    plt.title("Observations Histogram",fontsize=18) 
    plt.xlabel('Observations (ppbv)',fontsize=18) 
    plt.ylabel('Frequency', fontsize=18)
    plt.xlim(mino,maxo)
    plt.ylim(0,20)
    plt.suptitle(stnname + "station, Ozone lvl=" +str(lvl), fontsize=24)
    
    # if ext ==None:
    #     ext='png'
                                           
    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    plt.show()   
#    plt.savefig('FIG-HIST-CO//'+stnname +'.'+ext, dpi=600)    
    return()


n_lvl = 0
obs = obs_all(n_lvl)
mod = mod_all(n_lvl)

plt.figure()
FHISTOG('Lauder',n_lvl,'1994','2014',obs,mod)
plt.figure()
plot_vs('Lauder',n_lvl,'1994','2014',obs,mod,[0,60])
plt.figure()
FScatter('Watukosek',1,'1994','2014',obs,mod)








   