from typing import List, Any

from LOTUS_regression.regression import mzm_regression
from matplotlib.ticker import AutoMinorLocator

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

    plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Residuals/' + plname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Residuals/' + plname + '.eps')
    plt.close()


######################################################################################################################
# part for using extended predictors
pre_name = 'OneLinear_All_RelTrop'
plname = 'Trend_' + pre_name
tag = ''

# predictors = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt.csv')
predictors = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt_alltrend_nor.csv')
# #
predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)
predictors_pre = predictors.loc['1969-01-01':'1996-12-01']
predictors_post = predictors.loc['1997-01-01':'2018-12-01']

uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean_reltropop_deseas.csv')
# uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/DeBilt_1km_monthlymean_deseas.csv')

print('uccle', len(uccle), list(uccle), uccle.index)
setu = set(uccle.date.tolist())

uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)
uccle_pre = uccle.loc['1969-01-01':'1996-12-01']
uccle_post = uccle.loc['1997-01-01':'2018-12-01']

print('predictors', len(predictors), list(predictors))

alt = [''] * 36
uc = {}
uct = {}
uct_pre = {}
uct_post = {}

regression_output = [0] * 36
uX = [0] * 36
uY = [0] * 36
param_list = [0] * 36
error_list = [0] * 36
ut = [0]*36

trend_pre = [0]*36
trend_pre_err = [0]*36
trend_post = [0]*36
trend_post_err = [0]*36
trend_all = [0]*36
trend_all_err = [0]*36

mY = []

mean_pre = [0]*36
mean_post = [0]*36

for irt in range(24,-12,-1):
    alt[24-irt] = str(irt) + 'km_ds' #w.r.t. tropopause
    mY.append(irt)

print('MY', len(mY), mY)


# for i in range(36):
for i in range(24, -12, -1):

    print(i, mY[i], alt[i])

    uct[i] = uccle
    predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)
    uY[i] = uct[i][alt[i]].values
    uX[i] = predictors.values
    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))
    ut[i] = uct[i].index
    trend_all[i] = param_list[i]['linear_one'] *100
    trend_all_err[i] = 2 * error_list[i]['linear_one'] *100

 #    ## now for 1969-1997
 #    uct[i] = uccle_pre
 #    predictors_pre, uct[i] = pd.DataFrame.align(predictors_pre, uct[i], axis=0)
 #    uY[i] = uct[i][alt[i]].values
 #    uX[i] = predictors_pre.values
 #    regression_output[i] = mzm_regression(uX[i], uY[i])
 #    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
 #    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))
 #    ut[i] = uct[i].index
 #    trend_pre[i] = param_list[i]['linear_one'] * 100
 #    trend_pre_err[i] = 2 * error_list[i]['linear_one'] * 100
 #
 # ## now for 1997-2018
 #    uct[i] = uccle_post
 #    predictors_post, uct[i] = pd.DataFrame.align(predictors_post, uct[i], axis=0)
 #    uY[i] = uct[i][alt[i]].values
 #    uX[i] = predictors_post.values
 #    regression_output[i] = mzm_regression(uX[i], uY[i])
 #    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
 #    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))
 #    ut[i] = uct[i].index
 #    trend_post[i] = param_list[i]['linear_one'] * 100
 #    trend_post_err[i] = 2 * error_list[i]['linear_one'] * 100
 #


print('paramlist', param_list)
print('errorlist', error_list)

plt.close('all')

fig, axr = plt.subplots()
plt.title('Uccle 1969-2018')
plt.xlabel('Ozone Trend [%/dec]')
plt.ylabel('Altitude relative to the tropopause [km]')
plt.xlim(-10,10)
plt.ylim(-12,25)

axr.axvline(x=0, color='grey', linestyle='--')
axr.axhline(y=0, color='grey', linestyle=':')

axr.tick_params(axis='both', which='both', direction='in')
axr.yaxis.set_ticks_position('both')
axr.xaxis.set_ticks_position('both')
axr.yaxis.set_minor_locator(AutoMinorLocator(5))
axr.xaxis.set_minor_locator(AutoMinorLocator(5))
axr.set_xticks([-10,-5,0,5,10])

eb1 = axr.errorbar(trend_all, mY, xerr= trend_all_err, label='1969-2018', color='black', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')


axr.legend(loc='upper right', frameon=True, fontsize='small')

plname = plname
plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Uccle_' + plname + '.pdf')
plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Uccle_' + plname + '.eps')

plt.show()
plt.close()