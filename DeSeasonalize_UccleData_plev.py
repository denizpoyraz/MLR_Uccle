import pandas as pd
import numpy as np
from datetime import datetime
import statistics
import sys


uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_plev.csv')


#uccle = pd.read_csv('/Volumes/HD3/KMI//MLR_Uccle/Files/1km_monthlymean.csv')

uccle.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
uccle['date'] = pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

plev = [925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 50, 30, 20,10]


uc = {}
uct = {}
uct2 = {}

alt = [''] * 14

jan = [[0] * 50] * 14;
feb = [[0] * 50] * 14;
mar = [[0] * 50] * 14;
apr = [[0] * 50] * 14;
may = [[0] * 50] * 14;
jun = [[0] * 50] * 14;
jul = [[0] * 50] * 14;
aug = [[0] * 50] * 14;
sep = [[0] * 50] * 14;
oct = [[0] * 50] * 14;
nov = [[0] * 50] * 14;
dec = [[0] * 50] * 14

jan_mean = [0] * 14;
feb_mean = [0] * 14;
mar_mean = [0] * 14;
apr_mean = [0] * 14;
may_mean = [0] * 14;
jun_mean = [0] * 14;
jul_mean = [0] * 14;
aug_mean = [0] * 14;
sep_mean = [0] * 14;
oct_mean = [0] * 14;
nov_mean = [0] * 14;
dec_mean = [[0] * 50] * 14

for ir in range(14):  # per each km
    alt[ir] = str(plev[ir]) + 'hPa'
    uc[ir] = uccle[uccle[alt[ir]] > 0]
    uct[ir] = uc[ir]

    # v2
    # uc[ir][alt[ir]] = uccle[uccle[alt[ir]] > 0]
    # uct[ir] = uc[ir]

    jan[ir].clear();
    feb[ir].clear();
    mar[ir].clear();
    apr[ir].clear();
    may[ir].clear();
    jun[ir].clear()
    jul[ir].clear();
    aug[ir].clear();
    sep[ir].clear();
    oct[ir].clear();
    nov[ir].clear();
    dec[ir].clear()

    for i in (uct[ir][alt[ir]].index):

        if (pd.Timestamp(i).month == 1):
            # print('hey',alt[ir],  i, (uct[ir][alt[ir]].loc[pd.Timestamp(i)]))
            jan[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            jan[ir] = list(filter(lambda a: a != 0, jan[ir]))
        if (pd.Timestamp(i).month == 2):
            feb[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            feb[ir] = list(filter(lambda a: a != 0, feb[ir]))
        if (pd.Timestamp(i).month == 3):
            mar[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            mar[ir] = list(filter(lambda a: a != 0, mar[ir]))
        if (pd.Timestamp(i).month == 4):
            apr[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            apr[ir] = list(filter(lambda a: a != 0, apr[ir]))
        if (pd.Timestamp(i).month == 5):
            may[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            may[ir] = list(filter(lambda a: a != 0, may[ir]))
        if (pd.Timestamp(i).month == 6):
            jun[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            jun[ir] = list(filter(lambda a: a != 0, jun[ir]))
        if (pd.Timestamp(i).month == 7):
            jul[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            jul[ir] = list(filter(lambda a: a != 0, jul[ir]))
        if (pd.Timestamp(i).month == 8):
            aug[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            aug[ir] = list(filter(lambda a: a != 0, aug[ir]))
        if (pd.Timestamp(i).month == 9):
            sep[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            sep[ir] = list(filter(lambda a: a != 0, sep[ir]))
        if (pd.Timestamp(i).month == 10):
            oct[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            oct[ir] = list(filter(lambda a: a != 0, oct[ir]))
        if (pd.Timestamp(i).month == 11):
            nov[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            nov[ir] = list(filter(lambda a: a != 0, nov[ir]))
        if (pd.Timestamp(i).month == 12):
            dec[ir].append(uct[ir][alt[ir]].loc[pd.Timestamp(i)])
            dec[ir] = list(filter(lambda a: a != 0, dec[ir]))

        jan_mean[ir] = np.nanmean(jan[ir])
        feb_mean[ir] = np.nanmean(feb[ir])
        mar_mean[ir] = np.nanmean(mar[ir])
        apr_mean[ir] = np.nanmean(apr[ir])
        may_mean[ir] = np.nanmean(may[ir])
        jun_mean[ir] = np.nanmean(jun[ir])
        jul_mean[ir] = np.nanmean(jul[ir])
        aug_mean[ir] = np.nanmean(aug[ir])
        sep_mean[ir] = np.nanmean(sep[ir])
        oct_mean[ir] = np.nanmean(oct[ir])
        nov_mean[ir] = np.nanmean(nov[ir])
        dec_mean[ir] = np.nanmean(dec[ir])

print(jan_mean[0])
print(jan_mean[1])

dfde = pd.DataFrame()
alt2 = [''] * 14

# now subtract the monthly means from each year and the corresponding month

for ir2 in range(14):  # per each km
    alt2[ir2] = str(plev[ir2]) + 'hPa_ds'

    uct2[ir2] = uccle[uccle[alt[ir2]] > 0]
    # or uct[ir] = uc[ir].loc['1987-02-01':'2017-06-01']
    # uct[ir] = uc[ir]
    for i2 in (uct2[ir2][alt[ir2]].index):
        #
        # if (pd.Timestamp(i2).month == 1):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - jan_mean[ir2]
        # if (pd.Timestamp(i2).month == 2):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - feb_mean[ir2]
        # if (pd.Timestamp(i2).month == 3):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - mar_mean[ir2]
        # if (pd.Timestamp(i2).month == 4):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - apr_mean[ir2]
        # if (pd.Timestamp(i2).month == 5):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - may_mean[ir2]
        # if (pd.Timestamp(i2).month == 6):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - jun_mean[ir2]
        # if (pd.Timestamp(i2).month == 7):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - jul_mean[ir2]
        # if (pd.Timestamp(i2).month == 8):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - aug_mean[ir2]
        # if (pd.Timestamp(i2).month == 9):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - sep_mean[ir2]
        # if (pd.Timestamp(i2).month == 10):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - oct_mean[ir2]
        # if (pd.Timestamp(i2).month == 11):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - nov_mean[ir2]
        # if (pd.Timestamp(i2).month == 12):
        #     uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - dec_mean[ir2]
        if (pd.Timestamp(i2).month == 1):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - jan_mean[ir2])/jan_mean[ir2]
        if (pd.Timestamp(i2).month == 2):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - feb_mean[ir2])/feb_mean[ir2]
        if (pd.Timestamp(i2).month == 3):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - mar_mean[ir2])/mar_mean[ir2]
        if (pd.Timestamp(i2).month == 4):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - apr_mean[ir2])/apr_mean[ir2]
        if (pd.Timestamp(i2).month == 5):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - may_mean[ir2])/may_mean[ir2]
        if (pd.Timestamp(i2).month == 6):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - jun_mean[ir2])/jun_mean[ir2]
        if (pd.Timestamp(i2).month == 7):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - jul_mean[ir2])/jul_mean[ir2]
        if (pd.Timestamp(i2).month == 8):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - aug_mean[ir2])/aug_mean[ir2]
        if (pd.Timestamp(i2).month == 9):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - sep_mean[ir2])/sep_mean[ir2]
        if (pd.Timestamp(i2).month == 10):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - oct_mean[ir2])/oct_mean[ir2]
        if (pd.Timestamp(i2).month == 11):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - nov_mean[ir2])/nov_mean[ir2]
        if (pd.Timestamp(i2).month == 12):
            uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][alt[ir2]].loc[pd.Timestamp(i2)] - dec_mean[ir2])/dec_mean[ir2]

    dfde[alt2[ir2]] = uct2[ir2][alt[ir2]]

all = pd.concat([uccle, dfde], axis=1, sort=False)
#all.to_csv('/Volumes/HD3/KMI//MLR_Uccle/Files/1km_monthlymean_all.csv')

all.to_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_all_plev_relative.csv')
