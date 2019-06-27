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

    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.pdf')
    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/ilt_reltropop/' + plname + '.eps')

    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/' + plname + '.eps')
    plt.close()


######################################################################################################################

# predictors = load_data('pred_baseline_ilt.csv')
# #predictors = load_data('pred_baseline_pwlt.csv')
# pre_name = 'Baseline_ilt'
# plname = 'Trend_' + pre_name
# tag = ''

# part for using extended predictors
pre_name = 'NewPredictors'
plname = 'Trend_' + pre_name
tag = ''

# predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/Extended_ilt.csv')
# predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
# predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
# predictors.set_index('date', inplace=True)
#
#
# #uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_relative.csv', index_col=0)
# uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_deas_relative.csv')
#
# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
# uccle['date'] =  pd.to_datetime(uccle['date'], format='%Y-%m')
# uccle.set_index('date', inplace=True)

# try new predictors

predictors= pd.read_csv('/home/poyraden/MLR_Uccle/Files/NewPredictors_ilt.csv')

setp = set(predictors['Unnamed: 0'].tolist())


predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m-%d')
predictors.set_index('date', inplace=True)

print('predictors', predictors[0:3])
print('predictors test' , predictors.loc['1972-02-01'])

# For DeBilt
# predictors = predictors.loc['1992-11-01':'2018-12-01']


uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_deas_relative.csv')
# uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean_deseas.csv')

print('uccle', len(uccle), list(uccle), uccle.index)
setu = set(uccle.date.tolist())

# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
# pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

print('predictors', len(predictors), list(predictors))

# remove uccle missing dates:

print('setp.difference(setu)', setp.difference(setu))
print('setu.difference(setp)', setu.difference(setp))

removep = list(setp.difference(setu))
removeu = list(setu.difference(setp))

# difup = setp.symmetric_difference(setu)
# print('difup',difup)
# diup = list(difup)
uccle = uccle.drop(removeu)
print('after uccle', len(uccle))

for j in range(len(removep)):
    removep[j] = datetime.strptime(removep[j], '%Y-%m-%d')


predictors = predictors.drop(removep)
print('after pre', len(predictors))



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
    alt[24-irt] = str(irt) + 'km_ds' #w.r.t. tropopause
    mY.append(irt)



for i in range(36):
    uc[i] = uccle

    # uct_pre[i] = uc[i].loc['1977-02-01':'1996-12-01']
    # uct_post[i] = uc[i].loc['2000-02-01':'2017-06-01']


    #uct[i] = uc[i].loc['1977-02-01':'2017-06-01']
    uct[i] = uc[i]

    predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)

    uY[i] = uct[i][alt[i]].values
    uX[i] = predictors.values

    # print(i, len(uX[i]), len(uY[i]) )

    # mean_pre[i] = np.nanmean(uct_pre[i][alt[i]].values)
    # mean_post[i] = np.nanmean(uct_post[i][alt[i]].values)


    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))

    ut[i] = uct[i].index

    ptitle = str(alt[i])
    pname = pre_name + tag + str(alt[i])
    if(i == 24): print(i, len(ut[i]), len(uY[i]), len(regression_output[i]))

    #plotmlr_perkm(ut[i], uY[i], regression_output[i]['fit_values'], ptitle, pname)

    # trend_pre[i] =  param_list[i]['linear_pre']
    # trend_pre_err[i] =  error_list[i]['linear_pre']
    # trend_post[i] =  param_list[i]['linear_post']
    # trend_post_err[i] = error_list[i]['linear_post']

    trend_pre_rel[i] = param_list[i]['linear_pre'] *100
    trend_pre_err_rel[i] = 2 * error_list[i]['linear_pre'] *100
    trend_post_rel[i] = param_list[i]['linear_post'] *100
    trend_post_err_rel[i] = 2 * error_list[i]['linear_post'] *100



# plt.close('all')
#
# fig, ax = plt.subplots()
# plt.title('Uccle Lotus Regression Trends')
# plt.xlabel('Ozone Trend (%)')
# plt.ylabel('Altitude relative to the tropopause (km)')
# plt.xlim(-2,2)
# ax.axvline(x=0, color='grey', linestyle='--')
# ax.axhline(y=0, color='grey', linestyle=':')
#
#
#
# ax.errorbar(trend_pre, mY, xerr= trend_pre_err, label='pre-1997', color='black', linewidth=1,
#             elinewidth=0.5, capsize=1, capthick=0.5)
# ax.errorbar(trend_post, mY, xerr= trend_post_err, label='post-2000', color='green', linewidth=1,
#             elinewidth=0.5, capsize=1, capthick=0.5)
# ax.legend(loc='upper right', frameon=True, fontsize='small')
#
#
# # plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_Deseas_RelTropop_Extended/' + plname + '.pdf')
# # plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_Deseas_RelTropop_Extended/' + plname + '.eps')
#
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_Deseas_RelTropop_Extended/' + plname + '.pdf')
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_Deseas_RelTropop_Extended/' + plname + '.eps')
#
# plt.close()

plt.close('all')

fig, axr = plt.subplots()
plt.title('Uccle 1969-2018')
plt.xlabel('Ozone Trend [%/dec]')
plt.ylabel('Altitude relative to the tropopause [km]')
plt.xlim(-10,10)
axr.axvline(x=0, color='grey', linestyle='--')
axr.axhline(y=0, color='grey', linestyle=':')

axr.tick_params(axis='both', which='both', direction='in')
axr.yaxis.set_ticks_position('both')
axr.xaxis.set_ticks_position('both')
axr.yaxis.set_minor_locator(AutoMinorLocator(5))
axr.xaxis.set_minor_locator(AutoMinorLocator(5))
axr.set_xticks([-10,-5,0,5,10])



eb1 = axr.errorbar(trend_pre_rel, mY, xerr= trend_pre_err_rel, label='pre-1997', color='red', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')

eb2 = axr.errorbar(trend_post_rel, mY, xerr= trend_post_err_rel, label='post-2000', color='limegreen', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')

axr.legend(loc='upper right', frameon=True, fontsize='small')

plname = plname + "_rel"
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/RelTropop_' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/RelTropop_' + plname + '.eps')

# plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_Deseas_RelTropop_Extended/' + plname + '.pdf')
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_Deseas_RelTropop_Extended/' + plname + '.eps')

plt.close()