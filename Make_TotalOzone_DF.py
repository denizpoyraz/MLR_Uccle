from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from LOTUS_regression.predictors.seasonal import add_seasonal_components

clm = ['type', 'date', 'hour', 'x', 'TO', 'y', 'z', 't', 'p']
df = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/dobday.dat', sep = "\s *", engine="python", names = clm)
# df['dateindex'] = pd.to_datetime(df['date'], format='%Y%m%d')
df.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_daily.csv')

# df = df[df['date'] > 19710730]
dfm = df[['date', 'TO']]
dfm['Date'] = dfm['date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
dfm = dfm.set_index('Date')
dfm = dfm.resample('1M').mean()
# dfm = df.resample('M', on='dateindex').mean()

months = []
to_mmeans = [0] * 12

dfm['anomaly'] = 0

for i in range(1,13):
    j = i-1
    to_mmeans[j] = dfm[dfm.index.month == i].mean()[1]
    dfm.loc[dfm.index.month == i, 'anomaly'] = dfm.loc[dfm.index.month ==i, 'TO'] - to_mmeans[j]
    dfm.loc[dfm.index.month == i, 'rel_anomaly'] = (dfm.loc[dfm.index.month ==i, 'TO'] - to_mmeans[j])/to_mmeans[j]
    dfm.loc[dfm.index.month == i, 'rel_anomaly_v2'] = (dfm.loc[dfm.index.month ==i, 'TO'] - to_mmeans[j])/dfm['TO'].mean()


#
print(to_mmeans)

print(dfm[20:25])
# print(dfm.index.month)

dfm.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_monthly.csv')
