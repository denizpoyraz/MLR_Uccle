from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

''' Code to apply MLR, ILT or new predictors to the Uccle data'''

# boolean to run the code w.r.t. to reltropop of the absolute altitude
reltropop = False


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title(pltitle)
    plt.xlabel('Years')
    # plt.ylabel('Residuals')
    plt.ylabel('PO3 (hPa)')

    # plt.plot(pX, pY, label='Residuals', color='blue')
    plt.plot(pX, pY, label='Data', color='blue')

    plt.plot(pX, pRegOutput, label='Model', color='orange')

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.eps')
    plt.close()
    plt.close()


######################################################################################################################


# part for using extended predictors
pre_name = 'ilt'
plname = 'Trend_' + pre_name
tag = ''

predictors = pd.read_csv('/home/poyraden/MLR_Uccle/Files/Extended_ilt.csv')

# try new predictors
# predictors= pd.read_csv('/home/poyraden/MLR_Uccle/Files/NewPredictors_ilt.csv')

setp = set(predictors['Unnamed: 0'].tolist())

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)

# For DeBilt
# predictors = predictors.loc['1992-11-01':'2018-12-01']

if reltropop: uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_reltropop_deas_relative.csv')
else: uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean_all_relative.csv')

setu = set(uccle.date.tolist())

# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
uccle['dateindex'] = pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)
print('uccle', len(uccle), list(uccle))


print('predictors', len(predictors), list(predictors))

# remove uccle missing dates:

difup = setp.symmetric_difference(setu)
diup = list(difup)
# uccle = uccle.drop(diup)

# uccle['date'] = pd.to_datetime(uccle['date'], format='%Y-%m')
# uccle.set_index('date', inplace=True)


print(uccle.index)


alt = [''] * 36
alt_ds = [''] * 36

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

    #uct[i] = uc[i].loc['1992-11-15':'20178-12-15']
    uct[i] = uc[i]

    predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)

    uY[i] = uct[i][alt_ds[i]].values
    uX[i] = predictors.values

    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))

    ut[i] = uct[i].index
    ptitle = str(alt[i])
    pname = pre_name + tag + str(alt[i])


    # plotmlr_perkm(uct[i].dateindex, regression_output[i]['residual'], regression_output[i]['fit_values'], ptitle, pname)
    plotmlr_perkm(uct[i].dateindex, uY[i], regression_output[i]['fit_values'], ptitle, pname)

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
plt.ylabel('Altitude [km]')
plt.xlim(-10, 10)
plt.ylim(0,32)
ax.axvline(x=0, color='grey', linestyle='--')

ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_xticks([-10,-5,0,5,10])


eb1 = ax.errorbar(trend_pre, mY, xerr=trend_pre_err, label='pre-1997', color='red', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')
eb2 = ax.errorbar(trend_post, mY, xerr=trend_post_err, label='post-2000', color='limegreen', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')

ax.legend(loc='upper right', frameon=True, fontsize='small')


plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle' + plname + '.pdf')
plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle' + plname + '.eps')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
# plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
plt.close()
