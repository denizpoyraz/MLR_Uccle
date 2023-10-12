from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from LOTUS_regression.predictors.seasonal import add_seasonal_components



clm = ['x', 'month', 'year', 'TO']
df = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/evomira2020_update.dat', sep = "\s *", engine="python", names = clm)
# df['dateindex'] = pd.to_datetime(df['date'], format='%Y%m%d')

df.loc[df.month < 10, 'month'] = '0' + df.loc[df.month < 10, 'month'].astype(str)

df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str)



dfn = df[['date', 'TO']]
dfn['Date'] = pd.to_datetime(dfn['date'], format='%Y-%m')

# dfn['Date'] = dfn['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m'))
dfn = dfn.set_index('Date')

print(dfn.index.month)

to_mmeans = [0] * 12

dfn['anomaly'] = 0

for i in range(1,13):
    j = i-1
    to_mmeans[j] = dfn[dfn.index.month == i].TO.mean()
    print(j,to_mmeans[j] )
    dfn.loc[dfn.index.month == i, 'anomaly'] = dfn.loc[dfn.index.month ==i, 'TO'] - to_mmeans[j]
    dfn.loc[dfn.index.month == i, 'rel_anomaly'] = (dfn.loc[dfn.index.month ==i, 'TO'] - to_mmeans[j])/to_mmeans[j]

print(dfn[0:3])

# dfn.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_smoothed.csv')