import numpy as np
import pandas as pd
import requests
from io import StringIO
from dateutil import relativedelta
import os
import appdirs
import time
from datetime import datetime
import xarray as xr



'''Code to extend ilt time series to the period of Uccle'''

''' main code from : https://arg.usask.ca/docs/LOTUS_regression/dev/_modules/LOTUS_regression/predictors/download.html'''

########################################################################################################

def load_linear(inflection=1997):
    """
    Returns two piecewise linear components with a given inflection point in value / decade.

    Parameters
    ----------
    inflection : int, Optional. Default 1997
    """

    start_year = pd.to_datetime('1969-01-01', format='%Y-%m-%d')
    end_year = pd.to_datetime('2018-12-01', format='%Y-%m-%d')

    r = relativedelta.relativedelta(end_year, start_year)
    num_months = r.years * 12 + r.months + 1

    start_year = 1969

    index = pd.date_range('1975-01', periods=num_months, freq='M').to_period(freq='M')
    pre = 1/120*pd.Series([t - 12 * (inflection - (start_year+1)) if t < 12 * (inflection - (start_year+1)) else 0 for t in range(num_months)], index=index,
                    name='pre')
    post = 1/120*pd.Series([t - 12 * (inflection - (start_year+1)) if t > 12 * (inflection - (start_year+1)) else 0 for t in range(num_months)], index=index,
                     name='post')
    return pd.concat([pre, post], axis=1)


########################################################################################################33#
def load_independent_linear(pre_trend_end='1997-01-01', post_trend_start='2000-01-01', start_year = '1969-01-01', end_year = '2018-12-01'):
    """
    Creates the predictors required for performing independent linear trends.

    Parameters
    ----------
    pre_trend_end: str, Optional. Default '1997-01-01'

    post_trend_start: str, Optional.  Default '2000-01-01'
    """
    NS_IN_YEAR = float(31556952000000000)

    start_year = pd.to_datetime('1969-01-01', format='%Y-%m-%d')
    end_year = pd.to_datetime('2018-12-01', format='%Y-%m-%d')

    r = relativedelta.relativedelta(end_year, start_year)
    num_months = r.years * 12 + r.months + 1

    # num_months = 12 * (pd.datetime.now().year - start_year) + pd.datetime.now().month
    # num_months = 12 * (end_year - start_year) + pd.datetime.now().month
    # num_months = ((end_year - start_year)/np.timedelta64(1, 'M'))
    #print('num months', num_months)

    index = pd.date_range('1969-01-01', periods=num_months, freq='M').to_period(freq='M')

    pre_delta = -1 * (index.to_timestamp() - pd.to_datetime(pre_trend_end)).values
    post_delta = (index.to_timestamp() - pd.to_datetime(post_trend_start)).values

    assert (pre_delta.dtype == np.dtype('<m8[ns]'))
    assert (post_delta.dtype == np.dtype('<m8[ns]'))
    ## np.dtype('datetime64[ns]') would equal np.dtype('>M8[ns]')

    # time difference in number of years
    pre_delta = pre_delta.astype(np.int64) / NS_IN_YEAR
    post_delta = post_delta.astype(np.int64) / NS_IN_YEAR


    pre_const = np.ones_like(pre_delta)
    pre_const[pre_delta < 0] = 0

    post_const = np.ones_like(post_delta)
    post_const[post_delta < 0] = 0

    # Check if we need a gap constant
    pre_plus_post = pre_const + post_const
    if np.any(pre_plus_post == 0):
        need_gap_constant = True

        gap_constant = np.ones_like(pre_plus_post)
        gap_constant[pre_plus_post == 1] = 0

        gap_constant = pd.Series(gap_constant, index=index, name='gap_const')
    else:
        need_gap_constant = False

    pre_delta[pre_delta < 0] = 0
    post_delta[post_delta < 0] = 0

    pre = pd.Series(-1 * pre_delta / 10, index=index, name='linear_pre')
    post = pd.Series(post_delta / 10, index=index, name='linear_post')

    post_const = pd.Series(post_const, index=index, name='post_const')
    pre_const = pd.Series(pre_const, index=index, name='pre_const')

    # startyear = 1969
    # inflection = 1997
    #
    # indexp = pd.date_range('1969-01', periods=num_months, freq='M').to_period(freq='M')
    # pre_pw = 1 / 120 * pd.Series(
    #     [t - 12 * (inflection - (startyear + 1)) if t < 12 * (inflection - (startyear + 1)) else 0 for t in
    #      range(num_months)], index=indexp,
    #     name='pwlt_pre')
    # post_pw = 1 / 120 * pd.Series(
    #     [t - 12 * (inflection - (startyear + 1)) if t > 12 * (inflection - (startyear + 1)) else 0 for t in
    #      range(num_months)], index=indexp,
    #     name='pwlt_post')
    #
    # if need_gap_constant:
    #     data = pd.concat([pre, post, pre_pw, post_pw, post_const, pre_const, gap_constant], axis=1)
    # else:
    #     data = pd.concat([pre, post, pre_pw, post_pw, post_const, pre_const], axis=1)

    if need_gap_constant:
        data = pd.concat([pre, post, post_const, pre_const, gap_constant], axis=1)
    else:
        data = pd.concat([pre, post, post_const, pre_const], axis=1)

    return data

########################################################################################################################
def load_independent_linear_all(pre_trend_end='1997-01-01', post_trend_start='2000-01-01', start_year = '1969-01-01', end_year = '2018-12-01'):


    NS_IN_YEAR = float(31556952000000000)

    start_year = pd.to_datetime('1969-01-01', format='%Y-%m-%d')
    end_year = pd.to_datetime('1996-12-01', format='%Y-%m-%d')
    # end_year = pd.to_datetime('2018-12-01', format='%Y-%m-%d')


    r = relativedelta.relativedelta(end_year, start_year)
    num_months = r.years * 12 + r.months + 1

    index = pd.date_range('1969-01-01', periods=num_months, freq='M').to_period(freq='M')

    pre_delta = -1 * (index.to_timestamp() - pd.to_datetime(end_year)).values
    post_delta = (index.to_timestamp() - pd.to_datetime(end_year)).values

    assert (pre_delta.dtype == np.dtype('<m8[ns]'))
    assert (post_delta.dtype == np.dtype('<m8[ns]'))
    ## np.dtype('datetime64[ns]') would equal np.dtype('>M8[ns]')

    # time difference in number of years
    pre_delta = pre_delta.astype(np.int64) / NS_IN_YEAR
    post_delta = post_delta.astype(np.int64) / NS_IN_YEAR

    ## always use post, which is a linear increase term))
    # pre = pd.Series( pre_delta / 10, index=index, name='linear_pre_all')
    post = pd.Series(post_delta / 10, index=index, name='linear_one')


    data = pd.concat([post], axis=1)


    return data

#######################################################################################################################

def load_linear(inflection=1997):

    """
    Returns two piecewise linear components with a given inflection point in value / decade.

    Parameters
    ----------
    inflection : int, Optional. Default 1997
    """

    start_year = pd.to_datetime('1969-01-01', format='%Y-%m-%d')
    end_year = pd.to_datetime('2018-12-01', format='%Y-%m-%d')

    r = relativedelta.relativedelta(end_year, start_year)
    num_months = r.years * 12 + r.months + 1

    start_year = 1969

    index = pd.date_range('1969-01', periods=num_months, freq='M').to_period(freq='M')
    pre = 1/120*pd.Series([t - 12 * (inflection - (start_year+1)) if t < 12 * (inflection - (start_year+1)) else 0 for t in range(num_months)], index=index,
                    name='pwlt_pre')
    post = 1/120*pd.Series([t - 12 * (inflection - (start_year+1)) if t > 12 * (inflection - (start_year+1)) else 0 for t in range(num_months)], index=index,
                     name='pwlt_post')
    return pd.concat([pre, post], axis=1)


def load_enso(lag_months=0):

    """
    Downloads the ENSO from https://www.esrl.noaa.gov/psd/enso/mei/data/meiv2.data

    for uccle https://www.esrl.noaa.gov/psd/enso/mei.old/table.html
    Parameters
    ----------
    lag_months : int, Optional. Default 0
        The numbers of months of lag to introduce to the ENSO signal
    """

    # data = pd.read_table('https://www.esrl.noaa.gov/psd/enso/mei/data/meiv2.data', skiprows=1, skipfooter=4, sep='\s+',
    #                     index_col=0, engine='python', header=None)

    data = pd.read_table('/home/poyraden/Analysis/MLR_Uccle/Files/enso_mei.dat', skiprows=1, sep='\s+',index_col=0,
                         engine='python', header=None)

    assert (data.index[0] == 1969)
    data = data.stack()
    data = data[data > -998]
    data.index = pd.date_range(start='1969-01-01', periods=len(data), freq='M').to_period()

    data = data.shift(lag_months)

    return data


def load_qbo(pca=3):
    """
    Loads the QBO from http://www.geo.fu-berlin.de/met/ag/strat/produkte/qbo/qbo.dat.  If pca is set to an integer (default 3) then
    that many principal components are taken.  If pca is set to 0 then the raw QBO data is returned.

    Parameters
    ----------
    pca : int, optional.  Default 3.

    Starts from 1969, need to be modified for different time periods

    In order to have filan format you need to:
    qbo['qboA_nor'] = (qbo.pca - qbo.pca.mean())/qbo.pca.std()
    qbo['qboB_nor'] = (qbo.pcb - qbo.pcb.mean())/qbo.pcb.std()
    """
    import sklearn.decomposition as decomp
    # yymm date parser
    def date_parser(s):
        s = int(s)
        return pd.datetime(2000 + s // 100 if (s // 100) < 50 else 1900 + s // 100, s % 100, 1)

    data = pd.read_fwf(StringIO(requests.get('http://www.geo.fu-berlin.de/met/ag/strat/produkte/qbo/qbo.dat').text),
                       skiprows=200, header=None,
                       colspecs=[(0, 5), (6, 10), (12, 16), (19, 23), (26, 30), (33, 37), (40, 44), (47, 51), (54, 58)],
                         delim_whitespace=True, index_col=1, parse_dates=True, date_parser=date_parser,
                         names=['station', 'month', '70', '50', '40', '30', '20', '15', '10'])
    data.index = data.index.to_period(freq='M')

    data.drop('station', axis=1, inplace=True)
    data = data[:-1]

    if pca > 0:
        from string import ascii_lowercase
        pca_d = decomp.PCA(n_components=pca)
        for idx, c in zip(range(pca), ascii_lowercase):
            data['pc' + c] = pca_d.fit_transform(data.values).T[idx, :]

    return data


def load_solar():
    """
    Gets the solar F10.7 from 'http://www.spaceweather.ca/data-donnee/sol_flux/sx-5-mavg-eng.php'.
    """
    sess = requests.session()
    sess.get('https://omniweb.gsfc.nasa.gov/')

    # today = datetime.today()
    today = pd.to_datetime('20181231', format='%Y%m%d', errors='ignore')

    page = sess.get(
        'https://omniweb.gsfc.nasa.gov/cgi/nx1.cgi?activity=retrieve&res=daily&spacecraft=omni2_daily&start_date=19690101&end_date={}&vars=50&scale=Linear&ymin=&ymax=&charsize=&symsize=0.5&symbol=0&imagex=640&imagey=480'.format(
            today.strftime('%Y%M%d')))
    print('pgae',
          'https://omniweb.gsfc.nasa.gov/cgi/nx1.cgi?activity=retrieve&res=daily&spacecraft=omni2_daily&start_date=19690101&end_date={}&vars=50&scale=Linear&ymin=&ymax=&charsize=&symsize=0.5&symbol=0&imagex=640&imagey=480'.format(
              today.strftime('%Y%M%d')))
    # Won't have data for today, find the largest possible range
    ##last_day = page.text[page.text.rindex('19631128 - ') + 11:page.text.rindex('19631128 - ') + 8 + 11]
    ##page = sess.get('https://omniweb.gsfc.nasa.gov/cgi/nx1.cgi?activity=retrieve&res=daily&spacecraft=omni2_daily&start_date=19631128&end_date={}&vars=50&scale=Linear&ymin=&ymax=&charsize=&symsize=0.5&symbol=0&imagex=640&imagey=480'.format(last_day))

    data = StringIO(page.text[page.text.rindex('YEAR'):page.text.rindex('<hr>')])

    solar = pd.read_csv(data, delimiter='\s+')
    solar = solar[:-1]
    solar['dt'] = pd.to_datetime((solar['YEAR'].astype('int') * 1000) + solar['DOY'].astype(int), format='%Y%j')
    solar = solar.set_index(keys='dt')
    solar = solar.where(solar['1'] != 999.9)
    # month;y means
    solar = solar.resample('MS').mean()
    solar['solar_mm'] = solar['1']
    solar = solar.drop(columns='1')
    solar = solar.drop(columns='DOY')
    solar = solar.drop(columns='HR')

    return solar

# def load_eesc():
#     """
#     Calculates an EESC from the polynomial values [9.451393e-10, -1.434144e-7, 8.5901032e-6, -0.0002567041,
#     0.0040246245, -0.03355533, 0.14525718, 0.71710218, 0.1809734]
#     """
#     poly = [9.451393e-10, -1.434144e-7, 8.5901032e-6, -0.0002567041,
#             0.0040246245, -0.03355533, 0.14525718, 0.71710218, 0.1809734]
#     np.polyval(poly, 1)
#
#     num_months = 12 * (pd.datetime.now().year - 1979) + pd.datetime.now().month
#     num_months = 600
#     index = pd.date_range('1969-01-01', periods=num_months, freq='M').to_period(freq='M')
#     return pd.Series([np.polyval(poly, month/12) for month in range(num_months)], index=index)


def load_giss_aod():
    """
    Loads the giss aod index from giss
    """
    filename = 'tau_map_2012-12.nc'

    save_path = os.path.join(appdirs.user_data_dir(), filename)
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Only fetch from the ftp if the file does not exist
    if not os.path.exists(save_path) or time.time():
        r = requests.get(r'https://data.giss.nasa.gov/modelforce/strataer/tau_map_2012-12.nc')

        with open(save_path, 'wb') as f:
            f.write(r.content)

    data = xr.open_dataset(save_path)

    data = data.mean(dim='lat')['tau'].to_dataframe()

    data.index = data.index.map(lambda row: pd.datetime(int(row.year), int(row.month), 1)).to_period(freq='M')
    data.index.names = ['time']

    # Find the last non-zero entry and extend to the current date
    last_nonzero_idx = data[data['tau'] != 0].index[-1]
    last_nonzero_idx = np.argmax(data.index == last_nonzero_idx)

    # Extend the index to approximately now
    num_months = 12 * (pd.datetime.now().year - data.index[0].year) + pd.datetime.now().month
    index = pd.date_range(data.index[0].to_timestamp(), periods=num_months, freq='M').to_period(freq='M')

    # New values
    vals = np.zeros(len(index))
    vals[:last_nonzero_idx] = data['tau'].values[:last_nonzero_idx]
    vals[last_nonzero_idx:] = data['tau'].values[last_nonzero_idx]

    new_aod = pd.Series(vals, index=index, name='aod')

    return new_aod

# now make the dataframe for predictors

# linear_trends = load_independent_linear(pre_trend_end='1997-01-01', post_trend_start='2000-01-01')
linear_trends = load_independent_linear_all(pre_trend_end='1997-01-01', post_trend_start='2000-01-01')
# linear_trends = load_linear(inflection=1997)
# print('linear trend', list(linear_trends))
enso = load_enso(lag_months= 0 )
# print('enso', type(enso), list(enso))
solar = load_solar()
# print('solar', type(solar),list(solar))
QBO = load_qbo(pca = 2)
# print('QBO', list(QBO))
aod = load_giss_aod()
aod = aod['1969-01':'2018-12']
aod_nor = (aod - np.mean(aod))/np.std(aod)



ext_predictor = pd.DataFrame()

# extende solar dates
ex_dates = pd.date_range(start='2018-02', end='2018-12', freq = 'MS')

value = solar.loc['2018-01-01']['solar_mm']
values = [value] * len(ex_dates)
solar2 = pd.DataFrame(values, index= ex_dates, columns=['solar_mm'])
solar = solar.append(solar2)
solar['nor'] = (solar.solar_mm - np.mean(solar.solar_mm))/np.std(solar.solar_mm)
norsolar = solar.nor.tolist()

# predictors_uccle = linear_trends
## for one linear predictor
linear_trends_nor = (linear_trends - np.mean(linear_trends))/ np.std(linear_trends)
predictors_uccle = linear_trends_nor


predictors_uccle['enso'] = enso
predictors_uccle.loc['2018-12']['enso'] = predictors_uccle.loc['2018-11']['enso']
predictors_uccle['qboA'] = (QBO.pca - QBO.pca.mean())/QBO.pca.std()
predictors_uccle['qboB'] = (QBO.pcb - QBO.pcb.mean())/QBO.pcb.std()
predictors_uccle['solar'] = norsolar
predictors_uccle['AOD'] = aod_nor


predictors_uccle.to_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt_alltrend_nor_1969to1996.csv')

