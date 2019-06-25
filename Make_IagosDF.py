import pandas as pd  
import numpy as np  
from datetime import datetime
import astropy.time
import dateutil.parser

#df = pd.read_csv('/home/poyraden/MLR_Uccle/Files/IAGOS_vertprof.txt',  sep = "\s *", engine="python")
df = pd.read_csv('/home/poyraden/MLR_Uccle/Files/IAGOS_vertprof500.txt',  sep = "\s *", engine="python")


julian_dates = df.columns.tolist()
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

df = df.drop(columns='-9999.0')
df.columns = dates

# df = df.drop(df.index[12:36])
df = df.drop(df.index[24:72])

# nkm = 12
nkm = 24

dfT = df.T

columns_ds = ['']* nkm

for c in range(nkm):
    a = c * 0.5
    columns_ds[c] =  str(a)+'km'


dfT.columns = columns_ds

# dfT.to_csv('/home/poyraden/MLR_Uccle/Files/IAGOS_1km_monthlymean.csv')
dfT.to_csv('/home/poyraden/MLR_Uccle/Files/IAGOS_1km_monthlymean500.csv')

