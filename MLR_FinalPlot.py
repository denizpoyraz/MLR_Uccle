from typing import List, Any

from LOTUS_regression.regression import mzm_regression
from matplotlib.ticker import AutoMinorLocator
from LOTUS_regression.predictors import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## second version of the code to make trend plot of DeBilt from 1992 only post trend and Uccle all range pre and post
## trends


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title(pltitle)
    plt.xlabel('Years')
    plt.ylabel('PO3 (hPa)')

    plt.plot(pX, pY, label='Data', color='blue')
    plt.plot(pX, pRegOutput, label='Model', color='orange')

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.eps')
    plt.show()
    plt.close()


######################################################################################################################

# these are pwlt predictors from 1977
# predictors = load_data('pred_baseline_ilt.csv')
# pre_name = 'Baseline_pwlt'
# plname = 'Trend_' + pre_name
# tag = ''

# part for using extended predictors
pre_name = 'RelTrop20km'
plname = 'Trend_' + pre_name
tag = ''
predictors = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt.csv')
# predictors=pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TotalColumnPredictors_ilt.csv')
# predictors = predictors.drop(['AO', 'pre_tropop', 'temp_100', 'temp_500', 'EAWR', 'NAO'], axis = 1)
predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)


predictorsd = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt.csv')
predictorsd.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictorsd['date'] = pd.to_datetime(predictorsd['date'], format='%Y-%m')
predictorsd.set_index('date', inplace=True)
# For DeBilt
predictorsd = predictors.loc['1992-12-01':'2018-12-01']
# predictorsd = predictorsd.loc['2000-01-01':'2018-12-01']

# for one linear term
predictorsone = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt_alltrend_nor.csv')
# #
predictorsone.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictorsone['date'] = pd.to_datetime(predictorsone['date'], format='%Y-%m')
predictorsone.set_index('date', inplace=True)

# uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean_deas_relative.csv')
# uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean_reltropop_deas_relative.csv')
uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/1km_monthlymean_reltropop_deseas.csv')
#
uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
uccle['date'] = pd.to_datetime(uccle['date'], format='%Y-%m')
# pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)

debilt = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/DeBilt_1km_monthlymean_reltropop_deas.csv')
# debilt = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/DeBilt_1km_monthlymean_deseas.csv')

debilt.rename(columns={'Unnamed: 0':'date'}, inplace=True)
# pd.to_datetime(debilt['date'], format='%Y-%m') # original
debilt['date'] = pd.to_datetime(debilt['date'], format='%Y-%m')
debilt.set_index('date', inplace=True)
# debilt = debilt.loc['2000-01-01':'2018-12-01']
debilt = debilt.loc['1992-12-01':'2018-12-01']

# ## only for w.r.t. stratosphere
# debilt = debilt.drop(columns=['-11km_ds', '-10km_ds', '-9km_ds', '-8km_ds', '-7km_ds', '-6km_ds', '-5km_ds', '-4km_ds',
#                      '-3km_ds', '-2km_ds', '-1km_ds'])
# uccle = uccle.drop(columns=['-11km_ds', '-10km_ds', '-9km_ds', '-8km_ds', '-7km_ds', '-6km_ds', '-5km_ds', '-4km_ds',
#                     '-3km_ds', '-2km_ds', '-1km_ds'])

## rearregne debilt and predictors
# lpd = predictorsd.index.tolist()
# ldb = debilt.index.tolist()
# common_datesdb = list(set(lpd).intersection(set(ldb)))
# debilt = debilt[debilt.index.isin(common_datesdb)]
# predictorsd = predictorsd[predictorsd.index.isin(common_datesdb)]

# do the same for uccle:
lpu = predictors.index.tolist()
lu = uccle.index.tolist()
common_datesu = list(set(lpu).intersection(set(lu)))
uccle = uccle[uccle.index.isin(common_datesu)]
# predictorsu = predictors[predictors.index.isin(common_datesu)]
predictorsu = predictors



print('debilt', list(debilt))
print('uccle', len(uccle),list(uccle))
print('predictorsu', len(predictorsu))
print('predictors', len(predictors))

# nsize = 25 # stra
# nsize = 36 # all range
nsize = 21


alt = [''] * nsize

# uc = pd.DataFrame()
# uct = pd.DataFrame()
ud = {}
udt = {}

regression_output = [0] * nsize
uX = [0] * nsize
uY = [0] * nsize
param_list = [0] * nsize
error_list = [0] * nsize

trend_post = [0] * nsize
trend_post_err = [0] * nsize

#uccle
uc = {}
uct = {}

regression_outputu= [0] * nsize
uXu = [0] * nsize
uYu = [0] * nsize
param_listu = [0] * nsize
error_listu = [0] * nsize

trend_postu = [0] * nsize
trend_post_erru = [0] * nsize

trend_preu = [0] * nsize
trend_pre_erru = [0] * nsize

## uccle one trend variables
uco = {}
ucto = {}

regression_outputo = [0] * nsize
uXo = [0] * nsize
uYo = [0] * nsize
param_listo = [0] * nsize
error_listo = [0] * nsize
uto = [0]*nsize

trend_allo = [0]*nsize
trend_allo_err = [0]*nsize

mY = []


## for rel to the ground comment this out
# for irt in range(24,-12,-1): #w.r.t. tropopause
for irt in range(20, -1, -1):  # w.r.t. tropopause

    alt[20-irt] = str(irt) + 'km_ds' #w.r.t. tropopause
    # print(irt + 0.5, alt[20-irt])
    mY.append(irt+0.5)
    # mY.append(irt)

print('mY', mY)


# for i in range(36):
## for w.r.t. the ground
#     mY.append(i)
#     alt[i] = str(i) + 'km_ds'  #

for i in range(20,-1,-1): # only for plotting stratosphere
# for i in range(24,-12,-1):

    #debilt
    udt[i] = debilt

    # print('before,' , len(debilt), len(predictorsd))
    # print('dfd before', udt[i][alt[i]])
    # print('dfd predictorsd', predictorsd)

    predictorsd, udt[i] = pd.DataFrame.align(predictorsd, udt[i], axis=0)

    # print('after,', len(debilt), len(predictorsd))

    uY[i] = udt[i][alt[i]].values
    uX[i] = predictorsd.values
    # print('dfd after', udt[i][alt[i]])
    # print(i, alt[i], uY[i], uX[i])

    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictorsd), regression_output[i]['gls_results'].params))
    # print('one', param_list[i])

    error_list[i] = dict(zip(list(predictorsd), regression_output[i]['gls_results'].bse))

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

    predictorsu, uct[i] = pd.DataFrame.align(predictorsu, uct[i], axis=0)

    uYu[i] = uct[i][alt[i]].values
    uXu[i] = predictorsu.values

    regression_outputu[i] = mzm_regression(uXu[i], uYu[i])
    param_listu[i] = dict(zip(list(predictorsu), regression_outputu[i]['gls_results'].params))
    error_listu[i] = dict(zip(list(predictorsu), regression_outputu[i]['gls_results'].bse))

    ptitle = str(alt[i])
    pname = 'Uccle_' + pre_name + tag + str(alt[i])
    #plotmlr_perkm(uct[i], uYu[i], regression_outputu[i]['fit_values'], ptitle, pname)

    trend_postu[i] = param_listu[i]['linear_post']
    trend_post_erru[i] = error_listu[i]['linear_post']

    trend_preu[i] = param_listu[i]['linear_pre']
    trend_pre_erru[i] = error_listu[i]['linear_pre']

    # for % in decade for relative montly anamoly
    trend_postu[i] = trend_postu[i] * 100
    trend_post_erru[i] = 2 * trend_post_erru[i] * 100

    trend_preu[i] = trend_preu[i] * 100
    trend_pre_erru[i] = 2 * trend_pre_erru[i] * 100

# for monthly anamoly
    # trend_post[i] = trend_post[i] * 100 / (mean_post[i] * 10)
    # trend_post_err[i] = 2 * trend_post_err[i] * 100 / (mean_post[i] * 10)
    # trend_post[i] = trend_post[i] * 100 / (mean_post[i] * 10)
    # trend_post_err[i] = 2 * trend_post_err[i] * 100 / (mean_post[i] * 10)

    ## one trend term for uccle
    ucto[i] = uccle
    predictorsone, ucto[i] = pd.DataFrame.align(predictorsone, ucto[i], axis=0)
    uYo[i] = ucto[i][alt[i]].values
    uXo[i] = predictorsone.values
    regression_outputo[i] = mzm_regression(uXo[i], uYo[i])
    param_listo[i] = dict(zip(list(predictorsone), regression_outputo[i]['gls_results'].params))
    error_listo[i] = dict(zip(list(predictorsone), regression_outputo[i]['gls_results'].bse))
    uto[i] = ucto[i].index
    trend_allo[i] = param_listo[i]['linear_one'] *100
    trend_allo_err[i] = 2 * error_listo[i]['linear_one'] *100

# print('debilt', trend_post)
# print('pramlist', param_listu)
trend_preu = [round(i,3) for i in trend_preu]
trend_pre_erru = [round(i,3) for i in trend_pre_erru]
print('uccle pre', trend_preu)
print('uccle pre error', trend_pre_erru)
print('mY', mY)
print('alt', alt)
trend_postu = [round(i,3) for i in trend_postu]
trend_post_erru = [round(i,3) for i in trend_post_erru]

print('uccle post', trend_postu)
print('uccle post error', trend_post_erru)

plt.close('all')

fig, ax = plt.subplots()
plt.title('')
plt.xlabel(r'Ozone Trend [% dec$^{-1}$]')
# plt.ylabel('Altitude [km]')
plt.ylabel('Altitude relative to the tropopause [km]')

# plt.xlim(-8, 12) ## w.r.t. reltropop
# plt.xlim(-10, 12) ## w.r.t. stratosphre
plt.xlim(-10, 10) ## w.r.t. reltropop

# plt.ylim(-12,25) ## w.r.t. reltropop
# plt.ylim(0,25) ## w.r.t. stratosphre
plt.ylim(0,21) ## w.r.t. stratosphre


# plt.ylim(0, 33)

ax.axvline(x=0, color='grey', linestyle='--')
ax.axhline(y=0, color='grey', linestyle=':')

ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
# ax.set_xticks([-5,0,5,10]) ## w.r.t. reltropop
ax.set_xticks([-10,-5,0,5,10]) ## w.r.t. stratosphere
ax.set_yticks([0,5,10, 15, 20]) ## w.r.t. stratosphere

em = [i-j for i,j in zip(trend_allo,trend_allo_err)]
ep = [i+j for i,j in zip(trend_allo , trend_allo_err)]

empre = [i-j for i,j in zip(trend_preu,trend_pre_erru)]
eppre = [i+j for i,j in zip(trend_preu , trend_pre_erru)]

empost = [i-j for i,j in zip(trend_postu,trend_post_erru)]
eppost = [i+j for i,j in zip(trend_postu , trend_post_erru)]

dmpost = [i-j for i,j in zip(trend_post,trend_post_err)]
dppost = [i+j for i,j in zip(trend_post, trend_post_err)]


eb4 = ax.errorbar(trend_allo, mY, xerr= trend_allo_err, label='Uccle 1969-2018', color='black', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb4[-1][0].set_linestyle('--')
# ax.plot(em, mY,  color='black', linewidth=1, linestyle = "none", marker="o", markersize=3 )
# ax.plot(ep, mY,  color='black', linewidth=1, linestyle = "none", marker = 'o' , markersize=3)


eb3 = ax.errorbar(trend_preu, mY, xerr=trend_pre_erru, label='Uccle 1969-1996', color='red', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb3[-1][0].set_linestyle('--')
# eb3[-1][0].set_linestyle('-.')
# ax.plot(empre, mY,  color='red', linewidth=1, linestyle = "none", marker = 's', markersize=3 )
# ax.plot(eppre, mY,  color='red', linewidth=1, linestyle = "none", marker = 's' , markersize=3)


eb1 = ax.errorbar(trend_postu, mY, xerr=trend_post_erru, label='Uccle 2000-2018', color='limegreen', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')
# eb1[-1][0].set_linestyle(':')
# ax.plot(empost, mY,  color='limegreen', linewidth=1, linestyle = "none", marker = 'v', markersize=3 )
# ax.plot(eppost, mY,  color='limegreen', linewidth=1, linestyle = "none", marker = 'v' , markersize=3)
#
eb2 = ax.errorbar(trend_post, mY, xerr=trend_post_err, label='DeBilt 2000-2018', color='blue', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')
# eb2[-1][0].set_linestyle(':')
# ax.plot(dmpost, mY,  color='blue', linewidth=1, linestyle = "none", marker = '^' , markersize=3)
# ax.plot(dppost, mY,  color='blue', linewidth=1, linestyle = "none", marker = '^', markersize=3 )

print('trend_allo', trend_allo)



# #new style
# ax.errorbar(trend_allo, mY, xerr= trend_allo_err, label='Uccle 1969-2018', color='black', linewidth=1.5,
#             elinewidth=0.3, capsize=1, capthick=1)
# # ax.plot(trend_allo, mY, label='Uccle 1969-2018', color='black', linewidth=1 )
# ax.plot(em, mY,  color='black', linewidth=1, linestyle = "none", marker="o", markersize=3 )
# ax.plot(ep, mY,  color='black', linewidth=1, linestyle = "none", marker = 'o' , markersize=3)

# ax.fill_betweenx(mY,  em, ep, alpha=0.2, facecolor='k')
# ax.plot(trend_preu, mY, label='Uccle 1969-1996', color='red')
# ax.errorbar(trend_preu, mY, xerr=trend_pre_erru, label='Uccle 1969-1996', color='red', linewidth=1.5,
#             elinewidth=0.3, capsize=1.5, capthick=1)
# ax.plot(empre, mY,  color='red', linewidth=1, linestyle = "none", marker = 's', markersize=3 )
# ax.plot(eppre, mY,  color='red', linewidth=1, linestyle = "none", marker = 's' , markersize=3)

# ax.errorbar(trend_postu, mY, xerr=trend_post_erru, label='Uccle 2000-2018', color='limegreen', linewidth=1.5,
#             elinewidth=0.3, capsize=1.5, capthick=1)
# ax.plot(empost, mY,  color='limegreen', linewidth=1, linestyle = "none", marker = 'v', markersize=3 )
# ax.plot(eppost, mY,  color='limegreen', linewidth=1, linestyle = "none", marker = 'v' , markersize=3)

# ax.plot(trend_postu, mY, label='Uccle 2000-2018', color='limegreen')
# ax.fill_betweenx(mY, empre, eppre, alpha=0.2, facecolor='red')
# ax.fill_betweenx(mY, empost, eppost, alpha=0.2, facecolor='limegreen')

# ax.errorbar(trend_post, mY, xerr=trend_post_err, label='DeBilt 2000-2018', color='blue', linewidth=1.5,
#             elinewidth=0.3, capsize=1.5, capthick=1)
# ax.plot(dmpost, mY,  color='blue', linewidth=1, linestyle = "none", marker = '^' , markersize=3)
# ax.plot(dppost, mY,  color='blue', linewidth=1, linestyle = "none", marker = '^', markersize=3 )

#
# ax.plot(trend_post, mY, label='DeBilt 2000-2018', color='blue')
# ax.fill_betweenx(mY, dmpost, dppost, alpha=0.2, facecolor='blue')

ax.legend(loc='upper right', frameon=True, fontsize='small')

plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Fig2_new' + '.pdf')
plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Fig2_new' + '.eps')
plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/Fig2_new' + '.png')

# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/All' + plname + '.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years_2/All' + plname + '.eps')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_DeBilt/' + plname + '.eps')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.show()
plt.close()
