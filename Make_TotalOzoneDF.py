import pandas as pd  
import numpy as np  
from datetime import datetime
import astropy.time
import dateutil.parser


# Code to read data and convert it to a format I can analyze
# DEBilt

df = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TotalOzone.txt',  sep = "\s *", engine="python", names = ['jdate','mean', 'anamoly'])


julian_dates = df.jdate.tolist()
#julian_dates = julian_dates[1:]
dates = [0]*len(julian_dates)

for d in range(len(julian_dates)):
    tmp = julian_dates[d]
    tmp = float(tmp)
    tmp = int(tmp)
    julian_dates[d] = int(tmp)

    dates[d] = astropy.time.Time(julian_dates[d]-14,format='jd')
    dates[d] = dates[d].iso

    dates[d] = pd.to_datetime(dates[d]).date()

print(len(dates),dates)

df['date'] = dates
# df.anamoly_dnz =
print(list(df))


df['dateindex'] = pd.to_datetime(df['date'], format='%Y-%m')
df.set_index('date', inplace=True)
print('df', len(df), list(df))

df['monthly_mean'] = df['mean'] - df['anamoly']
df['rel_anamoly'] = (df['mean'] - df['monthly_mean'])/ df['monthly_mean']

# df.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TotalOzone_monthlymean.csv')
