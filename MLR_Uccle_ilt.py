from typing import List, Any

from LOTUS_regression.regression import mzm_regression
from LOTUS_regression.predictors import load_data
from LOTUS_regression.predictors.seasonal import add_seasonal_components
import LOTUS_regression.tests as tests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels as sm
from datetime import datetime
from scipy import stats


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title(pltitle)
    plt.xlabel('Years')
    plt.ylabel('PO3 (hPa)')

    plt.plot(pX, pY, label='Data', color='blue')
    plt.plot(pX, pRegOutput, label='Model', color='orange')

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/MLR_Uccle/Plots/deseas_div/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/deseas_div/' + plname + '.eps')
    plt.close()


######################################################################################################################

# test for two step fitting from the LOTUS report

predictors = load_data('pred_baseline_ilt.csv')
# predictors = load_data('pred_baseline_pwlt.csv')

pre_name = 'Baseline_ilt'
plname = 'Trend_' + pre_name
tag = ''


uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_all_divided.csv')

uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
uccle['date'] =  pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

alt = [''] * 36
alt_ds = [''] * 36

# uc = pd.DataFrame()
# uct = pd.DataFrame()
uc = {}
uct = {}
ucm = {}

regression_output = [0] * 36
uX = [0] * 36
uY = [0] * 36
param_list = [0] * 36
error_list = [0] * 36
ut = [0] * 36

trend_pre = [0] * 36
trend_pre_err = [0] * 36
trend_post = [0] * 36
trend_post_err = [0] * 36

mY = []

uct_pre = {}
uct_post = {}

mean_pre = [0]*36
mean_post = [0]*36

for i in range(36):
    mY.append(i)
    alt_ds[i] = str(i) + 'km_ds'
    alt[i] = str(i) + 'km'

    uc[i] = uccle
    ucm[i] = uccle[uccle[alt[i]]>0]
    #uc[alt[i]] = uccle[alt[i]]

    uct[i] = uc[i].loc['1977-02-01':'2017-06-01']

    uct_pre[i] = ucm[i].loc['1977-02-01':'1996-12-01']
    uct_post[i] = ucm[i].loc['2000-02-01':'2017-06-01']

    predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)

    uY[i] = uct[i][alt_ds[i]].values
    mean_pre[i] = np.nanmean(uct_pre[i][alt[i]].values)
    mean_post[i] = np.nanmean(uct_post[i][alt[i]].values)

    #print('pre', mean_pre[i], 'post', mean_post[i])

    uX[i] = predictors.values

    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))

    ut[i] = uct[i].index
    ptitle = str(alt[i])
    pname = pre_name + tag + str(alt[i])

    if (i == 24): print(i, len(ut[i]), len(uY[i]), len(regression_output[i]))

    plotmlr_perkm(ut[i], uY[i], regression_output[i]['fit_values'], ptitle, pname)

    trend_pre[i] = param_list[i]['linear_pre']
    trend_pre_err[i] = error_list[i]['linear_pre']
    trend_post[i] = param_list[i]['linear_post']
    trend_post_err[i] = error_list[i]['linear_post']

    print('pre', trend_pre[i], 'post', trend_post[i])


    # for % in decade

    trend_pre[i] = trend_pre[i] * 10 / mean_pre[i] *100
    trend_pre_err[i] = 2 * trend_pre_err[i] * 10 / mean_pre[i] * 100
    trend_post[i] = trend_post[i] * 10 / mean_post[i] *100
    trend_post_err[i] = 2 * trend_post_err[i] * 10 / mean_post[i] * 100

    # trend_pre[i] = trend_pre[i] * 100 / (mean_pre[i] * 10)
    # trend_pre_err[i] = 2 * trend_pre_err[i] * 100 / (mean_pre[i] * 10)
    # trend_post[i] = trend_post[i] * 100 / (mean_post[i] * 10)
    # trend_post_err[i] = 2 * trend_post_err[i] * 100 / (mean_post[i] * 10)

plt.close('all')

fig, ax = plt.subplots()
plt.title('Uccle Lotus Regression Trends')
plt.xlabel('Ozone Trend (%)')
plt.ylabel('Altitude (km)')
plt.xlim(-20, 20)
ax.axvline(x=0, color='grey', linestyle='--')

ax.errorbar(trend_pre, mY, xerr=trend_pre_err, label='pre-1997', color='black', linewidth=1,
            elinewidth=0.5, capsize=1, capthick=0.5)
ax.errorbar(trend_post, mY, xerr=trend_post_err, label='post-2000', color='green', linewidth=1,
            elinewidth=0.5, capsize=1, capthick=0.5)
ax.legend(loc='upper right', frameon=True, fontsize='small')

plname = plname + "_decade3"

plt.savefig('/home/poyraden/MLR_Uccle/Plots/deseas_div/' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/deseas_div/' + plname + '.eps')
plt.close()
