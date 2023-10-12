from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from LOTUS_regression.predictors.seasonal import add_seasonal_components


''' Code to apply MLR, ILT or new predictors to the Uccle data
    For data/model montly mean plots you need to add seasonal terms in the model'''

# boolean to run the code w.r.t. to reltropop of the absolute altitude
reltropop = False


def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    # plt.title('Total O3')
    plt.xlabel('Years')
    # plt.ylabel('Residuals')
    # plt.ylabel('Thickness of the ozone layer [DU]')
    plt.ylabel('Total O3 Relative Monthly Means')
    # plt.title(pltitle)

    # plt.plot(pX, pY, label='Residuals', color='blue')
    plt.plot(pX, pY, label='Data', color='blue', linewidth = 1)

    plt.plot(pX, pRegOutput, label='Model', color='red', linewidth = 1.2)

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/TotalO3/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/TotalO3/' + plname + '.eps')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.eps')
    plt.show()
    plt.close()
    plt.close()


###

def plotresidual(pX, pRegOutput, pltitle, plname):
    plt.close('all')

    fig, ax = plt.subplots()
    plt.title('Total O3 Relative Monthly Anamolies')
    # plt.title('Total O3 Monthly Means')

    plt.xlabel('Years')
    # plt.ylabel('Residuals')
    plt.ylabel('Residuals (Data - Model)')

    # plt.plot(pX, pY, label='Residuals', color='blue')
    # plt.plot(pX, pY, label='Data', color='blue')

    plt.plot(pX, pRegOutput, label='Model', color='black', linewidth = 0.75)

    # ax.legend(loc='upper right', frameon=True, fontsize='small')

    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/TotalO3/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/TotalO3/' + plname + '.eps')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.eps')
    plt.show()
    plt.close()
    plt.close()


######################################################################################################################


# part for using extended predictors
pre_name = 'ilt'
plname = 'Trend_' + pre_name
tag = ''

# predictors = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt.csv')
predictors=pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TotalColumnPredictors_ilt.csv')
predictors = predictors.drop(['AO', 'pre_tropop', 'temp_100', 'temp_500', 'EAWR', 'NAO'], axis = 1)

# try new predictors
# predictors= pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/NewPredictors_ilt.csv')

l2 = predictors['Unnamed: 0'].tolist()

print('l2', l2[0:5])

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
# predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)

# For Brewer Mast
predictors = predictors.loc['1971-07-01':'2018-12-01']

# only to plot data/model for monthly means
# predictors = add_seasonal_components(predictors, {'pre_const': 4, 'post_const':4, 'gap_cons':4})


uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TotalOzone_monthlymean.csv')




# uccle.rename(columns={'Unnamed: 0':'date'}, inplace=True)
#uccle['date'] =  dates
uccle['dateindex'] = pd.to_datetime(uccle['date'], format='%Y-%m')
print(uccle.dtypes)
# uccle = uccle['dateindex'].resample('6M').mean()

uccle.set_index('date', inplace=True)
print('uccle', len(uccle), list(uccle))

l1 = uccle.index.tolist()

print('l1', l1[0:5])



uccle['monthly_mean'] = uccle['mean'] - uccle['anamoly']
uccle['rel_anamoly'] = (uccle['mean'] - uccle['monthly_mean'])/ uccle['monthly_mean']



print('predictors', len(predictors), list(predictors))



print(uccle.index)


uccle_pre = uccle.loc['1971-07-01':'1996-12-01']
uccle_post = uccle.loc['2000-02-01':'2018-12-01']

mean_pre = np.nanmean(uccle_pre['mean'].values)
mean_post = np.nanmean(uccle_post['mean'].values)


common_dates12 = list(set(l1).intersection(set(l2)))

# only for total column ilt
uccle = uccle[uccle.index.isin(common_dates12)]
predictors = predictors[predictors.index.isin(common_dates12)]

print(len(uccle), len(predictors))
predictors, uccle = pd.DataFrame.align(predictors, uccle, axis=0)

print('last predictor', predictors[0:3])


uYra = uccle['rel_anamoly'].values
uY = uccle['mean'].values
uX = predictors.values
print('uX',uX)
print('uY', uY)
regression_output = mzm_regression(uX, uY)
param_list = dict(zip(list(predictors), regression_output['gls_results'].params))
error_list = dict(zip(list(predictors), regression_output['gls_results'].bse))

plotmlr_perkm(uccle.dateindex,uY,regression_output['fit_values'],'Total O3 Monthly Means','TotalOzone_totalcolumnilt')
# plotmlr_perkm(uccle.dateindex,uYra,regression_output['fit_values'],'Total O3 Monthly Means','TotalOzone_totalcolumnilt')

plotresidual(uccle.dateindex,regression_output['residual'],'residualmean','Residual_TotalOzone_totalcoulumnilt')

# # for relative anamoly
#
# regression_outputra = mzm_regression(uX, uYra)
# param_listra = dict(zip(list(predictors), regression_outputra['gls_results'].params))
# error_listra = dict(zip(list(predictors), regression_outputra['gls_results'].bse))
#
# plotmlr_perkm(uccle.dateindex,uYra,regression_outputra['fit_values'],'Total O3 Relative Monthly Anamolies','Relative_ilt')
# plotresidual(uccle.dateindex,regression_outputra['residual'],'residualmean','Residual_Relative_ilt')


trend_pre=param_list['linear_pre']
trend_pre_err=error_list['linear_pre']
trend_post=param_list['linear_post']
trend_post_err=error_list['linear_post']

# for ra

# trend_prera = param_listra['linear_pre']
# trend_pre_errra = error_listra['linear_pre']
# trend_postra = param_listra['linear_post']
# trend_post_errra = error_listra['linear_post']

# # for % in decade for relative monthly anamoly
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

# # # for  in decade for  montly means
# trend_pre=trend_pre  /mean_pre
# trend_pre_err=2 * trend_pre_err /mean_pre
# trend_post=trend_post / mean_post
# trend_post_err=2 * trend_post_err/mean_post
# #

print('trend_pre', trend_pre, ' err', trend_pre_err)
print('trend_post', trend_post, ' err', trend_post_err)

print('yearly')
print('pre', trend_pre/10)
print('post', trend_post/10)

print('monthl;y')
print('pre', trend_pre/120)
print('post', trend_post/120)


fig, ax = plt.subplots()

predictors[['linear_pre', 'linear_post']].plot(figsize=(16, 6))

# plt.title('Uccle 1969-2018')
# plt.xlabel('Ozone trend [%/dec]')
# plt.ylabel('Altitude [km]')
# plt.xlim(-10, 10)
# plt.ylim(0,32)
# ax.axvline(x=0, color='grey', linestyle='--')
#
# ax.tick_params(axis='both', which='both', direction='in')
# ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_ticks_position('both')
# # ax.yaxis.set_minor_locator(AutoMinorLocator(5))
# # ax.xaxis.set_minor_locator(AutoMinorLocator(5))
# ax.set_xticks([-10,-5,0,5,10])
#
#
# eb1 = ax.errorbar(trend_pre, uccle.dateindex, xerr=trend_pre_err, label='pre-1997', color='red', linewidth=1)
# eb1[-1][0].set_linestyle('--')
# eb2 = ax.errorbar(trend_post, uccle.dateindex, xerr=trend_post_err, label='post-2000', color='limegreen', linewidth=1)
# eb2[-1][0].set_linestyle('--')
#
# ax.legend(loc='upper right', frameon=True, fontsize='small')
#
# plt.show()

# print('decade rel anamoly')
# print('pre', trend_prera * 100)
# print('post', trend_postra * 100)
#
# print('month rel anamoly')
# print('pre', trend_prera/120)
# print('post', trend_postra/120 )

# didx = pd.DatetimeIndex(start ='1971-07-01', end = '2018-12-01', freq ='MS')
#
# print('year', didx.year)
# relative anamoly
# trend_pre -1.39265258923  err 0.986189844927
# trend_post 1.88317756816  err 1.52182046731

# plt.plot(didx.year,regression_output['fit_values'] )

# plt.plot(uccle.dateindex,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)
# plt.plot(uccle.dateindex, uX * trend_pre,label='Model',color='red',linewidth=0.75)
# plt.plot(didx.year,regression_output['fit_values'] )

# y = 2.7449 + didx.year*trend_pre/120
# y = didx.year*trend_pre/120

# print(y)

# y1 = 331
# t = -0.0411149462777
# post =  0.0324304947709
#
# x = [0] * 570
# xt = [0] * 570
# y = [0] * 570
#
# for i in range(570):
#     xt[i] = i
#     if i < 294:
#         x[i] = i
#         y[i] = y1 + (t*x[i])
#     if ( (i == 294) & (i < 333)):
#         x[i]= i
#         y[i]= y1
#     if i > 333:
#         x[i] = i
#         y[i] = y1 + (post *x[i])
#
#
#
#
#
# #
# #
# #
# fig, ax = plt.subplots()
#
# color = 'tab:red'
# ax.set_xlabel('time (s)')
# ax.set_ylabel('exp', color=color)
# plt.plot(uccle.dateindex,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)
# plt.plot(xt,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)

# ax.tick_params(axis='y', labelcolor=color)
#
# ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
#
# color = 'tab:blue'
# # ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax
# plt.plot(x,y)
# # ax2.tick_params(axis='y', labelcolor=color)
#
# # fig.tight_layout()  # otherwise the right y-label is slightly clipped

# pt = pd.pivot_table(uccle, index=uccle.index.year, columns=uccle.index.month,
#                     aggfunc='sum')
#
# print('pt[0:10', pt[-0:20])
#
# print(pt.index)
# pt.columns = pt.columns.droplevel()
#
# ticklabels = [datetime.date(1971,item,1).strftime('%Y') for item in pt.index]
# print('tick labels', ticklabels)
#
# ax.set_xticks(np.arange(0,47))
# ax.set_xticklabels(ticklabels) #add monthlabels to the xaxis


plt.show()
#
# # plt.plot(uccle.dateindex,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)
# # plt.plot(x,y)
# # plt.plot(uccle.dateindex, y ,label='Model',color='red',linewidth=0.75)
#
#
# # plt.plot(didx.year,y)
#
