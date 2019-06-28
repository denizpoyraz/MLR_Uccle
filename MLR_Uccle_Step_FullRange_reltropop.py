from typing import List, Any

from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from datetime import datetime



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


## IMPORTANT, change the boolean if you want to make the standard predictors or the one for
## total column

totalcolumn = True

# part for using extended predictors
if totalcolumn: pre_name = 'TotalColumn_'
else: pre_name = "All_"
plname = 'Trend_' + pre_name
tag = ''
# predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/Extended_ilt.csv')

# try new predictors
if totalcolumn:
    predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/TotalColumnPredictors_ilt.csv')
else:
    predictors= pd.read_csv('/home/poyraden/MLR_Uccle/Files/NewPredictors_ilt.csv')

setp = set(predictors['Unnamed: 0'].tolist())

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)


uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_deseas.csv')
# uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/DeBilt_1km_monthlymean_deseas.csv')

#dates = pd.date_range(start='1992-11', end='2018-12', freq = 'MS')
setu = set(uccle.date.tolist())

# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
# pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

# remove  missing dates:
removep = list(setp.difference(setu))
removeu = list(setu.difference(setp))
uccle = uccle.drop(removeu)
print('after uccle', len(uccle))

for j in range(len(removep)):
    removep[j] = datetime.strptime(removep[j], '%Y-%m-%d')
predictors = predictors.drop(removep)
print('after pre', len(predictors))

alt = [''] * 36
alt_ds = [''] * 36

uc = {}
uct = {}
ucm = {}

mY = []
ut = [0] * 36



if totalcolumn:
    predictorsilt = predictors.drop(columns=['EAWR','NAO', 'AOD', 'AO','EESC','temp_100'])
    predictorsEA = predictors.drop(columns=['NAO', 'AOD', 'AO','EESC','temp_100'])
    predictorsNOI = predictors.drop(columns= ['AOD', 'AO','EESC','temp_100'])
    predictorsAOD = predictors.drop(columns=['AO','EESC','temp_100'])
    predictorsAO = predictors.drop(columns=['EESC','temp_100'])
    predictorsEESC = predictors.drop(columns=['temp_100'])

else:
    predictorsilt = predictors.drop(columns=['pre_tropop', 'temp_sur', 'AO', 'NOI', "EA", 'AOD'])
    predictorsAO = predictors.drop(columns=['pre_tropop', 'temp_sur', 'NOI', "EA", 'AOD'])
    predictorsNOI = predictors.drop(columns=['pre_tropop', 'temp_sur', "EA", 'AOD'])
    predictorsEA = predictors.drop(columns=['pre_tropop', 'temp_sur', 'AOD'])
    predictorsAOD = predictors.drop(columns=['pre_tropop', 'temp_sur'])
    predictorspretropop = predictors.drop(columns=['temp_sur'])


#predictorstemp_sur = predictors.drop(columns=[ 'AO', 'NOI', "EA", 'AOD'])

#effect of temp surface is on the full predictor predictors

regression_outputilt = [0] * 36
uXilt = [0] * 36
uYilt = [0] * 36
param_listilt = [0] * 36
error_listilt = [0] * 36
trend_preilt = [0] * 36
trend_pre_errilt = [0] * 36
trend_postilt = [0] * 36
trend_post_errilt = [0] * 36
##
regression_outputpretropop = [0] * 36
uXpretropop = [0] * 36
uYpretropop = [0] * 36
param_listpretropop = [0] * 36
error_listpretropop = [0] * 36
trend_prepretropop = [0] * 36
trend_pre_errpretropop = [0] * 36
trend_postpretropop = [0] * 36
trend_post_errpretropop = [0] * 36
##
regression_outputAOD = [0] * 36
uXAOD = [0] * 36
uYAOD = [0] * 36
param_listAOD = [0] * 36
error_listAOD = [0] * 36
trend_preAOD = [0] * 36
trend_pre_errAOD = [0] * 36
trend_postAOD = [0] * 36
trend_post_errAOD = [0] * 36
##
regression_outputAO = [0] * 36
uXAO = [0] * 36
uYAO = [0] * 36
param_listAO = [0] * 36
error_listAO = [0] * 36
trend_preAO = [0] * 36
trend_pre_errAO = [0] * 36
trend_postAO = [0] * 36
trend_post_errAO = [0] * 36
##
regression_outputNOI = [0] * 36
uXNOI = [0] * 36
uYNOI = [0] * 36
param_listNOI = [0] * 36
error_listNOI = [0] * 36
trend_preNOI = [0] * 36
trend_pre_errNOI = [0] * 36
trend_postNOI = [0] * 36
trend_post_errNOI = [0] * 36
##
regression_outputEA = [0] * 36
uXEA = [0] * 36
uYEA = [0] * 36
param_listEA = [0] * 36
error_listEA = [0] * 36
trend_preEA = [0] * 36
trend_pre_errEA = [0] * 36
trend_postEA = [0] * 36
trend_post_errEA = [0] * 36
##
regression_outputeesc = [0] * 36
uXeesc = [0] * 36
uYeesc = [0] * 36
param_listeesc = [0] * 36
error_listeesc = [0] * 36
trend_preeesc = [0] * 36
trend_pre_erreesc = [0] * 36
trend_posteesc = [0] * 36
trend_post_erreesc = [0] * 36


##
regression_output = [0] * 36
uX = [0] * 36
uY = [0] * 36
param_list = [0] * 36
error_list = [0] * 36
trend_pre = [0] * 36
trend_pre_err = [0] * 36
trend_post = [0] * 36
trend_post_err = [0] * 36

for irt in range(24,-12,-1):
    alt[24-irt] = str(irt) + 'km_ds' #w.r.t. tropopause
    alt_ds[24-irt] = str(irt) + 'km_ds' #w.r.t. tropopause

    mY.append(irt)


for i in range(36):
    # alt_ds[i] = str(i) + 'km_ds'
    # alt[i] = str(i) + 'km'
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

    ## EESC
    predictorsEESC, uct[i] = pd.DataFrame.align(predictorsEESC, uct[i], axis=0)
    uYeesc[i] = uct[i][alt_ds[i]].values
    uXeesc[i] = predictorsEESC.values
    regression_outputeesc[i] = mzm_regression(uXeesc[i], uYeesc[i])
    param_listeesc[i] = dict(zip(list(predictorsEESC), regression_outputeesc[i]['gls_results'].params))
    error_listeesc[i] = dict(zip(list(predictorsEESC), regression_outputeesc[i]['gls_results'].bse))
    trend_preeesc[i] = param_listeesc[i]['linear_pre']
    trend_pre_erreesc[i] = error_listeesc[i]['linear_pre']
    trend_posteesc[i] = param_listeesc[i]['linear_post']
    trend_post_erreesc[i] = error_listeesc[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_preeesc[i] = trend_preeesc[i] * 100
    trend_pre_erreesc[i] = 2 * trend_pre_erreesc[i] * 100
    trend_posteesc[i] = trend_posteesc[i] * 100
    trend_post_erreesc[i] = 2 * trend_post_erreesc[i] * 100



    # ## pressure tropopause
    # predictorspretropop, uct[i] = pd.DataFrame.align(predictorspretropop, uct[i], axis=0)
    # uYpretropop[i] = uct[i][alt_ds[i]].values
    # uXpretropop[i] = predictorspretropop.values
    # regression_outputpretropop[i] = mzm_regression(uXpretropop[i], uYpretropop[i])
    # param_listpretropop[i] = dict(zip(list(predictorspretropop), regression_outputpretropop[i]['gls_results'].params))
    # error_listpretropop[i] = dict(zip(list(predictorspretropop), regression_outputpretropop[i]['gls_results'].bse))
    # trend_prepretropop[i] = param_listpretropop[i]['linear_pre']
    # trend_pre_errpretropop[i] = error_listpretropop[i]['linear_pre']
    # trend_postpretropop[i] = param_listpretropop[i]['linear_post']
    # trend_post_errpretropop[i] = error_listpretropop[i]['linear_post']
    # # for % in decade for relative montly anamoly
    # trend_prepretropop[i] = trend_prepretropop[i] * 100
    # trend_pre_errpretropop[i] = 2 * trend_pre_errpretropop[i] * 100
    # trend_postpretropop[i] = trend_postpretropop[i] * 100
    # trend_post_errpretropop[i] = 2 * trend_post_errpretropop[i] * 100
    #
    #



    predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)
    uY[i] = uct[i][alt_ds[i]].values
    uX[i] = predictors.values
    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))
    trend_pre[i] = param_list[i]['linear_pre']
    trend_pre_err[i] = error_list[i]['linear_pre']
    trend_post[i] = param_list[i]['linear_post']
    trend_post_err[i] = error_list[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_pre[i] = trend_pre[i] * 100
    trend_pre_err[i] = 2 * trend_pre_err[i] * 100
    trend_post[i] = trend_post[i] * 100
    trend_post_err[i] = 2 * trend_post_err[i] *100


plt.close('all')

fig, ax = plt.subplots()
plt.title('Uccle 1969-2018')
plt.xlabel('Ozone trend [%/dec]')
plt.ylabel('Altitude relative to tropopause [km]')
plt.xlim(-12, 12)
plt.ylim(-12,24)
ax.axvline(x=0, color='grey', linestyle='--')
ax.axhline(y=0, color='grey', linestyle=':')

ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_xticks([-10, -5,0,5,10])


if totalcolumn:
    plt.plot(trend_preilt, mY, label='pre ilt', color='red', linewidth=1.5)
    plt.plot(trend_preEA, mY, label='pre EAWR', color='indianred',linewidth = 1.5, linestyle = '--')
    plt.plot(trend_preNOI, mY, label='pre NAO', color='darkred', linewidth = 1.5, linestyle = ':')
    plt.plot(trend_preAOD, mY, label='pre AOD', color='purple', linewidth=1.5, linestyle = '--')
    plt.plot(trend_preAO, mY, label='pre AO', color='darkorange', linewidth=1.5, linestyle = ':')
    eb1 = ax.errorbar(trend_pre, mY, xerr=trend_pre_err, label='pre all (T100)', color='gold', linewidth=1.5,
            elinewidth=0.5, capsize=1.5, capthick=1)
    eb1[-1][0].set_linestyle('--')

    plt.plot(trend_postilt, mY, label='post ilt', color='limegreen', linewidth=2)
    plt.plot(trend_postEA, mY, label='post EAWR', color='forestgreen',linewidth = 1.5, linestyle = '--')
    plt.plot(trend_postNOI, mY, label='post NAO', color='dodgerblue', linewidth = 1.5, linestyle = ':')
    plt.plot(trend_postAOD, mY, label='post AOD', color='royalblue', linewidth=1.5, linestyle = '--')
    plt.plot(trend_postAO, mY, label='post AO', color='blue', linewidth=1.5, linestyle = ':')
    eb2 = ax.errorbar(trend_post, mY, xerr=trend_post_err, label='post all (T100)', color='black', linewidth=1.5,
            elinewidth=0.5, capsize=1.5, capthick=1)
    eb2[-1][0].set_linestyle('--')

else:
    plt.plot(trend_preilt, mY, label='pre ilt', color='red', linewidth = 1.5)
    plt.plot(trend_preAO, mY, label='pre AO', color='darkorange', linewidth = 1.5, linestyle = '--')
    plt.plot(trend_preNOI, mY, label='pre NOI', color='darkred', linewidth = 1.5, linestyle = '-.')
    plt.plot(trend_preEA, mY, label='pre EA', color='indianred',linewidth = 1.5, linestyle = '--')
    plt.plot(trend_preAOD, mY, label='pre AOD', color='purple',linewidth = 1.5, linestyle = '-.')
    plt.plot(trend_prepretropop, mY, label='pre pressure tropop', color='magenta', linewidth = 1.5, linestyle = '--')


    eb1 = ax.errorbar(trend_pre, mY, xerr=trend_pre_err, label='pre all', color='gold', linewidth=1.5, linestyle = '-.',
                elinewidth=0.5, capsize=1.5, capthick=1)
    eb1[-1][0].set_linestyle('--')

    plt.plot(trend_postilt, mY, label='post ilt', color='limegreen', linewidth = 1.5)
    plt.plot(trend_postAO, mY, label='post AO', color='forestgreen' , linewidth = 1.5, linestyle = '--')
    plt.plot(trend_postNOI, mY, label='post NOI', color='dodgerblue', linewidth = 1.5, linestyle = '-.')
    plt.plot(trend_postEA, mY, label='post EA', color='royalblue', linewidth = 1.5, linestyle = '--')
    plt.plot(trend_postAOD, mY, label='post AOD', color='blue', linewidth = 1.5, linestyle = '-.')
    plt.plot(trend_postpretropop, mY, label='post pressure tropop', color='cyan', linewidth = 1.5, linestyle = '--')

    eb2 = ax.errorbar(trend_post, mY, xerr=trend_post_err, label='post all', color='black', linewidth=1.2, linestyle = '-.',
                elinewidth=0.5, capsize=1.5, capthick=1)
    eb2[-1][0].set_linestyle('--')

#plt.plot(trend_postAOD, mY, label='post AOD', color='green')

ax.legend(loc='upper left', frameon=True, fontsize='small')


plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Step_RelTropop' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Step_RelTropop' + plname + '.eps')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.close()
