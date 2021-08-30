import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker  as ticker
from datetime import datetime
import pandas as pd
      

#https://mesonet.agron.iastate.edu/request/download.phtml?network=AR__ASOS
#https://www.ncdc.noaa.gov/cdo-web/orders GHCND (CSV        
dateparse = lambda dates: [datetime.strptime(d, '%Y-%m-%d') for d in dates]
df = pd.read_csv('2697742.csv',parse_dates=['DATE'], date_parser=dateparse)
#df = pd.read_csv('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/AR000877500.csv.gz',parse_dates=['DATE'], date_parser=dateparse,compression='gzip')
df.replace( -9999 , np.nan,inplace=True)
df['TMAX'].fillna(method='ffill',inplace=True)
df['TMIN'].fillna(method='ffill',inplace=True)
df['TAVG'].fillna((df['TMIN']+df['TMAX'])/2,inplace=True)
df['month'] = df['DATE'].dt.month
df['day'] = df['DATE'].dt.day
df['year'] = df['DATE'].dt.year
df.sort_values(['DATE'],inplace=True)


# Past dataframe
# dn, min,max,....
#
gb = df.groupby(['month','day'])

past = \
pd.DataFrame({
'mean' : gb['TAVG'].mean(), 
'min' : gb['TAVG'].min() ,
'max' : gb['TAVG'].max() ,
'std' : gb['TAVG'].std() ,
'count' : gb['TAVG'].count() 

}).reset_index()


past['dn'] = past.index
past.drop(['month','day'], axis=1, inplace=True)
past['upper3s'] = past['mean'] + 2.101*past['std']/np.sqrt(past['count'])
past['lower3s'] = past['mean'] - 2.101*past['std']/np.sqrt(past['count'])

# this year 
gb = df[df['year']==2021].groupby(['month','day'])
thisyear = \
pd.DataFrame({
'mean' : gb['TAVG'].mean(), 
'min' : gb['TAVG'].min() ,
'max' : gb['TAVG'].max() ,
'std' : gb['TAVG'].std() ,
'count' : gb['TAVG'].count() 

}).reset_index()


plt.bar(past['dn'], past['max']-past['min'], 0.5, past['min'],color='#EED8AE',alpha=0.5,linewidth=0)
plt.bar(past['dn'], past['upper3s']-past['lower3s'], 0.5, past['lower3s'],color='#8B7E66',alpha=0.5,linewidth=0)
plt.plot(thisyear['mean'],color='#303030')
#plt.axis('scaled')


ax = plt.axes()    
ax.set_facecolor("None")
    
xt = np.array([-5,0,5,10,15,20,25,30,35])
ax.set_yticks(xt)
ax.yaxis.grid(color='#FFFFFF',zorder=3,linewidth=2, linestyle='-') # horizontal lines
ax.set_yticklabels([])


ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color("white")
ax.spines['left'].set_color('#CCCCCC')


ax.set_xticks([31,59,90,120,151,181,212,243,273,304,334,365])
ax.xaxis.grid(color='#8B7E66',zorder=3,linewidth=1, linestyle='dotted') # vertical lines
ax.xaxis.set_visible = False
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.set_xticks([15,45,75,105,135,165,195,228,258,288,320,350],minor=True)
ax.set_xticklabels(['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],minor=True)
ax.tick_params(axis='x', labelbottom=False) 

plt.xlabel("Mes")
plt.ylabel("Temperatura")

ax.text(0.5, 1,'Temperaturas Bahía Blanca',
     horizontalalignment='center',
     verticalalignment='center',
    transform = ax.transAxes, fontsize=24,color="#202020", backgroundcolor="white")

    

plt.show()