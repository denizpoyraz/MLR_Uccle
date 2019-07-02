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

reltropop = True

# part for using extended predictors
pre_name = 'NewPredictors_Troposphere_ByOne_RelTropop'
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


# uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_all_relative.csv')
uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_deseas.csv')

#dates = pd.date_range(start='1992-11', end='2018-12', freq = 'MS')
setu = set(uccle.date.tolist())

# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
# pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)
#
# # # remove uccle missing dates:  Abs
# difup = setp.symmetric_difference(setu)
# diup = list(difup)
# uccle = uccle.drop(diup)

# # remove  missing dates: reltropop
removep = list(setp.difference(setu))
removeu = list(setu.difference(setp))
uccle = uccle.drop(removeu)
print('after uccle', len(uccle))

for j in range(len(removep)):
    removep[j] = datetime.strptime(removep[j], '%Y-%m-%d')
predictors = predictors.drop(removep)

alt = [''] * 36
alt_ds = [''] * 36

uc = {}
uct = {}
ucm = {}

mY = []
ut = [0] * 36

# ## predictors stepbystep
# predictorsilt = predictors.drop(columns=['AO', 'pre_tropop', 'temp_sur', 'NOI','EA'])
# predictorsNOI = predictors.drop(columns=['AO', 'pre_tropop', 'temp_sur','EA'])
# predictorstempsur = predictors.drop(columns=['AO', 'pre_tropop','EA'])

## predictors one each time
predictorsilt = predictors.drop(columns=['AO', 'pre_tropop', 'temp_sur', 'NOI','EA'])
predictorsNOI = predictors.drop(columns=['AO', 'pre_tropop', 'temp_sur','EA'])
predictorstempsur = predictors.drop(columns=['AO', 'pre_tropop', 'NOI','EA'])
predictorstropop = predictors.drop(columns=['AO', 'pre_tropop', 'EA'])

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
regression_outputtropop = [0] * 36
uXtropop = [0] * 36
uYtropop = [0] * 36
param_listtropop = [0] * 36
error_listtropop = [0] * 36
trend_pretropop = [0] * 36
trend_pre_errtropop = [0] * 36
trend_posttropop = [0] * 36
trend_post_errtropop = [0] * 36
##
regression_outputtempsur = [0] * 36
uXtempsur = [0] * 36
uYtempsur = [0] * 36
param_listtempsur = [0] * 36
error_listtempsur = [0] * 36
trend_pretempsur = [0] * 36
trend_pre_errtempsur = [0] * 36
trend_posttempsur = [0] * 36
trend_post_errtempsur = [0] * 36

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


## reltroopop
for i in range(-11, 25, 1):
    #reltropop
    akm = i
    i = i + 11
    mY.append(akm)
    alt_ds[i] = str(akm) + 'km_ds'
    alt[i] = str(akm) + 'km'
# abs altitude
# for i in range(36):
#     # reltropop
#     mY.append(i)
#     alt_ds[i] = str(i) + 'km_ds'
#     alt[i] = str(i) + 'km'



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
    predictorstempsur, uct[i] = pd.DataFrame.align(predictorstempsur, uct[i], axis=0)
    uYtempsur[i] = uct[i][alt_ds[i]].values
    uXtempsur[i] = predictorstempsur.values
    regression_outputtempsur[i] = mzm_regression(uXtempsur[i], uYtempsur[i])
    param_listtempsur[i] = dict(zip(list(predictorstempsur), regression_outputtempsur[i]['gls_results'].params))
    error_listtempsur[i] = dict(zip(list(predictorstempsur), regression_outputtempsur[i]['gls_results'].bse))
    trend_pretempsur[i] = param_listtempsur[i]['linear_pre']
    trend_pre_errtempsur[i] = error_listtempsur[i]['linear_pre']
    trend_posttempsur[i] = param_listtempsur[i]['linear_post']
    trend_post_errtempsur[i] = error_listtempsur[i]['linear_post']
    # for % in decade for relative montly anamoly
    trend_pretempsur[i] = trend_pretempsur[i] * 100
    trend_pre_errtempsur[i] = 2 * trend_pre_errtempsur[i] * 100
    trend_posttempsur[i] = trend_posttempsur[i] * 100
    trend_post_errtempsur[i] = 2 * trend_post_errtempsur[i] * 100


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
plt.xlim(-12, 12)
if reltropop: plt.ylim(-12,25)
else: plt.ylim(0,36)

ax.axvline(x=0, color='grey', linestyle='--')
ax.axhline(y=0, color='grey', linestyle=':')


ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_xticks([-10,-5,0,5,10])


# step by step
# eb0 = ax.errorbar(trend_preilt, mY, xerr=trend_pre_errilt, label='pre ilt', color='red', linewidth= 1,
#             elinewidth=0.5, capsize=1.5, capthick=1)
# eb0[-1][0].set_linestyle('--')
#
# plt.plot(trend_preNOI, mY, label='pre ilt+NOI', color='purple', linewidth = 1.5, linestyle = ':')
# plt.plot(trend_pretempsur, mY, label='pre ilt+NOI+temp. sur.', color='gold', linewidth = 2, linestyle = '--')

eb0 = ax.errorbar(trend_preilt, mY, xerr=trend_pre_errilt, label='pre ilt', color='red', linewidth= 1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb0[-1][0].set_linestyle('--')

plt.plot(trend_preNOI, mY, label='pre ilt+NOI', color='purple', linewidth = 1.5, linestyle = '--')
plt.plot(trend_pretempsur, mY, label='pre ilt+temp. sur.', color='salmon', linewidth = 1.5, linestyle = ':')
plt.plot(trend_pretropop, mY, label='pre all', color='gold', linewidth = 2, linestyle = "--")

# ## step by step
# eb3 = ax.errorbar(trend_postilt, mY, xerr=trend_post_errilt, label='post ilt', color='limegreen', linewidth= 1.5,
#             elinewidth=0.5, capsize=1.5, capthick=1)
# eb3[-1][0].set_linestyle('--')
# # plt.plot(trend_postilt, mY, label='post ilt', color='limegreen')
# plt.plot(trend_postNOI, mY, label='post ilt+NOI', color='blue', linewidth = 1.5, linestyle = ':')
#
# plt.plot(trend_posttempsur, mY, label='post ilt+NOI+temp. sur.', color='black', linewidth = 1.5, linestyle = '--')

eb3 = ax.errorbar(trend_postilt, mY, xerr=trend_post_errilt, label='post ilt', color='limegreen', linewidth= 1.5,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb3[-1][0].set_linestyle('--')
# plt.plot(trend_postilt, mY, label='post ilt', color='limegreen')
plt.plot(trend_postNOI, mY, label='post ilt+NOI', color='blue', linewidth = 1.5, linestyle = '--')

plt.plot(trend_posttempsur, mY, label='post ilt+temp. sur.', color='cyan', linewidth = 1.5, linestyle = ':')

plt.plot(trend_posttropop, mY, label='post all', color='black', linewidth = 1.5, linestyle = '--')


ax.legend(loc='lower left', frameon=True, fontsize='small')


plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle_' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle_' + plname + '.eps')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.show()
plt.close()
