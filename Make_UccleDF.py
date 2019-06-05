import pandas as pd  
import numpy as np  
from datetime import datetime

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

df = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1kmlev_monthlymeans.dat',  sep = "\s *", engine="python", names = date)

alt = ['']*36
for ia in range(36): alt[ia] = str(ia)+'km'

dfT = df.T
dfT.columns = alt

dfT.to_csv('/home/poyraden/MLR_Uccle/1km_monthlymean.csv')
