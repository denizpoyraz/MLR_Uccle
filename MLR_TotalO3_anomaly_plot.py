from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import gridspec
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
    # plt.ylabel('Total O3 Relative Monthly Means')
    plt.title(pltitle)

    # plt.plot(pX, pY, label='Residuals', color='blue')
    plt.plot(pX, pY, label='Data', color='blue', linewidth = 1)

    plt.plot(pX, pRegOutput, label='Model', color='red', linewidth = 1.2)

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/' + plname + '.pdf')
    plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/' + plname + '.eps')
    plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/' + plname + '.png')

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

predictors = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt.csv')
predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['dateindex'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors['dateindex'] = predictors['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))

predictors['dateindex_two'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors['dindex'] = predictors['dateindex_two'].dt.date.apply(lambda x: x.strftime('%Y-%m'))

predictors.set_index('dindex', inplace=True)
predictors = predictors.loc['1972-01':'2018-12']
l2 = predictors.dateindex.tolist()
# print('predictors ', predictors[0:5])
print('l2', l2[0:5])

print('predictors', list(predictors))

predictors = predictors.drop(['date', 'dateindex','dateindex_two'], axis =1)
predictors_noilt = predictors.drop(['linear_pre', 'linear_post', 'post_const', 'pre_const', 'gap_const'], axis=1)


uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_monthly.csv')
# uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_smoothed.csv')


uccle = uccle[(uccle.Date < '2019-01-01') & (uccle.Date >= '1972-01-01')]
# print(uccle.Date.min(), uccle.Date.max())


uccle['dateindex'] = pd.to_datetime(uccle['Date'], format='%Y-%m-%d')
uccle['dindex'] = uccle['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
uccle['dateindex_two'] = uccle['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
uccle.set_index('dindex', inplace=True)
l1 = uccle['dateindex_two'].tolist()
print('l1', l1)





common_dates12 = list(set(l1).intersection(set(l2)))
uccle = uccle[uccle.index.isin(common_dates12)]
predictors = predictors[predictors.index.isin(common_dates12)]



uccle_pre = uccle.loc['1971-12-01':'1996-12-01']
uccle_post = uccle.loc['2000-01-01':'2018-12-01']

mean_pre = np.nanmean(uccle_pre['TO'].values)
mean_post = np.nanmean(uccle_post['TO'].values)


#
#
uY = uccle['anomaly'].values
uX = predictors.values
uX_noilt = predictors_noilt.values

# print('uX', uX)
# print('uY', uY)
regression_output_anomaly = mzm_regression(uX, uY)
regression_output_anomaly_noilt = mzm_regression(uX_noilt, uY)

param_list_anomaly = dict(zip(list(predictors), regression_output_anomaly['gls_results'].params))
error_list = dict(zip(list(predictors), regression_output_anomaly['gls_results'].bse))
# param_list_anomaly['linear_pre'] = round(param_list_anomaly['linear_pre'] * 100 / (mean_pre ),3)
# param_list_anomaly['linear_post'] = round(param_list_anomaly['linear_post'] * 100 / (mean_post),3)

print('before anomaly linear_pre', param_list_anomaly['linear_pre'])
print('befire anomaly linear_post', param_list_anomaly['linear_post'])
print('before errors', regression_output_anomaly['gls_results'].bse)

pl = regression_output_anomaly['gls_results'].params
pl = [round(i, 3) for i in pl]
pl[0] = round(pl[0]* 100 / (mean_pre ),3)
pl[1] = round(pl[1]* 100 / (mean_pre ),3)
pl = dict(zip(list(predictors),pl))
# print('pl', pl)
print('param_list_anomaly',pl)
# print('predictors', predictors[0:3])
pl = regression_output_anomaly['gls_results'].bse
pl[0] = round(pl[0]* 100 / (mean_pre ),3)
pl[1] = round(pl[1]* 100 / (mean_pre ),3)
pl = [round(i, 3) for i in pl]
pl = dict(zip(list(predictors),pl))
print('error_list_anomaly',pl)


#
uYra = uccle['rel_anomaly'].values
regression_output_relanomaly = mzm_regression(uX, uYra)
param_list_relanomaly = dict(zip(list(predictors), regression_output_relanomaly['gls_results'].params))
error_list_relanomaly = dict(zip(list(predictors), regression_output_relanomaly['gls_results'].bse))
print('before rel anomaly linear_pre', param_list_relanomaly['linear_pre'])
print('befire rel anomaly linear_post', param_list_relanomaly['linear_post'])

pla = regression_output_relanomaly['gls_results'].params
pla = [round(i*100, 3) for i in pla]
pla = dict(zip(list(predictors),pla))
# print('pl', pl)
# print('param_list',pl)

print('param_list_rel_anomaly', pla)
pla = regression_output_relanomaly['gls_results'].bse
pla = [round(i*100, 3) for i in pla]
pla = dict(zip(list(predictors),pla))
print('error_list_rel_anomaly', pla)

#
#
# plotmlr_perkm(uccle.dateindex,uY,regression_output_anomaly['fit_values'],'Total O3 Monthly Anomaly','TotalOzone_DataModel_anomaly_notsmoothed_v2')
# plotmlr_perkm(uccle.dateindex,uYra,regression_output_relanomaly['fit_values'],'Total O3 Monthly Relative Anomaly','TotalOzone_DataModel_relanomaly_notsmoothed_v2')



trend_pre_anomaly=param_list_anomaly['linear_pre']
trend_post_anomaly=param_list_anomaly['linear_post']
trend_pre_relanomaly=param_list_relanomaly['linear_pre']
trend_post_relanomaly=param_list_relanomaly['linear_post']

# trend_pre_12m_anomaly=param_list_12m_anomaly['linear_pre']
# trend_post_12m_anomaly=param_list_12m_anomaly['linear_post']
# trend_pre_12m_relanomaly=param_list_12m_relanomaly['linear_pre']
# trend_post_12m_relanomaly=param_list_12m_relanomaly['linear_post']
#
# print('yearly trends anomaly', trend_pre_12m_anomaly, trend_post_12m_anomaly)
# print('yearly trends rel anomaly', trend_pre_12m_relanomaly, trend_post_12m_relanomaly)

print('monthly trends anomaly', trend_pre_anomaly, trend_post_anomaly)
print('monthly trends rel anomaly', trend_pre_relanomaly, trend_post_relanomaly)



predictors['dindex'] = pd.to_datetime(predictors.index, format='%Y-%m')

uccle['dindex'] = pd.to_datetime(uccle.Date, format='%Y-%m')

print('predictors', list(predictors))


#Monthly
# test = predictors12m[predictors12m.index < '1997-01-01']['linear_pre'].tolist()
pretrend = predictors[predictors.dindex < '1997-01-01']['linear_pre'].tolist()
# pretrend = predictors['linear_pre'].tolist()
pretrendm = [i * trend_pre_anomaly for i in pretrend]
pre_const = param_list_anomaly['pre_const']
pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)

posttrend = predictors[predictors.dindex > '2000-01-01']['linear_post'].tolist()
posttrendm = [i * trend_post_anomaly for i in posttrend]
post_const = param_list_anomaly['post_const']
posttrendmp = [i + post_const for i in posttrendm]

print('coeffcieints:')
print('enso', param_list_anomaly['enso'], 'qboA', param_list_anomaly['qboA'], 'qboB',  param_list_anomaly['qboB'] )
print('solar',  param_list_anomaly['solar'], 'AOD',  param_list_anomaly['AOD'])

## new plot for the paper

# fig = plt.figure()
# # set height ratios for subplots
# gs = gridspec.GridSpec(6, 1, height_ratios=[2,1,1,1,1,1])
# 
# # the first subplot
# ax0 = plt.subplot(gs[0])

# fig, ax = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3,1, 1], 'hspace': [0.5, 0, 0]})
# fig.suptitle('Vertically stacked subplots')

# gs_topone = plt.GridSpec(2, 1, top=0.95)
# gs_topone = plt.GridSpec(2, 1, top=0.95,  hspace=0.25)
gs_top = plt.GridSpec(6, 1, height_ratios=[3,2,1,1,1,1], hspace=0.05)
gs_toptwo = plt.GridSpec(6, 1, height_ratios=[3,2,1,1,1,1], hspace=0.25)

gs_base = plt.GridSpec(6, 1, height_ratios = [3,2,1,1,1,1], hspace = 0)
fig = plt.figure()

ax0 = fig.add_subplot(gs_top[0,:])
ax0.xaxis.set_major_locator(mdates.YearLocator(3))
ax0.xaxis.set_minor_locator(mdates.YearLocator(1))
ax0.plot(uccle.dateindex, uccle.anomaly, label = 'Total ozone anomalies', color = '#7f7f7f')
ax0.plot(uccle.dateindex, regression_output_anomaly['fit_values'], label = 'Regressed natural variations + ILT trend', color = 'black')
ax0.plot(uccle.dateindex, regression_output_anomaly_noilt['fit_values'], label = 'Regressed natural variations', color = '#1f77b4', linestyle = '--')
ax0.plot(predictors[predictors.dindex < '1997-01-01'].dindex, pretrendmp, label = 'Regressed ILT trends', color = '#d62728', linewidth = '2')
ax0.plot(predictors[predictors.dindex > '2000-01-01'].dindex,posttrendmp, color = '#d62728', linewidth = '2')
ax0.axhline(0, color='black', linewidth=0.8, linestyle = '--')
ax0.legend(loc='lower right', frameon=True, fontsize='x-small')
ax0.set_ylabel('Ozone anomalies [DU]')

# ax1 = plt.subplot(gs[1])
ax1 = fig.add_subplot(gs_toptwo[1,:])

ax1.xaxis.set_major_locator(mdates.YearLocator(3))
ax1.xaxis.set_minor_locator(mdates.YearLocator(1))
ax1.plot(uccle.dindex, regression_output_anomaly['residual'], label = 'Residuals', color = 'black')
ax1.axhline(0, color='black', linewidth=0.8, linestyle = '--')
ax1.legend(loc='lower right', frameon=True, fontsize='small')


# ax2 = plt.subplot(gs[2], sharex = True)
# 'enso', 'qboA', 'qboB', 'solar', 'AOD'

# ax2 = plt.subplot(gs[2])
ax2 = fig.add_subplot(gs_base[2,:])
# ax2.plot(predictors.dindex, predictors['enso'], label='ENSO', color = '#2ca02c')
ax2.plot(predictors.dindex, predictors['enso']*param_list_anomaly['enso'], label='ENSO', color = '#2ca02c')
# ax2.plot(predictors.dindex, predictors['enso'], label='ENSO 0')

ax2.axhline(0, color='black', linewidth=0.8, linestyle = '--')
ax2.legend(loc='lower right', frameon=True, fontsize='small')
#
ax3 = fig.add_subplot(gs_base[3,:])
# ax3.plot(predictors.dindex, predictors['qboA'], label = 'QBO1 (50 hPa)', color = '#9467bd')
# ax3.plot(predictors.dindex, predictors['qboB'], label = 'QBO2 (30 hPa)', color = '#ff7f0e')

ax3.plot(predictors.dindex, predictors['qboA']*param_list_anomaly['qboA'], label = 'QBO1 (50 hPa)', color = '#9467bd')
ax3.plot(predictors.dindex, predictors['qboB']*param_list_anomaly['qboB'], label = 'QBO2 (30 hPa)', color = '#ff7f0e')
# ax3.plot(predictors.dindex, predictors['qboA'], label = 'QBO1 0(50 hPa)')
# ax3.plot(predictors.dindex, predictors['qboB'], label = 'QBO2 0 (30 hPa)')
ax3.axhline(0, color='black', linewidth=0.8, linestyle = '--')
ax3.legend(loc='lower right', frameon=True, fontsize='small')

ax4 = fig.add_subplot(gs_base[4,:])
ax4.plot(predictors.dindex, predictors['solar']*param_list_anomaly['solar'], color = '#17becf', label = 'Solar')
# ax4.plot(predictors.dindex, predictors['solar'], color = '#17becf', label = 'Solar')
# ax4.plot(predictors.dindex, predictors['solar'], label = 'Solar 0')

ax4.axhline(0, color='black', linewidth=0.8, linestyle = '--')
ax4.legend(loc='lower right', frameon=True, fontsize='small')

ax5 = fig.add_subplot(gs_base[5,:])
ax5.xaxis.set_major_locator(mdates.YearLocator(3))
ax5.xaxis.set_minor_locator(mdates.YearLocator(1))
# ax5.plot(predictors.dindex, predictors['AOD'], color = '#1f77b4', label = 'AOD')
ax5.plot(predictors.dindex, predictors['AOD']*param_list_anomaly['AOD'], color = '#1f77b4', label = 'AOD')
# ax5.plot(predictors.dindex, predictors['AOD'], label = 'AOD 0')

ax5.axhline(0, color='black', linewidth=0.8, linestyle = '--')
ax5.legend(loc='lower right', frameon=True, fontsize='small')

plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax4.get_xticklabels(), visible=False)
# plt.setp(ax5.get_xticklabels(), visible=False)


# uccle.dateindex,uY,regression_output_anomaly['fit_values'],
# ax1.plot(x, -y)

# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_newplot.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_newplot.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_newplot.eps')

plt.show()


# fig, ax = plt.subplots()
#
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=365))   #to get a tick every 15 minutes
# # ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
#
# plt.plot(uccle.index, uccle['anomaly'], color = '#1f77b4', label = 'Total ozone monthly anomaly')
# plt.plot(predictors[predictors.index < '1997-01-01'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors[predictors.index > '2000-01-01'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_notsmoothed_v2.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_notsmoothed_v2.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_notsmoothed_v2.eps')
#
# plt.show()
# plt.close()
#
# pretrend = predictors[predictors.index < '1997-01-01']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_relanomaly for i in pretrend]
# pre_const = param_list_relanomaly['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors[predictors.index > '2000-01-01']['linear_post'].tolist()
# posttrendm = [i * trend_post_relanomaly for i in posttrend]
# post_const = param_list_relanomaly['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
# ax.xaxis.set_major_locator(mdates.YearLocator(4))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
#
# plt.plot(uccle.index, uccle['rel_anomaly'], color = '#1f77b4', label = 'Total ozone monthly relative anomaly')
# plt.plot(predictors[predictors.index < '1997-01-01'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors[predictors.index > '2000-01-01'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_relanomaly_notsmoothed_v2.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_relanomaly_notsmoothed_v2.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_relanomaly_notsmoothed_v2.eps')
#
# plt.show()
# plt.close()
# #
#
#
# # ## Yearly

# # uccle.set_index('date', inplace=True)
# uccle12m = uccle.resample('12M', on='dateindex').mean()
# uccle12m['dateindex'] = pd.to_datetime(uccle12m.index, format='%Y-%m')
# uccle12m['dindex'] = uccle12m.dateindex.dt.date.apply(lambda x: x.strftime('%Y-%m'))
# l1_12m = uccle12m.dindex.tolist()
#
# # print('uccle', len(uccle), list(uccle))
# # print(uccle12m[0:5])
#
# print('l1_12m', l1_12m[0:5])
# print('predictors', len(predictors), list(predictors))

# predictors12m = predictors.resample('12M',on='dateindex_two').mean()
# # print('one predictors 12m', predictors12m[0:5])
# predictors12m['dateindex'] = pd.to_datetime(predictors12m.index, format='%Y-%m')
# predictors12m['dindex'] = predictors12m.dateindex.dt.date.apply(lambda x: x.strftime('%Y-%m'))
#
# print('predictors 12m', list(predictors12m))
# l2_12m = predictors12m.dindex.tolist()
# print('l2 12m', l2_12m)

# common_dates12m = list(set(l1_12m).intersection(set(l2_12m)))
# uccle12m = uccle12m[uccle12m.dindex.isin(common_dates12m)]
# predictors12m = predictors12m[predictors12m.dindex.isin(common_dates12m)]
#
# print(len(predictors), len(predictors12m))
# print(len(uccle), len(uccle12m))
#
# predictors, uccle = pd.DataFrame.align(predictors, uccle, axis=0)
# predictors12m, uccle12m = pd.DataFrame.align(predictors12m, uccle12m, axis=0)
# predictors = predictors.drop(['date' ,'dateindex_two','dateindex'],axis=1)
# predictors12m = predictors12m.drop(['dindex','dateindex'],axis=1)
# #
# pretrend = predictors12m[predictors12m.index < '1997-01-01']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_12m_anomaly for i in pretrend]
# pre_const = param_list_12m_anomaly['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# # print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors12m[predictors12m.index > '2000-01-01']['linear_post'].tolist()
# # posttrend = predictors12m['linear_post'].tolist()
# posttrendm = [i * trend_post_12m_anomaly for i in posttrend]
# post_const = param_list_12m_anomaly['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
#
# # ax.set_xlim(1971, 2019)
# ax.xaxis.set_major_locator(mdates.YearLocator(5))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
# plt.plot(uccle12m.index, uccle12m['anomaly'], color = '#1f77b4', label = 'Total ozone yearly anomaly')
# # plt.plot(predictors12m.index, pretrendmp, label = 'ILT pre', color = '#d62728')
# # plt.plot(predictors12m.index ,posttrendmp, label = 'ILT post', color = '#2ca02c')
# plt.plot(predictors12m[predictors12m.index < '1997-01-01'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors12m[predictors12m.index > '2000-01-01'].index,posttrendmp, label = 'ILT post',  color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m_notsmoothed_v2.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m_notsmoothed_v2.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m_notsmoothed_v2.eps')
#
# plt.show()
# plt.close()


# pretrend = predictors12m[predictors12m.index < '1997-01-01']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_12m_relanomaly for i in pretrend]
# pre_const = param_list_12m_relanomaly['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors12m[predictors12m.index > '2000-01-01']['linear_post'].tolist()
# posttrendm = [i * trend_post_12m_relanomaly for i in posttrend]
# post_const = param_list_12m_relanomaly['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
# ax.xaxis.set_major_locator(mdates.YearLocator(4))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
#
# plt.plot(uccle12m.index, uccle12m['rel_anomaly'], color = '#1f77b4', label = 'Total ozone yearly reative anomaly')
# plt.plot(predictors12m[predictors12m.index < '1997-01-01'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors12m[predictors12m.index > '2000-01-01'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m_relanomaly_notsmoothed_v2.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m_relanomaly_notsmoothed_v2.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m_relanomaly_notsmoothed_v2.eps')
#
# plt.show()
# plt.close()


# #
# uY12m = uccle12m['anomaly'].values
# uX12m = predictors12m.values
# regression_output_12m_anomaly = mzm_regression(uX12m, uY12m)
# param_list_12m_anomaly = dict(zip(list(predictors12m), regression_output_12m_anomaly['gls_results'].params))
# error_list_12m_anomaly = dict(zip(list(predictors12m), regression_output_12m_anomaly['gls_results'].bse))
# print('yearly before anomaly linear_pre', param_list_12m_anomaly['linear_pre'])
# print('yearly befire anomaly linear_post', param_list_12m_anomaly['linear_post'])
# pla = regression_output_12m_anomaly['gls_results'].params
# pla = [round(i,3) for i in pla]
# pla[0] = round(pla[0]* 100 / (mean_pre ),3)
# pla[1] = round(pla[1]* 100 / (mean_pre ),3)
# pla = dict(zip(list(predictors12m),pla))
# print('anaomaly yearly param_list12m', pla)
# pla = regression_output_12m_anomaly['gls_results'].bse
# pla = [round(i,3) for i in pla]
# pla[0] = round(pla[0]* 100 / (mean_pre ),3)
# pla[1] = round(pla[1]* 100 / (mean_pre ),3)
# pla = dict(zip(list(predictors12m),pla))
# print('anomaly yearly error_list12m', pla)
#
#
#
# #
# uYra12m = uccle12m['rel_anomaly'].values
# regression_output_12m_relanomaly = mzm_regression(uX12m, uYra12m)
# param_list_12m_relanomaly = dict(zip(list(predictors12m), regression_output_12m_relanomaly['gls_results'].params))
# error_list_12manomaly = dict(zip(list(predictors12m), regression_output_12m_relanomaly['gls_results'].bse))
# print('yearly before rel anomaly linear_pre', param_list_12m_relanomaly['linear_pre'])
# print('yearly befire rel anomaly linear_post', param_list_12m_relanomaly['linear_post'])
# pla = regression_output_12m_relanomaly['gls_results'].params
# pla[0] = pla[0]* 100
# pla[1] = pla[1]* 100
# pla = [round(i,3) for i in pla]
# pla = dict(zip(list(predictors12m),pla))
# print('relative anomaly yearly param_list_12m_relanomaly', pla)
# pla = regression_output_12m_relanomaly['gls_results'].bse
# pla[0] = pla[0]* 100
# pla[1] = pla[1]* 100
# pla = [round(i,3) for i in pla]
# pla = dict(zip(list(predictors12m),pla))
# print('relative anomaly yearly error_list_12manomaly', pla)
#
# plotmlr_perkm(uccle12m.index,uY12m,regression_output_12m_anomaly['fit_values'],'Total O3 Yearly Anomaly','TotalOzone_DataModel_yearlyanomaly_notsmoothed_v2')
# plotmlr_perkm(uccle12m.index,uYra12m,regression_output_12m_relanomaly['fit_values'],'Total O3 Yearly Relative Anomaly',
#               'TotalOzone_DataModel_yearly_relativeanomaly_notsmoothed_v2')