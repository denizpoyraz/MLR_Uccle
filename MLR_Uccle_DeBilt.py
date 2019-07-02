from typing import List, Any

from LOTUS_regression.regression import mzm_regression
from matplotlib.ticker import AutoMinorLocator
from LOTUS_regression.predictors import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title(pltitle)
    plt.xlabel('Years')
    plt.ylabel('PO3 (hPa)')

    plt.plot(pX, pY, label='Data', color='blue')
    plt.plot(pX, pRegOutput, label='Model', color='orange')

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/home/poyraden/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.eps')
    plt.close()
    plt.close()


######################################################################################################################

# these are pwlt predictors from 1977
# predictors = load_data('pred_baseline_ilt.csv')
# pre_name = 'Baseline_pwlt'
# plname = 'Trend_' + pre_name
# tag = ''

# part for using extended predictors
pre_name = 'Abs'
plname = 'Trend_' + pre_name
tag = ''
predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/Extended_ilt.csv')

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)

# For DeBilt
predictors = predictors.loc['2000-01-01':'2018-12-01']

uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_deas_relative.csv')
# uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_deas_relative.csv')
#
uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)
uccle = uccle.loc['2000-01-01':'2018-12-01']

# debilt = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean_reltropop_deas.csv')
debilt = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean_deseas.csv')

debilt.rename(columns={'Unnamed: 0':'date'}, inplace=True)
pd.to_datetime(debilt['date'], format='%Y-%m')
debilt.set_index('date', inplace=True)
debilt = debilt.loc['2000-01-01':'2018-12-01']

print(debilt.index)
print(list(uccle))

alt = [''] * 36

# uc = pd.DataFrame()
# uct = pd.DataFrame()
ud = {}
udt = {}
udm = {}

regression_output = [0] * 36
uX = [0] * 36
uY = [0] * 36
param_list = [0] * 36
error_list = [0] * 36
utd = [0] * 36

trend_post = [0] * 36
trend_post_err = [0] * 36

#uccle
uc = {}
uct = {}
ucm = {}

regression_outputu= [0] * 36
uXu = [0] * 36
uYu = [0] * 36
param_listu = [0] * 36
error_listu = [0] * 36
utc = [0] * 36

trend_postu = [0] * 36
trend_post_erru = [0] * 36

mY = []


# for irt in range(24,-12,-1):
#     alt[24-irt] = str(irt) + 'km_ds' #w.r.t. tropopause
#     print(irt, alt[24-irt])
#     mY.append(irt)


for i in range(36):
    mY.append(i)
    alt[i] = str(i) + 'km_ds'

    #debilt
    udt[i] = debilt
    #.loc['2000-01-01':'2018-12-01']

    predictors, udt[i] = pd.DataFrame.align(predictors, udt[i], axis=0)

    uY[i] = udt[i][alt[i]].values
    uX[i] = predictors.values

    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    print('one', param_list[i])

    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))

    utd[i] = udt[i].index
    ptitle = str(alt[i])
    pname = 'DeBilt_' + pre_name + tag + str(alt[i])
    #plotmlr_perkm(udt[i], uY[i], regression_output[i]['fit_values'], ptitle, pname)

    trend_post[i] = param_list[i]['linear_post']
    trend_post_err[i] = error_list[i]['linear_post']


    # for % in decade for relative montly anamoly
    trend_post[i] = trend_post[i] * 100
    trend_post_err[i] = 2 * trend_post_err[i] * 100

    #uccle
    uct[i] = uccle
    #.loc['2000-01-01':'2018-12-01']

    predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)

    uYu[i] = uct[i][alt[i]].values
    uXu[i] = predictors.values

    regression_outputu[i] = mzm_regression(uXu[i], uYu[i])
    param_listu[i] = dict(zip(list(predictors), regression_outputu[i]['gls_results'].params))
    error_listu[i] = dict(zip(list(predictors), regression_outputu[i]['gls_results'].bse))

    utc[i] = uct[i].index
    ptitle = str(alt[i])
    pname = 'Uccle_' + pre_name + tag + str(alt[i])
    #plotmlr_perkm(uct[i], uYu[i], regression_outputu[i]['fit_values'], ptitle, pname)

    trend_postu[i] = param_listu[i]['linear_post']
    trend_post_erru[i] = error_listu[i]['linear_post']

    # for % in decade for relative montly anamoly
    trend_postu[i] = trend_postu[i] * 100
    trend_post_erru[i] = 2 * trend_post_erru[i] * 100

# for monthly anamoly
    # trend_post[i] = trend_post[i] * 100 / (mean_post[i] * 10)
    # trend_post_err[i] = 2 * trend_post_err[i] * 100 / (mean_post[i] * 10)
    # trend_post[i] = trend_post[i] * 100 / (mean_post[i] * 10)
    # trend_post_err[i] = 2 * trend_post_err[i] * 100 / (mean_post[i] * 10)
print('debilt', trend_post)
print('uccle', trend_postu)

plt.close('all')

fig, ax = plt.subplots()
plt.title('')
plt.xlabel('Ozone Trend (%/dec)')
plt.ylabel('Altitude [km]')
# plt.ylabel('Altitude relative to the tropopause [km]')

plt.xlim(-10, 12)
# plt.ylim(-10,23)

plt.ylim(0, 33)

ax.axvline(x=0, color='grey', linestyle='--')
# ax.axhline(y=0, color='grey', linestyle=':')

ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_xticks([-10,-5,0,5,10])


eb1 = ax.errorbar(trend_postu, mY, xerr=trend_post_erru, label='Uccle 2000-2018', color='limegreen', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')
eb2 = ax.errorbar(trend_post, mY, xerr=trend_post_err, label='DeBilt 2000-2018', color='blue', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')

ax.legend(loc='lower left', frameon=True, fontsize='small')


plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.eps')
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.close()
