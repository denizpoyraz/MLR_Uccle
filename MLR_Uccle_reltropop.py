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

    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')

    plt.savefig('/home/poyraden/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')
    plt.close()


######################################################################################################################

predictors = load_data('pred_baseline_ilt.csv')
#predictors = load_data('pred_baseline_pwlt.csv')

pre_name = 'Baseline_ilt'
plname = 'Trend_' + pre_name
tag = ''


predictors_with_seasons = add_seasonal_components(predictors, {'pre_const': 4, 'post_const':4, 'gap_cons':4})

#uccle = pd.read_csv('/Volumes/HD3/KMI/MLR_Uccle/Files/1km_monthlymean_reltropop_relative.csv', index_col=0)
uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_relative.csv', index_col=0)


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

trend_pre_rel = [0]*36
trend_pre_err_rel = [0]*36
trend_post_rel = [0]*36
trend_post_err_rel = [0]*36

mY = []

mean_pre = [0]*36
mean_post = [0]*36

for irt in range(24,-12,-1):
    alt[24-irt] = str(irt) + 'km' #w.r.t. tropopause
    mY.append(irt)



for i in range(36):
    uc[i] = uccle[uccle[alt[i]] > 0]

    uct_pre[i] = uc[i].loc['1977-02-01':'1996-12-01']
    uct_post[i] = uc[i].loc['2000-02-01':'2017-06-01']


    uct[i] = uc[i].loc['1977-02-01':'2017-06-01']
    #uct[i] = uc[i].loc['1985-02-01': '2017-06-01']

    predictors_with_seasons, uct[i] = pd.DataFrame.align(predictors_with_seasons, uct[i], axis=0)

    uY[i] = uct[i][alt[i]].values
    uX[i] = predictors_with_seasons.values

    print(i, len(uX[i]), len(uY[i]) )

    mean_pre[i] = np.nanmean(uct_pre[i][alt[i]].values)
    mean_post[i] = np.nanmean(uct_post[i][alt[i]].values)


    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors_with_seasons), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors_with_seasons), regression_output[i]['gls_results'].bse))

    ut[i] = uct[i].index
    ptitle = str(alt[i])
    pname = pre_name + tag + str(alt[i])
    if(i == 24): print(i, len(ut[i]), len(uY[i]), len(regression_output[i]))

    plotmlr_perkm(ut[i], uY[i], regression_output[i]['fit_values'], ptitle, pname)

    trend_pre[i] =  param_list[i]['linear_pre']
    trend_pre_err[i] =  error_list[i]['linear_pre']
    trend_post[i] =  param_list[i]['linear_post']
    trend_post_err[i] = error_list[i]['linear_post']

    trend_pre_rel[i] = param_list[i]['linear_pre'] / mean_pre[i] *100
    trend_pre_err_rel[i] = 2 * error_list[i]['linear_pre']/ mean_pre[i] *100
    trend_post_rel[i] = param_list[i]['linear_post'] / mean_pre[i] *100
    trend_post_err_rel[i] = 2 * error_list[i]['linear_post']/ mean_pre[i] *100



plt.close('all')

fig, ax = plt.subplots()
plt.title('Uccle Lotus Regression Trends')
plt.xlabel('Ozone Trend (%)')
plt.ylabel('Altitude relative to the tropopause (km)')
plt.xlim(-2,2)
ax.axvline(x=0, color='grey', linestyle='--')
ax.axhline(y=0, color='grey', linestyle=':')



ax.errorbar(trend_pre, mY, xerr= trend_pre_err, label='pre-1997', color='black', linewidth=1,
            elinewidth=0.5, capsize=1, capthick=0.5)
ax.errorbar(trend_post, mY, xerr= trend_post_err, label='post-2000', color='green', linewidth=1,
            elinewidth=0.5, capsize=1, capthick=0.5)
ax.legend(loc='upper right', frameon=True, fontsize='small')


# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')

plt.savefig('/home/poyraden/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')

plt.close()

plt.close('all')

fig, axr = plt.subplots()
plt.title('Uccle Lotus Regression Trends')
plt.xlabel('Ozone Trend (%)')
plt.ylabel('Altitude relative to the tropopause (km)')
plt.xlim(-20,20)
axr.axvline(x=0, color='grey', linestyle='--')
axr.axhline(y=0, color='grey', linestyle=':')



axr.errorbar(trend_pre_rel, mY, xerr= trend_pre_err_rel, label='pre-1997', color='black', linewidth=1,
            elinewidth=0.5, capsize=1, capthick=0.5)
axr.errorbar(trend_post_rel, mY, xerr= trend_post_err_rel, label='post-2000', color='green', linewidth=1,
            elinewidth=0.5, capsize=1, capthick=0.5)
axr.legend(loc='upper right', frameon=True, fontsize='small')

plname = plname + "_rel"
plt.savefig('/home/poyraden/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')

# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')

plt.close()