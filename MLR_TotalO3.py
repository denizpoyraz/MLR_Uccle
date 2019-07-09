from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from sklearn.linear_model import LinearRegression

''' Code to apply MLR, ILT or new predictors to the Uccle data'''

# boolean to run the code w.r.t. to reltropop of the absolute altitude
reltropop = False


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title('Total O3')
    plt.xlabel('Years')
    # plt.ylabel('Residuals')
    plt.ylabel('PO3 (hPa)')

    # plt.plot(pX, pY, label='Residuals', color='blue')
    plt.plot(pX, pY, label='Data', color='blue', linewidth = 1)

    plt.plot(pX, pRegOutput, label='Model', color='red', linewidth = 1.2)

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.pdf')
    # plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/pwlt_deseas/' + plname + '.eps')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.eps')
    plt.close()
    plt.close()


###

def plotresidual(pX, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title('Total O3')
    plt.xlabel('Years')
    # plt.ylabel('Residuals')
    plt.ylabel('Residuals (Data - Model)')

    # plt.plot(pX, pY, label='Residuals', color='blue')
    # plt.plot(pX, pY, label='Data', color='blue')

    plt.plot(pX, pRegOutput, label='Model', color='black', linewidth = 0.75)

    # ax.legend(loc='upper right', frameon=True, fontsize='small')

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

# For Brewer Mast
predictors = predictors.loc['1971-07-01':'2018-12-01']

uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/TotalOzone_monthlymean.csv')



setu = set(uccle.date.tolist())

# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
uccle['dateindex'] = pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)
print('uccle', len(uccle), list(uccle))

uccle['monthly_mean'] = uccle['mean'] - uccle['anamoly']
uccle['rel_anamoly'] = (uccle['mean'] - uccle['monthly_mean'])/ uccle['monthly_mean']



print('predictors', len(predictors), list(predictors))

# remove uccle missing dates:

difup = setp.symmetric_difference(setu)
diup = list(difup)
# uccle = uccle.drop(diup)

# uccle['date'] = pd.to_datetime(uccle['date'], format='%Y-%m')
# uccle.set_index('date', inplace=True)


print(uccle.index)


uccle_pre = uccle.loc['1971-07-01':'1996-12-01']
uccle_post = uccle.loc['2000-02-01':'2018-012-01']

mean_pre = np.nanmean(uccle_pre['mean'].values)
mean_post = np.nanmean(uccle_post['mean'].values)

predictors, uccle = pd.DataFrame.align(predictors, uccle, axis=0)

uY = uccle['rel_anamoly'].values
# uY = uccle['mean'].values

uX = predictors.values

regression_output = mzm_regression(uX, uY)
param_list = dict(zip(list(predictors), regression_output['gls_results'].params))
error_list = dict(zip(list(predictors), regression_output['gls_results'].bse))

plotmlr_perkm(uccle.dateindex,uY,regression_output['fit_values'],'testmean','testmean')
plotresidual(uccle.dateindex,regression_output['residual'],'residualmean','residualmean')


trend_pre=param_list['linear_pre']
trend_pre_err=error_list['linear_pre']
trend_post=param_list['linear_post']
trend_post_err=error_list['linear_post']

# # for % in decade for relative montly anamoly
# trend_pre=trend_pre * 100
# trend_pre_err=2 * trend_pre_err * 100
# trend_post=trend_post * 100
# trend_post_err=2 * trend_post_err * 100
#
#
# # for % in decade for  montly means
# trend_pre=trend_pre * 100 /mean_pre
# trend_pre_err=2 * trend_pre_err * 100/mean_pre
# trend_post=trend_post * 100/ mean_post
# trend_post_err=2 * trend_post_err * 100/mean_post
# #

# # for  in decade for  montly means
# trend_pre=trend_pre  /mean_pre
# trend_pre_err=2 * trend_pre_err /mean_pre
# trend_post=trend_post / mean_post
# trend_post_err=2 * trend_post_err/mean_post
# #

print('trend_pre', trend_pre, ' err', trend_pre_err)
print('trend_post', trend_post, ' err', trend_post_err)

print('monthly')
print('pre', trend_pre/10)
print('post', trend_post/10)

didx = pd.DatetimeIndex(start ='1971-07-01', end = '2018-12-01', freq ='MS')

print('year', didx.year)
# relative anamoly
# trend_pre -1.39265258923  err 0.986189844927
# trend_post 1.88317756816  err 1.52182046731

# plt.plot(didx.year,regression_output['fit_values'] )

# plt.plot(uccle.dateindex,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)
# plt.plot(uccle.dateindex, uX * trend_pre,label='Model',color='red',linewidth=0.75)
# plt.plot(didx.year,regression_output['fit_values'] )

# y = 2.7449 + didx.year*trend_pre/120
y = didx.year*trend_pre/120

print(y)

plt.plot(uccle.dateindex,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)
plt.plot(uccle.dateindex, y ,label='Model',color='red',linewidth=0.75)


# plt.plot(didx.year,y)

plt.show()