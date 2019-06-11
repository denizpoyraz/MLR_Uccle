import pandas as pd
import numpy as np
from datetime import datetime
import statistics

uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean.csv')

uccle.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
uccle['date'] = pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

uc = {}
uct = {}
uct2 = {}

alt = [''] * 36

jan = [[0] * 50] * 36;
feb = [[0] * 50] * 36;
mar = [[0] * 50] * 36;
apr = [[0] * 50] * 36;
may = [[0] * 50] * 36;
jun = [[0] * 50] * 36;
jul = [[0] * 50] * 36;
aug = [[0] * 50] * 36;
sep = [[0] * 50] * 36;
oct = [[0] * 50] * 36;
nov = [[0] * 50] * 36;
dec = [[0] * 50] * 36

jan_mean = [0] * 36;
feb_mean = [0] * 36;
mar_mean = [0] * 36;
apr_mean = [0] * 36;
may_mean = [0] * 36;
jun_mean = [0] * 36;
jul_mean = [0] * 36;
aug_mean = [0] * 36;
sep_mean = [0] * 36;
oct_mean = [0] * 36;
nov_mean = [0] * 36;
dec_mean = [[0] * 50] * 36

for ir in range(36):  # per each km
    alt[ir] = str(ir) + 'km'
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
alt2 = [''] * 36

# now subtract the monthly means from each year and the corresponding month

for ir2 in range(36):  # per each km
    alt[ir2] = str(ir2) + 'km'
    alt2[ir2] = str(ir2) + 'km_ds'

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
all.to_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_all_divided.csv')

