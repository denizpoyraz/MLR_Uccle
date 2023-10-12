import pandas as pd  
import numpy as np  
from datetime import datetime
import astropy.time

# Code to read data and convert it to a format I can analyze
# Uccle

year = [0]*50; month = [12]*12
header = np.zeros((50, 12),dtype =int)

for iy in range(1969,2019):
    year[iy-1969] = iy
for im in range(12):
    month[im] = im+1

for i in range(50):
    for j in range(12):
        header[i][j] = int(header[i][j])
        header[i][j] = str(int(year[i]))+str(int(month[j]))
        
b = header.ravel()

bd = ['']*600
date = ['']*600
for k in range(600):
    bd[k] = str(b[k])
    date[k] = datetime.strptime(bd[k], '%Y%m')
    date[k] = date[k].strftime('%Y-%m-%d')

df = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1kmlev_monthlymeans.dat',  sep = "\s *", engine="python", names = date)
df_rel = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1kmlev_reltropop_monthlymeans.dat',  sep = "\s *", engine="python", names = date)
df_pre = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/plev_monthlymeans.dat',  sep = "\s *", engine="python", names = date)


alt = ['']*36
alt_rel = ['']*36

plev = [925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 50, 30, 20,10]
pre = ['']*14

for ia in range(36):
    alt[ia] = str(ia)+'km'

for ir in range(24,-12,-1):
    alt_rel[24-ir] = str(ir)+'km' #w.r.t. tropopause
    #print(ir, alt_rel[24-ir])

for p in range(14):
    pre[p] = str(plev[p])+'hPa'


dfT = df.T
dfT.columns = alt

dfT.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean.csv')


dfT_rel = df_rel.T
dfT_rel.columns = alt_rel

dfT_rel.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean_reltropop.csv')

dfT_pre = df_pre.T
dfT_pre.columns = pre

dfT_pre.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean_plev.csv')

# 500 meter resolution

df5 = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Uccle_vertprofabs500ppb.txt',  sep = "\s *", engine="python")


julian_dates = df5.columns.tolist()
julian_dates = julian_dates[1:]
dates = [0]*len(julian_dates)

for d in range(len(julian_dates)):
    tmp = julian_dates[d]
    tmp = float(tmp)
    tmp = int(tmp)
    julian_dates[d] = int(tmp)

    dates[d] = astropy.time.Time(julian_dates[d]-14,format='jd')
    dates[d] = dates[d].iso
    dates[d] = pd.to_datetime(dates[d]).date()

df5 = df5.drop(columns='-9999.0')
df5.columns = dates

# df5 = df5.drop(df5.index[12:36])
#df5 = df5.drop(df5.index[24:72])

# nkm = 12
nkm = 36 * 2 -1

df5T = df5.T

columns_ds = ['']* nkm

for c in range(nkm):
    a = c * 0.5
    columns_ds[c] =  str(a)+'km'
    #print(columns_ds[c])


df5T.columns = columns_ds

# dfT.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/IAGOS_1km_monthlymean.csv')
df5T.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean500.csv')

