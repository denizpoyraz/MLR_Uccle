from typing import List, Any

from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import statsmodels as sm
from datetime import datetime
from scipy import stats
from Extend_Predictors import load_enso, load_independent_linear, load_qbo, load_solar


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title(pltitle)
    plt.xlabel('Years')
    plt.ylabel('PO3 (hPa)')

    plt.plot(pX, pY, label='Data', color='blue')
    plt.plot(pX, pRegOutput, label='Model', color='orange')

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/' + plname + '.eps')
    plt.close()
    plt.close()


######################################################################################################################

# these are pwlt predictors from 1977
# predictors = load_data('pred_baseline_ilt.csv')
# pre_name = 'Baseline_pwlt'
# plname = 'Trend_' + pre_name
# tag = ''

# part for using extended predictors
pre_name = 'NewPredictors_Step_Trop'
plname = 'Trend_' + pre_name
tag = ''
# predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/Extended_ilt.csv')

# try new predictors
predictors= pd.read_csv('/home/poyraden/MLR_Uccle/Files/NewPredictors_ilt.csv')

setp = set(predictors['Unnamed: 0'].tolist())

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)

# For DeBilt
# predictors = predictors.loc['1992-11-01':'2018-12-01']


uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_all_relative.csv')
# uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean_deseas.csv')

#dates = pd.date_range(start='1992-11', end='2018-12', freq = 'MS')
setu = set(uccle.date.tolist())

# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
# pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

# remove uccle missing dates:
difup = setp.symmetric_difference(setu)
diup = list(difup)
uccle = uccle.drop(diup)

alt = [''] * 12
alt_ds = [''] * 12

uc = {}
uct = {}
ucm = {}

mY = []
ut = [0] * 12

predictorsilt = predictors.drop(columns=['pre_tropop', 'temp_sur', 'AO', 'NOI', "EA", 'AOD'])
predictorsAOD = predictors.drop(columns=['pre_tropop', 'temp_sur', 'NOI', "EA", 'AO'])
predictorsNOI = predictors.drop(columns=['pre_tropop', 'temp_sur', "EA", 'AO'])
predictorstropop = predictors.drop(columns=['pre_tropop', "EA", 'AO'])

regression_outputilt = [0] * 12
uXilt = [0] * 12
uYilt = [0] * 12
param_listilt = [0] * 12
error_listilt = [0] * 12
trend_preilt = [0] * 12
trend_pre_errilt = [0] * 12
trend_postilt = [0] * 12
trend_post_errilt = [0] * 12
##
regression_outputtropop = [0] * 12
uXtropop = [0] * 12
uYtropop = [0] * 12
param_listtropop = [0] * 12
error_listtropop = [0] * 12
trend_pretropop = [0] * 12
trend_pre_errtropop = [0] * 12
trend_posttropop = [0] * 12
trend_post_errtropop = [0] * 12
##
regression_outputAOD = [0] * 12
uXAOD = [0] * 12
uYAOD = [0] * 12
param_listAOD = [0] * 12
error_listAOD = [0] * 12
trend_preAOD = [0] * 12
trend_pre_errAOD = [0] * 12
trend_postAOD = [0] * 12
trend_post_errAOD = [0] * 12

##
regression_outputNOI = [0] * 12
uXNOI = [0] * 12
uYNOI = [0] * 12
param_listNOI = [0] * 12
error_listNOI = [0] * 12
trend_preNOI = [0] * 12
trend_pre_errNOI = [0] * 12
trend_postNOI = [0] * 12
trend_post_errNOI = [0] * 12
##



for i in range(12):
    mY.append(i)
    alt_ds[i] = str(i) + 'km_ds'
    alt[i] = str(i) + 'km'
    uc[i] = uccle
    uct[i] = uc[i]

    ## ilt
    predictorsilt, uct[i] = pd.DataFrame.align(predictorsilt, uct[i], axis=0)
    uYilt[i] = uct[i][alt_ds[i]].values
    uXilt[i] = predictorsilt.values
    regression_outputilt[i] = mzm_regression(uXilt[i], uYilt[i])
    param_listilt[i] = dict(zip(list(predictorsilt), regression_outputilt[i]['gls_results'].params))
    error_listilt[i] = dict(zip(list(predictorsilt), regression_outputilt[i]['gls_results'].bse))
    trend_preilt[i] = param_listilt[i]['linear_pre']
    trend_pre_errilt[i] = error_listilt[i]['linear_pre']
    trend_postilt[i] = param_listilt[i]['linear_post']
    trend_post_errilt[i] = error_listilt[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_preilt[i] = trend_preilt[i] * 100
    trend_pre_errilt[i] = 2 * trend_pre_errilt[i] * 100
    trend_postilt[i] = trend_postilt[i] * 100
    trend_post_errilt[i] = 2 * trend_post_errilt[i] * 100



    ##  NOI
    predictorsNOI, uct[i] = pd.DataFrame.align(predictorsNOI, uct[i], axis=0)
    uYNOI[i] = uct[i][alt_ds[i]].values
    uXNOI[i] = predictorsNOI.values
    regression_outputNOI[i] = mzm_regression(uXNOI[i], uYNOI[i])
    param_listNOI[i] = dict(zip(list(predictorsNOI), regression_outputNOI[i]['gls_results'].params))
    error_listNOI[i] = dict(zip(list(predictorsNOI), regression_outputNOI[i]['gls_results'].bse))
    trend_preNOI[i] = param_listNOI[i]['linear_pre']
    trend_pre_errNOI[i] = error_listNOI[i]['linear_pre']
    trend_postNOI[i] = param_listNOI[i]['linear_post']
    trend_post_errNOI[i] = error_listNOI[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_preNOI[i] = trend_preNOI[i] * 100
    trend_pre_errNOI[i] = 2 * trend_pre_errNOI[i] * 100
    trend_postNOI[i] = trend_postNOI[i] * 100
    trend_post_errNOI[i] = 2 * trend_post_errNOI[i] * 100


    ## AOD
    predictorsAOD, uct[i] = pd.DataFrame.align(predictorsAOD, uct[i], axis=0)
    uYAOD[i] = uct[i][alt_ds[i]].values
    uXAOD[i] = predictorsAOD.values
    regression_outputAOD[i] = mzm_regression(uXAOD[i], uYAOD[i])
    param_listAOD[i] = dict(zip(list(predictorsAOD), regression_outputAOD[i]['gls_results'].params))
    error_listAOD[i] = dict(zip(list(predictorsAOD), regression_outputAOD[i]['gls_results'].bse))
    trend_preAOD[i] = param_listAOD[i]['linear_pre']
    trend_pre_errAOD[i] = error_listAOD[i]['linear_pre']
    trend_postAOD[i] = param_listAOD[i]['linear_post']
    trend_post_errAOD[i] = error_listAOD[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_preAOD[i] = trend_preAOD[i] * 100
    trend_pre_errAOD[i] = 2 * trend_pre_errAOD[i] * 100
    trend_postAOD[i] = trend_postAOD[i] * 100
    trend_post_errAOD[i] = 2 * trend_post_errAOD[i] * 100



    ## pressure tropopause
    predictorstropop, uct[i] = pd.DataFrame.align(predictorstropop, uct[i], axis=0)
    uYtropop[i] = uct[i][alt_ds[i]].values
    uXtropop[i] = predictorstropop.values
    regression_outputtropop[i] = mzm_regression(uXtropop[i], uYtropop[i])
    param_listtropop[i] = dict(zip(list(predictorstropop), regression_outputtropop[i]['gls_results'].params))
    error_listtropop[i] = dict(zip(list(predictorstropop), regression_outputtropop[i]['gls_results'].bse))
    trend_pretropop[i] = param_listtropop[i]['linear_pre']
    trend_pre_errtropop[i] = error_listtropop[i]['linear_pre']
    trend_posttropop[i] = param_listtropop[i]['linear_post']
    trend_post_errtropop[i] = error_listtropop[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_pretropop[i] = trend_pretropop[i] * 100
    trend_pre_errtropop[i] = 2 * trend_pre_errtropop[i] * 100
    trend_posttropop[i] = trend_posttropop[i] * 100
    trend_post_errtropop[i] = 2 * trend_post_errtropop[i] * 100


    # ###
    # ut[i] = uct[i].index
    # ptitle = str(alt[i])
    # pname = pre_name + tag + str(alt[i])
    #
    # # plotmlr_perkm(ut[i], uY[i], regression_output[i]['fit_values'], ptitle, pname)


plt.close('all')

fig, ax = plt.subplots()
plt.title('Uccle 1969-2018')
plt.xlabel('Ozone trend [%/dec]')
plt.ylabel('Altitude [km]')
plt.xlim(-5, 10)
plt.ylim(0,12)
ax.axvline(x=0, color='grey', linestyle='--')

ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_xticks([-5,0,5,10])



plt.plot(trend_preilt, mY, label='pre ilt', color='gold')
plt.plot(trend_preAOD, mY, label='pre AOD', color='purple')
plt.plot(trend_preNOI, mY, label='pre NOI', color='salmon')

#plt.plot(trend_pretropop, mY, label='pre pressure tropop', color='magenta')


eb1 = ax.errorbar(trend_pretropop, mY, xerr=trend_pre_errtropop, label='pre all', color='red', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')

#plt.plot(trend_preAOD, mY, label='pre AOD', color='gold')



plt.plot(trend_postilt, mY, label='post ilt', color='limegreen')
plt.plot(trend_postAOD, mY, label='post AOD', color='blue')

plt.plot(trend_postNOI, mY, label='post NOI', color='dodgerblue')
#plt.plot(trend_posttropop, mY, label='post pressure tropop', color='cyan')



eb2 = ax.errorbar(trend_posttropop, mY, xerr=trend_post_errtropop, label='post all', color='black', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')

#plt.plot(trend_postAOD, mY, label='post AOD', color='green')

ax.legend(loc='lower left', frameon=True, fontsize='small')


plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Step_Only_Tro' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Step_Only_Tro' + plname + '.eps')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.show()
plt.close()
