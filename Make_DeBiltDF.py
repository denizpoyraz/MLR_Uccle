import pandas as pd  
import numpy as np  
from datetime import datetime
import astropy.time
import dateutil.parser

df = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_vertprofabs.txt',  sep = "\s *", engine="python")
df_rel = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_vertprofrel.txt',  sep = "\s *", engine="python")


julian_dates = df.columns.tolist()
julian_dates = julian_dates[1:]
dates = [0]*len(julian_dates)

for d in range(len(julian_dates)):
    tmp = julian_dates[d]
    tmp = float(tmp)
    tmp = int(tmp)
    julian_dates[d] = int(tmp)

    dates[d] = astropy.time.Time(julian_dates[d],format='jd')
    dates[d] = dates[d].iso
    dates[d] = pd.to_datetime(dates[d]).date()

df = df.drop(columns='-9999.0')
df.columns = dates
dfT = df.T

df_rel = df_rel.drop(columns='-9999.0')
df_rel.columns = dates
dfT_rel = df_rel.T



columns_ds = ['']*36
alt_rel = ['']*36

for c in range(36):
    columns_ds[c] =  str(c)+'km'

for ir in range(24,-12,-1):
    alt_rel[24-ir] = str(ir)+'km' #w.r.t. tropopause

dfT.columns = columns_ds
dfT_rel.columns = alt_rel

dfT.to_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean.csv')
dfT_rel.to_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean_reltropop.csv')

