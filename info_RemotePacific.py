#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 22:20:08 2020
@author: menares



"""
import pandas as pd  
# Libreria para Serie de datos indexa fechas, genera estadisticos rapidos .. etc
import numpy as np  
# Libreria para matrices y operaciones matematicas modo Matlab incluye Nans .. etc
import scipy.io
# Libreria para lectura de datos formato h5 h4 mat etc
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
# Libreria para graficos 



#################### Funcion para definir la info type Laura

def informacion(k):
    """" Otorga las ruta del nombre del archivo, nombre completo y abreviatura para cada estacion.
    La entrada es un numero del 1 al 14 para entrar a las estaciones
    """    
    if k==1: #Christmas Island
            ruta = 'MCO-chr'
            sname='Christmas Island (1.70N, 157.1W)';
            fn='CHR';
    elif k==2: #Rapa Nui
            ruta = 'MCO-eic'
            sname='Rapa Nui (27.16S,109.4W)';
            fn='RAP';
    elif k==3: # Samoa
            ruta='MCO-smo'
            sname='Samoa (14.25S, 170.6W)';
            fn='SMO';
    elif k==4: #POCN15
            ruta = 'MCO-pocn15'
            sname='Pacif. Ocean (15N,145W)';
            fn='POCN15';
    elif k==5: #POCN10
            ruta = 'MCO-pocn10'
            sname='Pacif. Ocean (10N,149W)';
            fn='POCN10';
    elif k==6: #POCN05
            ruta = 'MCO-pocn05'
            sname='Pacif. Ocean (5N,151W)';
            fn='POCN05';
    elif k==7: #POC000
            ruta = 'MCO-poc000'
            sname='Pacif. Ocean (0N/S,155W)';
            fn='POC000';
    elif k==8: #POCS05
            ruta='MCO-pocs05'
            sname='Pacif. Ocean (5S,159W)';
            fn='POCS05';
    elif k==9: #POCS10
            ruta='MCO-pocs10'
            sname='Pacif. Ocean (10S,161W)';
            fn='POCS10';
    elif k==10: #POCS15
            ruta = 'MCO-pocs15'
            sname='Pacif. Ocean (15S,164W)';
            fn='POCS15';
    elif k==11: # POCS20
            ruta= 'MCO-pocs20'
            sname='Pacif. Ocean (20S,167W)';
            fn='POCS20';
    elif k==12: # POCS 25
            ruta = 'MCO-pocs25'
            sname='Pacif. Ocean (25S,171W)';
            fn='POCS25';
    elif k==13:  #POCS30
            ruta = 'MCO-pocs30'
            sname='Pacif. Ocean (30S,176W)';
            fn='POCS30';
    
    elif k==14:  #Guam
            ruta = 'MCO-gmi'
            sname='Guam (13.39N, 144.65E)'
            fn='GUAM'
     
    return(ruta,sname,fn)



#################### Funcion para leer todos los modelos


def leerModel():
    """Lee todos los modelos y devuelve un Datamframe para todos los modelos y sus nombres"""
    for i in range(1,15):                                                      # Define i del 1 al 14           

        ruta,sname,fn =  informacion(i)                                        # Llama a la ruta del nombre al nombre y abrev del modelo sub i
    
        fechas = pd.date_range('1980-01-01', '2017-11-30', freq='M')           # Define las fechas de los modelos
  #      data = pd.read_csv( 'Model\'+ruta+'.txt' ,delimiter=' ', header = 0);  # le los datos txt de la carpeta Model
        data = pd.read_csv( 'Model/'+ruta+'.txt' ,delimiter=' ', header = 0);  # le los datos txt de la carpeta Model
        data   = data.values[:,1]                                              # Elige solo los datos
 
        if i == 1 :        
            df_data = pd.DataFrame(data, index=fechas, columns= [fn])          # Genera el primer tipo de archivo Dataframe
            name = list([sname])
        else:
            df_data[(fn)]  = data                                              # Agrega las otras estaciones al Dataframe creado con la primera estacion
            name.append(sname)

    return df_data.astype('float'), name                                       # Devuele los datos Datafrme "df_data" y los fuerza a ser float .astype('float')  



#################### Funcion para leer todos las Obs

def leerObs():
    """Lee todos los modelos y devuelve un Datamframe para todos las obs y sus nombres"""

    for i in range(1,15):                                                      # Define i del 1 al 14

        ruta,sname,fn =  informacion(i)                                        # Llama a la ruta del nombre al nombre y abrev del modelo sub i
        mat = scipy.io.loadmat('Obs/'+ruta+'.mat')                             # Lee los .mat en obs
        
        fechas = pd.date_range('1989-01-01', '2018-01-30', freq='M')           # Define las fechas de las obs
        data = mat['Mobs'] ;  data = data[:,2]
        
        if i == 1 :                                                            # Agrega las otras estaciones al Dataframe creado con la primera estacion                     
            df_data = pd.DataFrame(data, index=fechas, columns= [fn])
            name = list([sname])
        else:                                                                  # Agrega las otras estaciones al Dataframe creado con la primera estacion
            df_data[(fn)]  = data
            name.append(sname)
    return df_data.astype('float'), name 


######## Plot funcion para poder generar todos los model vs obs

def plot_vs(nombre,fecha_inical,fecha_final,lim,ext):
    """ Esta funcion genera plot entre mod y obs, calculando algunos estadisticos
    las variables de entrada son:
    nombre=  Un string por ej:
        'CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05', 'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM',
    fechaa_inicial: Fecha string desde por ej:
        '1989-01-31' 
    fecha_final   : Fecha string desde por ej: '2017-12-31
    lim = Una lista con el valor inicial y final ej:
        [40,120]
    ext = al tipo de imagen a guardar por ej:
        'png' 'tiff' 'jpg' 'pdf'...
    asi por ej  plot_vs('RAP','1994-01-31','2014-12-31',[40,150].png) plotena Rapanui   '"""
    
    model_CO , name  = leerModel()                                             # Carga los datos y los nombres del Modelo en un Datafame 
    obs_CO   , name  = leerObs()                                               # Carga los datos y los nombres de las Obs en un Dataframe 

    aux = ['CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05',
       'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM']
    
    indice = aux.index(nombre)                                                 # Este es pora llamar los plots con el nombre lat lon completo

    ax= plt.subplot(1,1,1)
    
    ####### Define Variables    
    var_model =  model_CO[nombre].loc[fecha_inical : fecha_final]              # Esto busca las fechas para plotiar
    var_obs = obs_CO[nombre].loc[fecha_inical : fecha_final]                   # Esto busca las fechas para plotiar 
    
    
    ####### Parametros para estilo del Plot
    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    
    plt.plot(var_model,'-',color='black',linewidth=1,markersize=5)             # Plot del modelo
    plt.plot(var_obs,'ob',color='red',linewidth=2,markersize=3)                # Plot de la obs
    plt.xlabel('Months', fontsize=14) ; plt.ylabel('CO [ppbv]', fontsize=14 )  # label x "meses"
    plt.title(name[indice], fontsize=15)                                       # Titulo busca el nombre con las ids CHR,RAP,SOMO.. 
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
    
    plt.savefig(nombre+'_modelVsObs.'+ ext,dpi=600)                              # Guardar figura eslilo nombre def por RAP SMO etc.. puedes cambiar 
    
        
    return(plt.show())                                                         # Retonar la figura                                                                    

######################## Function scatter plot ##############################
def FScatter(stnname,fecha1,fecha2,ext=None):
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
    rcParams['figure.figsize'] = 5, 5
    
    mod_CO, name  = leerModel()                                            # Carga los datos y los nombres del Modelo en un Datafame 
    obs_CO   , name  = leerObs()                                              # Carga los datos y los nombres de las Obs en un Dataframe 

    aux = ['CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05',
       'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM']
    
    indice = aux.index(stnname)     

    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    vmod=mod_CO[stnname].loc[fecha1 : fecha2]
    vobs=obs_CO[stnname].loc[fecha1 : fecha2]
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
    plt.title(name[indice], fontsize=18) 
    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    if ext ==None:
        ext='png'
    plt.savefig('FIG-SCATTER-CO//'+stnname +'.'+ext, dpi=600)    
    return(plt.show())            


################### Histograms of model and observations #########################
def FHISTOG(stnname,fecha1,fecha2,ext=None):
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
    mod_CO, name  = leerModel()                                            # Carga los datos y los nombres del Modelo en un Datafame 
    obs_CO   , name  = leerObs()                                              # Carga los datos y los nombres de las Obs en un Dataframe 

    aux = ['CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05',
       'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM']
    indice = aux.index(stnname)     
    vmod=mod_CO[stnname].loc[fecha1 : fecha2]
    vobs=obs_CO[stnname].loc[fecha1 : fecha2]

    mino=min(min(vmod),min(vobs)) ; mino = mino*0.8
    maxo=max(max(vmod),max(vobs)) ; maxo=maxo*1.2
    nbins=30
#    figure(figsize(8,5))
    ax1=plt.subplot(1,2,1)    
    plt.hist(vmod, bins=nbins,color ='black',alpha=1.0) 
    plt.title("Model Histogram",fontsize=18) 
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
    plt.suptitle(name[indice], fontsize=24)
    
    if ext ==None:
        ext='png'
                                           
    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    plt.show()   
    plt.savefig('FIG-HIST-CO//'+stnname +'.'+ext, dpi=600)    
    return()


def boxplot_ENSO(nombre,Mod_or_Obs,Freq,ENSO_name,rest_trend=True,show_trend=False):
    """
    Parameters
    ----------
    nombre : string
        nombre estacion elejis
        ej : 'CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05',
       'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM'
    Mod_or_Obs : string
        Selecionar el calculo para modelo o para 'obs' o 'mod' 
        ej:'obs'
    Freq : string
        Resolucion para los promedios, years o month
        ej :"Y" o "M".
    ENSO_name : string
        Para el calculo de la anomalia enso index desde https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.81-10.ascii
        ej: 'ANOM1.3' 'ANOM3.4' 'ANOM4' 'ANOM3' .
    rest_trend : operador logico True o False, optional
        True calcula el resto de la tendencia para las conc de CO. The default is True.
        ej: True
    lim_enso : string, optional
        Encuentra limites en 0.5 para ENSO. usar:
            'TWO': para limites  de 0.5 y -0.5 en el niño y la niña
            'Niño': limites arriba de 0,5 solo en niño
            'Niña': limites de -0.5 solo niña.
    show_trend : Operador logico True o False
        Añade un grafico que muestra como es la tendencia. The default is False.
        

    Returns : Un scatter plot con las correlaciones anomalas de ENSO y CO mas algunos estadist.
    -------
    por Camilo M. 9/5/2020.

    """
        # Lectura de datos
    
    model_CO , name  = leerModel()                                            # Carga los datos y los nombres del Modelo en un Datafame 
    obs_CO   , name  = leerObs()                                              # Carga los datos y los nombres de las Obs en un Dataframe 

    ### Define Datafrmae para Obs y Mod    

    df        = pd.DataFrame()   
    df['obs'] = obs_CO[nombre]
    df['mod'] = model_CO[nombre]          
    
    # Define OSI o ENSO anolaia
    
    fechas = pd.date_range('1951-01-01', '2020-04-01', freq='M')           # Define las fechas de los modelos
    osi = pd.read_csv( 'data_OSI.csv',header=1)
    
    osi = pd.Series(osi.values[:,1], index = fechas)
    enso = pd.read_csv( 'Enso.txt', delim_whitespace=True ,header=0)
    
    fecha_inical = '1994-01-31'
    fecha_final = '2014-12-31'

    fechas = pd.date_range('1950-01-01', '2020-05-01', freq='M')           # Define las fechas de los Ensos
    enso = enso.set_index(fechas)
    enso = enso[ENSO_name]
    
    # Acopla fechas
    
    osi = osi.loc[fecha_inical : fecha_final]
    enso = enso.loc[fecha_inical : fecha_final]
    df  = df.loc[fecha_inical : fecha_final]

    #Calculo de tendencia
    
    time       = df.index 
    x          = np.arange(time.size)                                          # = array([0, 1, 2, ..., 3598, 3599, 3600])
    y          = df[Mod_or_Obs].fillna(df[Mod_or_Obs].mean())                                            # Saca Nans
    fit        = np.polyfit(x, y, 1)
    fit_fn     = np.poly1d(fit)
    trend_line = fit_fn(x)
    
    ##Verifica trend line 
    if show_trend == True:
        plt.figure() ; plt.plot(df.index, df[Mod_or_Obs].values, 'k-') ; plt.plot(df.index, fit_fn(x), '-',color='red') ; plt.ylabel('CO [ppmb]')
        plt.title(nombre+': Trend Line '+ ENSO_name ,fontsize=14)
    
    ## Concentracion - Trend line
    if rest_trend == True:
        anomal_obs = df[Mod_or_Obs] - trend_line 


    #Calculo climatologia
    
    mat_h = df.set_index(df.index.month, append=True)[Mod_or_Obs].unstack().mean()
    a = pd.concat([mat_h] * int(len(df.index)/12), axis=0)
    clim_obs = pd.Series( a.values ,index = df.index)

    ## Concentracion - Climatologia
    anomal_obs = df[Mod_or_Obs] - clim_obs 


    ## Define nuevo Dataframe
    df_clima = pd.DataFrame()
    df_clima['anomal_obs'] = anomal_obs

    if ENSO_name == 'SOI':
        df_clima['anomal_ens'] = osi
    else:    
        df_clima['anomal_ens'] = enso    

                                                      
    # Condicion para tomar Meses o Años
    if Freq == 'M':
        Corr = df_clima.corr(method ='pearson') ; Corr = Corr.values[0,1]
    if Freq == 'Y':
        Corr = df_clima.resample('Y').mean().corr(method ='pearson') ; Corr = Corr.values[0,1]
        df_clima = df_clima.resample('Y').mean()
        

    #Calculo de tendencia ENSO vs ANOM CO
    
    y          = df_clima['anomal_obs'].fillna(df_clima['anomal_obs'].mean())                                          # = array([0, 1, 2, ..., 3598, 3599, 3600])
    x          = df_clima['anomal_ens']                                            # Saca Nans
    fit        = np.polyfit(x, y, 1)
    fit_fn     = np.poly1d(fit)
    trend_line = fit_fn(x)

        
        
    #################### Parametros para el plot##############################

    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    
#    plt.figure(figsize=(10,5))

    if Mod_or_Obs == 'obs':
        ax2 = plt.subplot(2,1,1)
    elif Mod_or_Obs == 'mod':
        ax2 = plt.subplot(2,1,2)            

    plt.plot(np.zeros(2),[-38,38],'-k',alpha=0.8,linewidth=0.8) ; plt.ylim([-38,38])
    plt.plot([-2.5,2.5],np.zeros(2),'-k',alpha=0.8,linewidth=0.8)   ; plt.xlim([-2.2,2.2])

    plt.plot([0.5, 0.5],[-38,38],':k',alpha=0.6,linewidth=0.8) 
    plt.plot([-0.5, -0.5],[-38,38],':k',alpha=0.6,linewidth=0.8)

    plt.plot(df_clima['anomal_ens'],trend_line, '-k',linewidth=2)
     
    # Scaterr, ciclo para pintar cada color niña o niño    
    for i,j in zip(df_clima['anomal_ens'],df_clima['anomal_obs']):
        if i>0.5:
            plt.scatter(i,j,color='red',alpha=0.8)
        elif i<-0.5:
            plt.scatter(i,j,color='blue',alpha=0.8)
        else:
            plt.scatter(i,j,color='gray',alpha=0.9)
            
    # Condicion para el Titulo de Obs o Mod
    
    if Mod_or_Obs == 'obs':
        plt.ylabel('Obs Anomaly CO (ppbv)',fontsize=18)
    elif Mod_or_Obs == 'mod':
        plt.ylabel('Mod Anomaly CO (ppbv)',fontsize=18)
        
    plt.xlabel('ENSO '+ ENSO_name[4:7],fontsize=18)


    aux_nino  = df_clima[ (df_clima['anomal_ens']>0.5) ]                     # Niños extremos, descomentar
    corr_nino = aux_nino.corr(method ='pearson') ; corr_nino = corr_nino.values[0,1]
    Nnan = np.sum(np.isnan(aux_nino['anomal_obs']))
    N = len(aux_nino)-Nnan
    anchored_text = AnchoredText( "Corr=" + str(round(corr_nino,2)) +
                                 "\n N=" + str(round(N,0)) , prop=dict(size=16,color='red',fontweight="bold"),frameon=False, loc=1)
    ax2.add_artist(anchored_text)

    aux_nina  = df_clima[ (df_clima['anomal_ens']<-0.5) ]                     # Niños extremos, descomentar
    corr_nina = aux_nina.corr(method ='pearson') ; corr_nina = corr_nina.values[0,1]
    Nnan = np.sum(np.isnan(aux_nina['anomal_obs']))
    N = len(aux_nina)-Nnan
    anchored_text = AnchoredText( "Corr=" + str(round(corr_nina,2)) +
                                 "\n N=" + str(round(N,0))  , prop=dict(size=16,color='blue',fontweight="bold"),frameon=False, loc=2)
    ax2.add_artist(anchored_text)

    corr_t = df_clima.corr(method ='pearson') ; corr_t = corr_t.values[0,1]
    Nnan = np.sum(np.isnan(df_clima['anomal_obs']))
    N = len(df_clima['anomal_obs'])-Nnan
    anchored_text = AnchoredText( "CO$_{Anomaly}$ (ppbv) = %.2f$\cdot$ENSO$_{3.4}$ + %.2f"%(fit[0],fit[1]) + 
                                 "\n                 N=" + str(round(N,0))+ "           Corr=" + str(round(corr_t,2)) 
                                 ,prop=dict(size=16,color='black',fontweight="bold"),frameon=False, loc=9)

    ax2.add_artist(anchored_text)   
    
    plt.tight_layout()
    
    return(plt.show())



def ENSO_mei(nombre,Mod_or_Obs,rest_trend=True,show_trend=False):
    """
    Parameters
    ----------
    nombre : string
        nombre estacion elejis
        ej : 'CHR', 'RAP', 'SMO', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'POCS05',
       'POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30', 'GUAM'
    Mod_or_Obs : string
        Selecionar el calculo para modelo o para 'obs' o 'mod' 
        ej:'obs'
    rest_trend : operador logico True o False, optional
        True calcula el resto de la tendencia para las conc de CO. The default is True.
        ej: True
    show_trend : Operador logico True o False
        Añade un grafico que muestra como es la tendencia. The default is False.
        

    Returns : Un subplot para scatter plot con las correlaciones anomalas de ENSO y CO mas algunos estadist.
    -------
    por Camilo M. 12/5/2020.

    """
        # Lectura de datos
    
    model_CO , name  = leerModel()                                            # Carga los datos y los nombres del Modelo en un Datafame 
    obs_CO   , name  = leerObs()                                              # Carga los datos y los nombres de las Obs en un Dataframe 

    ### Define Datafrmae para Obs y Mod    

    df        = pd.DataFrame()   
    df['obs'] = obs_CO[nombre]
    df['mod'] = model_CO[nombre]        
    
    
    # Define mei

    mei = pd.read_csv( 'meiv2.data.txt',delim_whitespace=True,header=None)
    mei = mei.values
    mei = mei[:,1:13]
    mei = mei.reshape(12*42)

    
    fechas = pd.date_range('1979-01-01', '2021-01-01', freq='M')           # Define las fechas de los modelos
    mei = pd.DataFrame(mei, index = fechas)

    # Acopla fechas

    fecha_inical = '1994-01-01'
    fecha_final = '2014-12-31'
    
    mei = mei.loc[fecha_inical : fecha_final]
    df  = df.loc[fecha_inical : fecha_final]

    ### Promedio movil de 2 meses
    
    df = df.rolling(window=2).mean()

    #Calculo climatologia
    
    mat_h = df.set_index(df.index.month, append=True)[Mod_or_Obs].unstack().mean()
    a = pd.concat([mat_h] * int(len(df.index)/12), axis=0)
    clim_obs = pd.Series( a.values ,index = df.index)

    ## Concentracion - Climatologia
    anomal_obs = df[Mod_or_Obs] - clim_obs 

    #Calculo de tendencia
    
    time       = anomal_obs.index 
    x          = np.arange(time.size)                                          # = array([0, 1, 2, ..., 3598, 3599, 3600])
    y          = anomal_obs.fillna(anomal_obs.mean())                                            # Saca Nans
    fit        = np.polyfit(x, y, 1)
    fit_fn     = np.poly1d(fit)
    trend_line = fit_fn(x)
    
    ##Verifica trend line 
    if show_trend == True:
        plt.figure() ; plt.plot(anomal_obs.index, anomal_obs.values, 'k-') ; plt.plot(anomal_obs.index, fit_fn(x), '-',color='red') ; plt.ylabel('CO [ppmb]')
        plt.title(nombre+': Trend Line ' ,fontsize=14)
    
    ## Concentracion - Trend line
    if rest_trend == True:
        anomal_obs = anomal_obs - trend_line 


    ## Define nuevo Dataframe
    df_clima = pd.DataFrame()
    df_clima['anomal_obs'] = anomal_obs

    df_clima['anomal_ens'] = mei    

                                                      

    #Calculo de tendencia ENSO vs ANOM CO
    
    y          = df_clima['anomal_obs'].fillna(df_clima['anomal_obs'].mean())                                          # = array([0, 1, 2, ..., 3598, 3599, 3600])
    x          = df_clima['anomal_ens']                                            # Saca Nans
    fit        = np.polyfit(x, y, 1)
    fit_fn     = np.poly1d(fit)
    trend_line = fit_fn(x)

        
    #################### Parametros para el plot##############################

    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    
#    plt.figure(figsize=(10,5))

    if Mod_or_Obs == 'obs':
        ax2 = plt.subplot(2,1,1)
    elif Mod_or_Obs == 'mod':
        ax2 = plt.subplot(2,1,2)            

    plt.plot(np.zeros(2),[-38,38],'-k',alpha=0.8,linewidth=0.8) ; plt.ylim([-38,38])
    plt.plot([-2.5,2.5],np.zeros(2),'-k',alpha=0.8,linewidth=0.8)   ; plt.xlim([-2.2,2.2])

    plt.plot([0.5, 0.5],[-38,38],':k',alpha=0.6,linewidth=0.8) 
    plt.plot([-0.5, -0.5],[-38,38],':k',alpha=0.6,linewidth=0.8)

    plt.plot(df_clima['anomal_ens'],trend_line, '-k',linewidth=2)
     
    # Scaterr, ciclo para pintar cada color niña o niño    
    for i,j in zip(df_clima['anomal_ens'],df_clima['anomal_obs']):
        if i>0.5:
            plt.scatter(i,j,color='red',alpha=0.8)
        elif i<-0.5:
            plt.scatter(i,j,color='blue',alpha=0.8)
        else:
            plt.scatter(i,j,color='gray',alpha=0.9)
            
    # Condicion para el Titulo de Obs o Mod
    
    if Mod_or_Obs == 'obs':
        plt.ylabel('Obs Anomaly CO (ppbv)',fontsize=18)
    elif Mod_or_Obs == 'mod':
        plt.ylabel('Mod Anomaly CO (ppbv)',fontsize=18)
        
    plt.xlabel('ENSO MEI$_{v2}$ ',fontsize=18)


    aux_nino  = df_clima[ (df_clima['anomal_ens']>0.5) ]                     # Niños extremos, descomentar
    corr_nino = aux_nino.corr(method ='pearson') ; corr_nino = corr_nino.values[0,1]
    Nnan = np.sum(np.isnan(aux_nino['anomal_obs']))
    N = len(aux_nino)-Nnan
    anchored_text = AnchoredText( "Corr=" + str(round(corr_nino,2)) +
                                 "\n N=" + str(round(N,0)) , prop=dict(size=16,color='red',fontweight="bold"),frameon=False, loc=1)
    ax2.add_artist(anchored_text)

    aux_nina  = df_clima[ (df_clima['anomal_ens']<-0.5) ]                     # Niños extremos, descomentar
    corr_nina = aux_nina.corr(method ='pearson') ; corr_nina = corr_nina.values[0,1]
    Nnan = np.sum(np.isnan(aux_nina['anomal_obs']))
    N = len(aux_nina)-Nnan
    anchored_text = AnchoredText( "Corr=" + str(round(corr_nina,2)) +
                                 "\n N=" + str(round(N,0))  , prop=dict(size=16,color='blue',fontweight="bold"),frameon=False, loc=2)
    ax2.add_artist(anchored_text)

    corr_t = df_clima.corr(method ='pearson') ; corr_t = corr_t.values[0,1]
    Nnan = np.sum(np.isnan(df_clima['anomal_obs']))
    N = len(df_clima['anomal_obs'])-Nnan
    
    if 0 < fit[1] :
        anchored_text = AnchoredText( "CO$_{Anomaly}$ (ppbv) = %.2f$\cdot$ENSO$_{MEI_{v2}}$+%.2f"%(fit[0],fit[1]) + 
                                     "\n                 N=" + str(round(N,0))+ "           Corr=" + str(round(corr_t,2)) 
                                     ,prop=dict(size=16,color='black',fontweight="bold"),frameon=False, loc=9)
    if 0 > fit[1] :
        anchored_text = AnchoredText( "CO$_{Anomaly}$ (ppbv) = %.2f$\cdot$ENSO$_{MEI_{v2}}$%.2f"%(fit[0],fit[1]) + 
                                     "\n                 N=" + str(round(N,0))+ "           Corr=" + str(round(corr_t,2)) 
                                     ,prop=dict(size=16,color='black',fontweight="bold"),frameon=False, loc=9)


    ax2.add_artist(anchored_text)   
    
    plt.tight_layout()
    
    return(plt.show())





def FScatterNS(fecha1,fecha2,ext=None):
    '''

    '''
        
    from pylab import rcParams
    rcParams['figure.figsize'] = 5, 5
    
    mod_CO, name  = leerModel()           # Carga los datos y los nombres del Modelo en un Datafame 
    obs_CO, name  = leerObs()            # Carga los datos y los nombres de las Obs en un Dataframe 

    # Splitting into northern and southern hemisphere stations
    mod_HS = pd.DataFrame()
    aux_HS =  ['RAP', 'SMO', 'POCS05','POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30']
    for stn in aux_HS:
        mod_HS = pd.concat([mod_HS, mod_CO[stn]],axis=0)
   
    obs_HS = pd.DataFrame()
    aux_HS =  ['RAP', 'SMO', 'POCS05','POCS10', 'POCS15', 'POCS20', 'POCS25', 'POCS30']
    for stn in aux_HS:
        obs_HS = pd.concat([obs_HS, obs_CO[stn]],axis=0)
   
    mod_HN = pd.DataFrame()
    aux_HN =  ['CHR', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'GUAM']
    for stn in aux_HN:
        mod_HN = pd.concat([mod_HN, mod_CO[stn]],axis=0)
   
    obs_HN = pd.DataFrame()
    aux_HN = ['CHR', 'POCN15', 'POCN10', 'POCN05', 'POC000', 'GUAM']
    for stn in aux_HN:
        obs_HN = pd.concat([obs_HN, obs_CO[stn]],axis=0)
  
    rcParams['figure.figsize'] = 8, 8

    plt.figure()
    ax= plt.subplot(1,1,1)

    plt.rcParams["font.family"] = "Times New Roman"                            # Parametros para letras y tamaños
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16


    vobsS=obs_HS.loc[fecha1 : fecha2]
    vmodS=mod_HS.loc[fecha1 : fecha2]

    NS=float(np.size(vobsS)-np.sum(np.isnan(vobsS)))
    
    vobsN=obs_HN.loc[fecha1 : fecha2]
    vmodN=mod_HN.loc[fecha1 : fecha2]

    NH=float(np.size(vobsN)-np.sum(np.isnan(vobsN))) 
  
    
    #Calculatig mean fractional bias for both hemispheres
    aa=float(vobsS.mean())
    bb=float(vmodS.mean())
    #FBS=((aa-bb)/((aa+bb)*0.5))*-1.   
    BS=bb-aa
    
    aa=float(vobsN.mean())
    bb=float(vmodN.mean())
    #FBN=((aa-bb)/((aa+bb)*0.5))*-1.    
    BN=bb-aa

    
    plt.scatter(vobsS,vmodS, c="blue", alpha=0.7, marker='o')
    plt.axes().set_aspect('equal', 'box')
    plt.xlim([40,150])
    plt.ylim([40,150])
    plt.xlabel('Observation (ppbv)',fontsize=18) 
    plt.ylabel('Model (ppbv)', fontsize=18)
    
    plt.scatter(vobsN,vmodN, c="red", alpha=0.3, marker='o')
    plt.axes().set_aspect('equal', 'box')
    plt.xlim([40,150])
    plt.ylim([40,150])
    
    lino=[40,150]
    plt.plot(lino,lino,'-k')
    #plt.title(name[indice], fontsize=20) 
    at1 =  AnchoredText(' N(SH) = '+ str(int(NS))+"\n Bias SH=" + str(round(BS,1)) +' ppbv', loc='upper left', prop=dict(size=16), frameon=False)
    ax.add_artist(at1)
   
    at2 =  AnchoredText(' N(NH) = '+ str(int(NH))+"\n Bias NH=" + str(round(BN,1)) +' ppbv', loc='upper center', prop=dict(size=16), frameon=False)
    #at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at2)

    plt.legend(['1:1','SH','NH'],loc='lower right',ncol=3,frameon=False
               , fontsize=16)     
    
    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    if ext ==None:
        ext='png'
    plt.savefig('FIG_Scat_CO//' +'All' +'.'+ext, dpi=600)    
    return(plt.show())     
        