#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 22:47:47 2020

@author: menares
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13

plt.figure(figsize=(8,8))

# set up orthographic map projection with
# use low resolution coastlines.
map = Basemap(projection='ortho',lat_0=-20,lon_0=-165,resolution='l')

# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.10)
map.drawcountries(linewidth=0.20)
#map.fillcontinents(color='tan',lake_color='lightblue') # color= color='coral',lake_color='aqua'

# draw the edge of the map projection region (the projection limb)
map.drawmapboundary(fill_color='aqua')

# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))
# make up some data on a regular lat/lon grid.


lats = [1.7, -27.16, -14.25, 15, 10, 5 , 0 , -5 ,-10, -15, -20, -25 , -30, 13.39, -7.6, -18.15, -0.9]
lons = [ -157.1,-109.4, -170.6, -145, -149, -151, -155, -159, -161, -164, -167, -171, -176, -144.6, 112.6,178.45, -86.6] 

x, y = map(lons, lats)

def anotar_pacifico(altura,xx,yy):
    plt.annotate( altura , xy=(xx, yy),  xycoords='data',
                    xytext=(5, -3), textcoords='offset points',
                    color='black',fontsize=13)

anotar_pacifico('15°N',x[3],y[3])
anotar_pacifico('10°N',x[4],y[4])
anotar_pacifico('5°N',x[5],y[5])
anotar_pacifico('0°',x[6],y[6])
anotar_pacifico('5°S',x[7],y[7])
anotar_pacifico('10°S',x[8],y[8])
anotar_pacifico('15°S',x[9],y[9])
anotar_pacifico('20°S',x[10],y[10])
anotar_pacifico('25°S',x[11],y[11])
anotar_pacifico('30°S',x[12],y[12])


plt.annotate('Chr.Island', xy=(x[0], y[0]),  xycoords='data',
                xytext=(-65, 15), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)

plt.annotate('Rapa Nui', xy=(x[1], y[1]),  xycoords='data',
                xytext=(20, 10), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)

plt.annotate('Guam', xy=(x[13], y[13]),  xycoords='data',
                xytext=(-60, 15), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)

plt.annotate('Samoa', xy=(x[2], y[2]),  xycoords='data',
                xytext=(-60, -0), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)

plt.annotate('Watukosek', xy=(x[14], y[14]),  xycoords='data',
                xytext=(25, 10), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)

plt.annotate('Suva', xy=(x[15], y[15]),  xycoords='data',
                xytext=(-55, 0), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)

plt.annotate('San Cristobal', xy=(x[16], y[16]),  xycoords='data',
                xytext=(-60, 20), textcoords='offset points',
                color='black',
                arrowprops=dict(arrowstyle="fancy", color='k')
                ,fontsize=13)



# compute native map projection coordinates of lat/lon grid.
# contour data over the map.
map.scatter(x, y, 30, marker='o',color='red')
map.scatter(x[-3:len(x)], y[-3:len(x)],30, marker='x',color='white')
map.scatter(x[1], y[1],30, marker='x',color='white')
map.scatter(x[2], y[2],30, marker='x',color='white')


map.etopo()

#plt.tight_layout()
plt.show()
#plt.savefig('Loc_stn_png',dpi=600)


# from netCDF4 import Dataset


# fh = Dataset('o3_monthly_ts.nc', mode='r')
# names = fh.variables['names'][:]
# lat = fh.variables['lat'][:]
# lon = fh.variables['lon'][:]
# time = fh.variables['time'][:]
# conc = fh.variables['conc'][:]

# fechas = pd.date_range('1980-01-01', '2017-11-30', freq='M') 
# conc_stn = conc[:,0,np.arange(20),np.arange(20)]


# df_o3 = pd.DataFrame(conc_stn, index= fechas, columns = names)

# df_o3.plot(figsize=(12,15.5),color='black',subplots=True,layout=(5, 4),ylim=[0,55]) ; plt.tight_layout()