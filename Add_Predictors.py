import numpy as np
import pandas as pd
import astropy.time
from datetime import datetime
from Extend_Predictors import load_enso, load_independent_linear, load_qbo, load_solar, load_eesc


## IMPORTANT, change the boolean if you want to make the standard predictors or the one for
## total column

totalcolumn = True


# EESC#
def load_eesc():
    """
    Extra note: normally this is not in LOTUS ilt model, but it is one of the proxies Roeland used for total column

    Calculates an EESC from the polynomial values [9.451393e-10, -1.434144e-7, 8.5901032e-6, -0.0002567041,
    0.0040246245, -0.03355533, 0.14525718, 0.71710218, 0.1809734]
    """
    poly = [9.451393e-10, -1.434144e-7, 8.5901032e-6, -0.0002567041,
            0.0040246245, -0.03355533, 0.14525718, 0.71710218, 0.1809734]
    np.polyval(poly, 1)

    num_months = 12 * (pd.datetime.now().year - 1979) + pd.datetime.now().month
    num_months = 600
    index = pd.date_range('1969-01-01', periods=num_months, freq='M').to_period(freq='M')
    return pd.Series([np.polyval(poly, month/12) for month in range(num_months)], index=index)


#   #   #   #   #   #
#  Tropopause Pressure txt and convert it to dates and normalize it
#   #   #   #   #   #

columnStr = ['jdate', 'pressure', 'pressure_ano']
tropop = pd.read_csv('/home/poyraden/MLR_Uccle/Files/newProxies/tropop.txt', header = None, sep = "\s *",
                     engine="python", names=columnStr)

julian_dates = tropop['jdate'].tolist()
dates = [0]*len(julian_dates)

for d in range(len(julian_dates)):
    tmp = julian_dates[d]
    tmp = float(tmp)
    tmp = int(tmp)
    julian_dates[d] = int(tmp)

    dates[d] = astropy.time.Time(julian_dates[d]-14,format='jd')
    dates[d] = dates[d].iso
    dates[d] = pd.to_datetime(dates[d]).date()

tropop['date'] = dates
pd.to_datetime(tropop['date'], format='%Y-%m')
tropop.set_index('date', inplace=True)

tropop['tropop_pre'] = (tropop.pressure - np.nanmean(tropop.pressure))/np.nanstd(tropop.pressure)
#tropop['pressure_ano_nor'] = (tropop.two - np.nanmean(tropop.two))/np.nanstd(tropop.two)
tropop = tropop.drop(columns={'jdate','pressure', 'pressure_ano'})

#   #   #   #   #   #
# Surface Temperature
#   #   #   #   #   #

columnStr = ['jdate', 'temp', 'ano']
tempsur = pd.read_csv('/home/poyraden/MLR_Uccle/Files/newProxies/tempsurf.txt', header = None, sep = "\s *",
                     engine="python", names=columnStr)

julian_dates = tempsur['jdate'].tolist()
dates = [0]*len(julian_dates)

for d in range(len(julian_dates)):
    tmp = julian_dates[d]
    tmp = float(tmp)
    tmp = int(tmp)
    julian_dates[d] = int(tmp)

    dates[d] = astropy.time.Time(julian_dates[d]-14,format='jd')
    dates[d] = dates[d].iso
    dates[d] = pd.to_datetime(dates[d]).date()

tempsur['date'] = dates
pd.to_datetime(tempsur['date'], format='%Y-%m')
tempsur.set_index('date', inplace=True)

tempsur['temp_nor'] = (tempsur.temp - np.nanmean(tempsur.temp))/np.nanstd(tempsur.temp)
# tempsur['tempano_nor'] = (tempsur.ano - np.nanmean(tempsur.ano))/np.nanstd(tempsur.ano)
tempsur = tempsur.drop(columns={'jdate','temp', 'ano'})

#   #   #   #   #   #
#  Temperature @ 100hPa
#   #   #   #   #   #

columnStr = ['jdate', 'temp', 'ano']
temp100 = pd.read_csv('/home/poyraden/MLR_Uccle/Files/newProxies/temp100.txt', header = None, sep = "\s *",
                     engine="python", names=columnStr)

julian_dates = temp100['jdate'].tolist()
dates = [0]*len(julian_dates)

for d in range(len(julian_dates)):
    tmp = julian_dates[d]
    tmp = float(tmp)
    tmp = int(tmp)
    julian_dates[d] = int(tmp)

    dates[d] = astropy.time.Time(julian_dates[d]-14,format='jd')
    dates[d] = dates[d].iso
    dates[d] = pd.to_datetime(dates[d]).date()

temp100['date'] = dates
pd.to_datetime(temp100['date'], format='%Y-%m')
temp100.set_index('date', inplace=True)

temp100['temp100_nor'] = (temp100.temp - np.nanmean(temp100.temp))/np.nanstd(temp100.temp)
# temp100['tempano_nor'] = (temp100.ano - np.nanmean(temp100.ano))/np.nanstd(temp100.ano)
temp100 = temp100.drop(columns={'jdate','temp', 'ano'})


#   #   #   #   #   #
# AO 2018
#   #   #   #   #   #

columnStr = ['year', 'month', 'day','ao']
ao = pd.read_csv('/home/poyraden/MLR_Uccle/Files/newProxies/AO2018.txt', header = None, sep = "\s *",
                     engine="python", names=columnStr)
ao['date'] = pd.to_datetime(ao[['year', 'month', 'day']])
ao.set_index('date', inplace=True)
ao = ao.resample('MS').mean()

ao = ao.drop(columns={'year','month', 'day'})

ao['AO'] = (ao.ao - np.nanmean(ao.ao))/np.nanstd(ao.ao)
ao = ao.drop(columns = 'ao')
ao = ao.loc['1969-01-01':'2018-12-01'] # to have the same time period for all proxies


#   #   #   #   #   #
# NOI
#   #   #   #   #   #
columnStr = ['date', 'what','noi']
noi = pd.read_csv('/home/poyraden/MLR_Uccle/Files/newProxies/NOI_NOAA2018.txt', header = None, sep = "\s *",
                     engine="python", names=columnStr)
noi['date'] = pd.to_datetime(noi['date'], format='%d-%b-%Y')
noi['date'] = noi['date'] - pd.offsets.MonthBegin(1, normalize=True)
noi.set_index('date', inplace=True)
noi = noi.drop(columns= 'what')
noi['noi_nor'] = (noi.noi - np.nanmean(noi.noi))/np.nanstd(noi.noi)
noi = noi.loc['1969-01-01':'2018-12-01']

#   #   #   #   #   #
# tele_index EA
#   #   #   #   #   #

columnStr = ['year', 'month', 'NAO', 'EA','WP', 'EP_NP','PNA', 'EA_WR',
             'SCA', 'TNH', 'POL', 'PT', 'Expl_Var']
tele = pd.read_csv('/home/poyraden/MLR_Uccle/Files/newProxies/tele_index.nh',
                   header = None, sep = "\s *",
                   engine="python", names=columnStr, skiprows = 19)
tele['day'] = len(tele) * [1]
tele['date'] = pd.to_datetime(tele[['year', 'month','day']])
tele.set_index('date', inplace=True)
tele = tele.drop(columns={'year','month', 'day'})

tele = tele.loc['1969-01-01':'2018-12-01'] # to have the same time period for all proxies

#   #   #   #   #   #
#AOD
#   #   #   #   #   #

columnStr = ['bdate', 'global_aod', 'north_aod', 'south_aod']
aod1 = pd.read_csv('/home/poyraden/MLR_Uccle/Files/teleconnection_indices/AOD.txt', header = None, sep = "\s *",
                   engine="python", names = columnStr)
aod1['date'] = pd.date_range(start='1850-01-01', end='2012-09-01', freq = 'MS')

aod1.set_index('date', inplace=True)
aod1 = aod1.drop(columns={'bdate'})

mean_glob = np.nanmean(aod1.loc['2009-01-01':'2012-09-01']['global_aod'].tolist())
mean_north = np.nanmean(aod1.loc['2009-01-01':'2012-09-01']['north_aod'].tolist())
mean_south = np.nanmean(aod1.loc['2009-01-01':'2012-09-01']['south_aod'].tolist())

aod2 = pd.DataFrame()
aod2['date'] = pd.date_range(start='2012-10-01', end='2018-12-01', freq = 'MS')
aod2['global_aod'] = [mean_glob] * len(aod2)
aod2['north_aod'] = [mean_north] * len(aod2)
aod2['south_aod'] = [mean_south] * len(aod2)

aod2.set_index('date', inplace=True)

frames = [aod1, aod2]
aod = pd.concat(frames)
aod = aod.loc['1969-01-01':'2018-12-01']

aod['global_nor'] = (aod.global_aod -  np.nanmean(aod.global_aod))/ np.nanstd(aod.global_aod)
aod['north_nor'] = (aod.north_aod -  np.nanmean(aod.north_aod))/ np.nanstd(aod.north_aod)
aod['south_nor'] = (aod.south_aod -  np.nanmean(aod.south_aod))/ np.nanstd(aod.south_aod)


#   #   #   #   #   #



new_predictors = tempsur
new_predictors['AO'] = ao.AO
new_predictors['pre_tropop'] = tropop['tropop_pre']
new_predictors['temp_sur'] = tempsur['temp_nor']
new_predictors['NOI'] = noi['noi_nor']
new_predictors['EA'] = tele['EA']
new_predictors['AOD'] = aod.global_nor
## only for total column
if totalcolumn:
    new_predictors['temp_100'] = temp100['temp100_nor']
    new_predictors['EAWR'] = tele['EA_WR']
    new_predictors['NAO'] = tele['NAO']



# now make the dataframe for predictors

linear_trends = load_independent_linear(pre_trend_end='1997-01-01', post_trend_start='2000-01-01')
print('linear trend', list(linear_trends))
enso = load_enso(lag_months= 0 )
print('enso', type(enso), list(enso))
solar = load_solar()
print('solar', type(solar),list(solar))
QBO = load_qbo(pca = 2)
print('QBO', list(QBO))

ext_predictor = pd.DataFrame()

# extende solar dates
ex_dates = pd.date_range(start='2018-02', end='2018-12', freq = 'MS')

value = solar.loc['2018-01-01']['solar_mm']
values = [value] * len(ex_dates)
solar2 = pd.DataFrame(values, index= ex_dates, columns=['solar_mm'])
solar = solar.append(solar2)
solar['nor'] = (solar.solar_mm - np.mean(solar.solar_mm))/np.std(solar.solar_mm)
norsolar = solar.nor.tolist()
eesc = load_eesc()
eesc_nor = (eesc - np.mean(eesc))/np.std(eesc)

predictors_uccle = linear_trends
predictors_uccle['enso'] = enso
predictors_uccle.loc['2018-12']['enso'] = predictors_uccle.loc['2018-11']['enso']
predictors_uccle['qboA'] = (QBO.pca - QBO.pca.mean())/QBO.pca.std()
predictors_uccle['qboB'] = (QBO.pcb - QBO.pcb.mean())/QBO.pcb.std()
predictors_uccle['solar'] = norsolar
# this is only for the total column
if totalcolumn:predictors_uccle['EESC'] = eesc_nor


# missing dates from newpredictors need to be removed from predictors_uccle
predictors_uccle.index = predictors_uccle.index.to_timestamp()

datelist1 = new_predictors.index.tolist()
datelist2 = predictors_uccle.index.date.tolist()

d1 = [''] * len(datelist1); d2 = [''] * len(datelist2)
for d in range(len(datelist1)):
    d1[d] = datelist1[d].strftime('%Y-%m-%d')
for di in range(len(datelist2)):
    d2[di] = datelist2[di].strftime('%Y-%m-%d')

set1 = set(d1)
set2 = set(d2)
difference = set1.symmetric_difference(set2)
print(len(difference), difference)
difference = list(difference)
print(len(difference))
print(difference[0:10])

difdate = [0]* 41

for j in range(41):
    difdate[j] = datetime.strptime(difference[j], '%Y-%m-%d')

predictors_uccle = predictors_uccle.drop(difdate)
print(len(predictors_uccle))


predictors_uccle['AO'] =  new_predictors.AO.tolist()
predictors_uccle['AOD'] = new_predictors['AOD'].tolist()

if totalcolumn:
    predictors_uccle['temp_100'] = new_predictors['temp_100'].tolist()
    predictors_uccle['EAWR'] = new_predictors['EAWR'].tolist()
    predictors_uccle['NAO'] = new_predictors['NAO'].tolist()
else:
    predictors_uccle['pre_tropop'] = new_predictors['pre_tropop'].tolist()
    predictors_uccle['temp_sur'] = new_predictors['temp_sur'].tolist()
    predictors_uccle['NOI'] = new_predictors['NOI'].tolist()
    predictors_uccle['EA'] = new_predictors['EA'].tolist()


if totalcolumn:
    predictors_uccle.to_csv('/home/poyraden/MLR_Uccle/Files/TotalColumnPredictors_ilt.csv')
else:
    predictors_uccle.to_csv('/home/poyraden/MLR_Uccle/Files/NewPredictors_ilt.csv')


