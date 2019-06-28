from typing import List, Any

from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


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
pre_name = 'NewPredictors_Stratosphere'
plname = 'Trend_' + pre_name
tag = ''
# predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/Extended_ilt.csv')

# try new predictors
predictors= pd.read_csv('/home/poyraden/MLR_Uccle/Files/NewPredictors_ilt.csv')

setp = set(predictors['Unnamed: 0'].tolist())

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)


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

alt = [''] * 24
alt_ds = [''] * 24

uc = {}
uct = {}
ucm = {}

mY = []
ut = [0] * 24

predictorsilt = predictors.drop(columns=['pre_tropop', 'temp_sur', 'AO', 'NOI', "EA", 'AOD'])
predictorsAO = predictors.drop(columns=['pre_tropop', 'temp_sur', 'NOI', "EA", 'AOD'])
predictorsEA = predictors.drop(columns=['pre_tropop', 'temp_sur','NOI', 'AOD'])
predictorsAOD = predictors.drop(columns=['pre_tropop', 'temp_sur', 'NOI'])
predictorspretropop = predictors.drop(columns=['temp_sur','NOI'])


#predictorstemp_sur = predictors.drop(columns=[ 'AO', 'NOI', "EA", 'AOD'])

#effect of temp surface is on the full predictor predictors

regression_outputilt = [0] * 24
uXilt = [0] * 24
uYilt = [0] * 24
param_listilt = [0] * 24
error_listilt = [0] * 24
trend_preilt = [0] * 24
trend_pre_errilt = [0] * 24
trend_postilt = [0] * 24
trend_post_errilt = [0] * 24
##
regression_outputpretropop = [0] * 24
uXpretropop = [0] * 24
uYpretropop = [0] * 24
param_listpretropop = [0] * 24
error_listpretropop = [0] * 24
trend_prepretropop = [0] * 24
trend_pre_errpretropop = [0] * 24
trend_postpretropop = [0] * 24
trend_post_errpretropop = [0] * 24
##
regression_outputAOD = [0] * 24
uXAOD = [0] * 24
uYAOD = [0] * 24
param_listAOD = [0] * 24
error_listAOD = [0] * 24
trend_preAOD = [0] * 24
trend_pre_errAOD = [0] * 24
trend_postAOD = [0] * 24
trend_post_errAOD = [0] * 24
##
regression_outputAO = [0] * 24
uXAO = [0] * 24
uYAO = [0] * 24
param_listAO = [0] * 24
error_listAO = [0] * 24
trend_preAO = [0] * 24
trend_pre_errAO = [0] * 24
trend_postAO = [0] * 24
trend_post_errAO = [0] * 24
##
regression_outputEA = [0] * 24
uXEA = [0] * 24
uYEA = [0] * 24
param_listEA = [0] * 24
error_listEA = [0] * 24
trend_preEA = [0] * 24
trend_pre_errEA = [0] * 24
trend_postEA = [0] * 24
trend_post_errEA = [0] * 24


for i in range(12, 36,1):
    akm = i
    i = i-12
    mY.append(akm)
    alt_ds[i] = str(akm) + 'km_ds'
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

    ## AO
    predictorsAO, uct[i] = pd.DataFrame.align(predictorsAO, uct[i], axis=0)
    uYAO[i] = uct[i][alt_ds[i]].values
    uXAO[i] = predictorsAO.values
    regression_outputAO[i] = mzm_regression(uXAO[i], uYAO[i])
    param_listAO[i] = dict(zip(list(predictorsAO), regression_outputAO[i]['gls_results'].params))
    error_listAO[i] = dict(zip(list(predictorsAO), regression_outputAO[i]['gls_results'].bse))
    trend_preAO[i] = param_listAO[i]['linear_pre']
    trend_pre_errAO[i] = error_listAO[i]['linear_pre']
    trend_postAO[i] = param_listAO[i]['linear_post']
    trend_post_errAO[i] = error_listAO[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_preAO[i] = trend_preAO[i] * 100
    trend_pre_errAO[i] = 2 * trend_pre_errAO[i] * 100
    trend_postAO[i] = trend_postAO[i] * 100
    trend_post_errAO[i] = 2 * trend_post_errAO[i] * 100

    ## EA
    predictorsEA, uct[i] = pd.DataFrame.align(predictorsEA, uct[i], axis=0)
    uYEA[i] = uct[i][alt_ds[i]].values
    uXEA[i] = predictorsEA.values
    regression_outputEA[i] = mzm_regression(uXEA[i], uYEA[i])
    param_listEA[i] = dict(zip(list(predictorsEA), regression_outputEA[i]['gls_results'].params))
    error_listEA[i] = dict(zip(list(predictorsEA), regression_outputEA[i]['gls_results'].bse))
    trend_preEA[i] = param_listEA[i]['linear_pre']
    trend_pre_errEA[i] = error_listEA[i]['linear_pre']
    trend_postEA[i] = param_listEA[i]['linear_post']
    trend_post_errEA[i] = error_listEA[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_preEA[i] = trend_preEA[i] * 100
    trend_pre_errEA[i] = 2 * trend_pre_errEA[i] * 100
    trend_postEA[i] = trend_postEA[i] * 100
    trend_post_errEA[i] = 2 * trend_post_errEA[i] * 100

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
    predictorspretropop, uct[i] = pd.DataFrame.align(predictorspretropop, uct[i], axis=0)
    uYpretropop[i] = uct[i][alt_ds[i]].values
    uXpretropop[i] = predictorspretropop.values
    regression_outputpretropop[i] = mzm_regression(uXpretropop[i], uYpretropop[i])
    param_listpretropop[i] = dict(zip(list(predictorspretropop), regression_outputpretropop[i]['gls_results'].params))
    error_listpretropop[i] = dict(zip(list(predictorspretropop), regression_outputpretropop[i]['gls_results'].bse))
    trend_prepretropop[i] = param_listpretropop[i]['linear_pre']
    trend_pre_errpretropop[i] = error_listpretropop[i]['linear_pre']
    trend_postpretropop[i] = param_listpretropop[i]['linear_post']
    trend_post_errpretropop[i] = error_listpretropop[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_prepretropop[i] = trend_prepretropop[i] * 100
    trend_pre_errpretropop[i] = 2 * trend_pre_errpretropop[i] * 100
    trend_postpretropop[i] = trend_postpretropop[i] * 100
    trend_post_errpretropop[i] = 2 * trend_post_errpretropop[i] * 100



plt.close('all')

fig, ax = plt.subplots()
plt.title('Uccle 1969-2018')
plt.xlabel('Ozone trend [%/dec]')
plt.ylabel('Altitude [km]')
plt.xlim(-12, 15)
plt.ylim(12,32)
ax.axvline(x=0, color='grey', linestyle='--')

ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_xticks([ -10, -5,0,5,10, 15])
ax.set_yticks([ 12, 15,20,25,30])


plt.plot(trend_preilt, mY, label='pre ilt', color='gold')
plt.plot(trend_preAO, mY, label='pre AO', color='darkorange')
plt.plot(trend_preEA, mY, label='pre EA', color='indianred')
plt.plot(trend_preAOD, mY, label='pre AOD', color='purple')

eb1 = ax.errorbar(trend_prepretropop, mY, xerr=trend_post_errpretropop, label='pre pressure tropop (all)', color='red', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')

#plt.plot(trend_preAOD, mY, label='pre AOD', color='gold')



plt.plot(trend_postilt, mY, label='post ilt', color='limegreen')
plt.plot(trend_postAO, mY, label='post AO', color='olive')
plt.plot(trend_postEA, mY, label='post EA', color='royalblue')
plt.plot(trend_postAOD, mY, label='post AOD', color='blue')

eb2 = ax.errorbar(trend_postpretropop, mY, xerr=trend_post_errpretropop, label='post pressure tropop (all)', color='black', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')

#plt.plot(trend_postAOD, mY, label='post AOD', color='green')

ax.legend(loc='upper right', frameon=True, fontsize='small')


plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle_' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle_' + plname + '.eps')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.show()
plt.close()
