from LOTUS_regression.regression import mzm_regression
from matplotlib.ticker import AutoMinorLocator
from LOTUS_regression.predictors import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import LOTUS_regression.predictors as predictors

def add_seasonal_components(basis_df, num_components):
    for column in basis_df:
        n_harmonic = num_components.get(column, 0)

        for i in range(n_harmonic):
            basis_df[column + '_sin' + str(i)] = basis_df[column] * np.sin(2*np.pi * (basis_df.dateindex_func.dt.dayofyear-1) / 365.25 * (i+1))
            basis_df[column + '_cos' + str(i)] = basis_df[column] * np.cos(2*np.pi * (basis_df.dateindex_func.dt.dayofyear-1) / 365.25 * (i+1))

    return basis_df




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
predictors['dateindex_func'] = pd.to_datetime(predictors['date'], format='%Y-%m-%d')

predictors['dindex'] = predictors['dateindex_two'].dt.date.apply(lambda x: x.strftime('%Y-%m'))

predictors = add_seasonal_components(predictors, {'pre_const': 4, 'post_const': 4 })
predictors.set_index('dindex', inplace=True)

predictors = predictors.loc['1972-01':'2018-12']
l2 = predictors.dateindex.tolist()


print('l2', l2[0:5])

predictors12m = predictors.resample('12M',on='dateindex_two').mean()
predictors12m['dateindex'] = pd.to_datetime(predictors12m.index, format='%Y-%m')
predictors12m['dindex'] = predictors12m.dateindex.dt.date.apply(lambda x: x.strftime('%Y-%m'))
l2_12m = predictors12m.dindex.tolist()
print('l2 12m', l2_12m[0:5])

# predictors = predictors.drop(['dateindex'], axis =1)

uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_monthly.csv')
uccle = uccle[(uccle.Date < '2019-01-01') & (uccle.Date >= '1972-01-01')]
print(uccle.Date.min(), uccle.Date.max())


uccle['dateindex'] = pd.to_datetime(uccle['Date'], format='%Y-%m-%d')
uccle['dindex'] = uccle['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
uccle['dateindex_two'] = uccle['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
uccle.set_index('dindex', inplace=True)
l1 = uccle['dateindex_two'].tolist()
print('l1', l1)


# uccle.set_index('date', inplace=True)
uccle12m = uccle.resample('12M', on='dateindex').mean()
uccle12m['dateindex'] = pd.to_datetime(uccle12m.index, format='%Y-%m')
uccle12m['dindex'] = uccle12m.dateindex.dt.date.apply(lambda x: x.strftime('%Y-%m'))
l1_12m = uccle12m.dindex.tolist()

print('l1_12m', l1_12m[0:5])


common_dates12 = list(set(l1).intersection(set(l2)))
uccle = uccle[uccle.index.isin(common_dates12)]
predictors = predictors[predictors.index.isin(common_dates12)]

# common_dates12m = list(set(l1_12m).intersection(set(l2_12m)))
# uccle12m = uccle12m[uccle12m.dindex.isin(common_dates12m)]
# predictors12m = predictors12m[predictors12m.dindex.isin(common_dates12m)]

print(len(predictors), len(predictors12m))
print(len(uccle), len(uccle12m))


#
predictors, uccle = pd.DataFrame.align(predictors, uccle, axis=0)
# predictors12m, uccle12m = pd.DataFrame.align(predictors12m, uccle12m, axis=0)

print(len(predictors), len(predictors12m))
print(len(uccle), len(uccle12m))
#
# predictors = predictors.drop(['date' ,'dateindex_two','dateindex'],axis=1)
# predictors12m = predictors12m.drop(['dindex','dateindex'],axis=1)


#
#
uY = uccle['TO'].values
uX = predictors.values
regression_output = mzm_regression(uX, uY)
param_list = dict(zip(list(predictors), regression_output['gls_results'].params))
error_list = dict(zip(list(predictors), regression_output['gls_results'].bse))
pl = regression_output['gls_results'].params
pl = [round(i, 3) for i in pl]
pl = dict(zip(list(predictors),pl))
# print('pl', pl)
print('param_list',pl)
# print('predictors', predictors[0:3])
pl = regression_output['gls_results'].bse
pl = [round(i, 3) for i in pl]
pl = dict(zip(list(predictors),pl))
# print('pl', pl)
print('error_list',pl)

plotmlr_perkm(uccle.dateindex,uY,regression_output['fit_values'],'Total O3 Monthly Means','TotalOzone_totalcolumnilt_monthly_otherpredictor')




# #
# uYra = uccle['anomaly'].values
# regression_output_anomaly = mzm_regression(uX, uYra)
# param_list_anomaly = dict(zip(list(predictors), regression_output_anomaly['gls_results'].params))
# error_list_anomaly = dict(zip(list(predictors), regression_output_anomaly['gls_results'].bse))
#
# pla = regression_output_anomaly['gls_results'].params
# pla = [round(i, 3) for i in pla]
# pla = dict(zip(list(predictors),pla))
# # print('pl', pl)
# # print('param_list',pl)
#
# print('param_list_anomaly', pla)
# pla = regression_output_anomaly['gls_results'].bse
# pla = [round(i, 3) for i in pla]
# pla = dict(zip(list(predictors),pla))
# print('error_list_anomaly', pla)
#
#
# #
# #
# uY12m = uccle12m['TO'].values
# uX12m = predictors12m.values
# regression_output_12m = mzm_regression(uX12m, uY12m)
# param_list_12m = dict(zip(list(predictors12m), regression_output_12m['gls_results'].params))
# error_list_12m = dict(zip(list(predictors12m), regression_output_12m['gls_results'].bse))
#
# pla = regression_output_12m['gls_results'].params
# pla = [round(i,3) for i in pla]
# pla = dict(zip(list(predictors12m),pla))
# print('param_list12m', pla)
# pla = regression_output_12m['gls_results'].bse
# pla = [round(i,3) for i in pla]
# pla = dict(zip(list(predictors12m),pla))
# print('error_list12m', pla)
#
# #
# uYra12m = uccle12m['anomaly'].values
# regression_output_12manomaly = mzm_regression(uX12m, uYra12m)
# param_list_12manomaly = dict(zip(list(predictors12m), regression_output_12manomaly['gls_results'].params))
# error_list_12manomaly = dict(zip(list(predictors12m), regression_output_12manomaly['gls_results'].bse))
#
# pla = regression_output_12manomaly['gls_results'].params
# pla = [round(i,3) for i in pla]
# pla = dict(zip(list(predictors12m),pla))
# print('param_list_12manomaly', pla)
# pla = regression_output_12manomaly['gls_results'].bse
# pla = [round(i,3) for i in pla]
# pla = dict(zip(list(predictors12m),pla))
# print('error_list_12manomaly', pla)
#
# trend_pre=param_list['linear_pre']
# trend_post=param_list['linear_post']
#
# # fig, (ax1, ax2) = plt.subplots(2)
# # fig.suptitle('Monthly predictors')
# # # predictors[['solar', 'enso']].plot(figsize=(16, 6))
# #
# # # plt.plot(uccle12m.index, uccle12m['mean'])
# # ax1.plot(predictors.index, predictors['linear_pre'])
# # ax1.plot(predictors.index, predictors['linear_post'])
# # ax1.set_title('Predictors')
# #
# # ax2.plot(predictors.index, (trend_pre * predictors['linear_pre'])+ param_list['pre_const'])
# # ax2.plot(predictors.index, (trend_post * predictors['linear_post']) + param_list['post_const'])
# # ax2.set_title('Fitted Predictors')
# # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/Monthly_PrePost_Predictors.pdf')
# # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/Monthly_PrePost_Predictors.png')
# # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/Monthly_PrePost_Predictors.eps')
# #
# # plt.show()
# # plt.close()
#
# trend_pre_anomaly=param_list_anomaly['linear_pre']
# trend_post_anomaly=param_list_anomaly['linear_post']
#
# trend_pre_12m=param_list_12m['linear_pre']
# trend_post_12m=param_list_12m['linear_post']
#
# # fig, (ax1, ax2) = plt.subplots(2)
# # fig.suptitle('Yearly predictors')
# # # predictors[['solar', 'enso']].plot(figsize=(16, 6))
# #
# # # plt.plot(uccle12m.index, uccle12m['mean'])
# # ax1.plot(predictors12m.index, predictors12m['linear_pre'])
# # ax1.plot(predictors12m.index, predictors12m['linear_post'])
# # ax1.set_title('Predictors')
# #
# # ax2.plot(predictors12m.index, (trend_pre_12m * predictors12m['linear_pre'])+ param_list_12m['pre_const'])
# # ax2.plot(predictors12m.index, (trend_post_12m * predictors12m['linear_post']) + param_list_12m['post_const'])
# # ax2.set_title('Fitted Predictors')
# # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/Yearly_PrePost_Predictors.pdf')
# # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/Yearly_PrePost_Predictors.png')
# # plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/Yearly_PrePost_Predictors.eps')
# #
# # plt.show()
# # plt.close()
#
#
# trend_pre_12manomaly=param_list_12manomaly['linear_pre']
# trend_post_12manomaly=param_list_12manomaly['linear_post']
#
# print('here', list(predictors12m))
# print('here 2', predictors12m[0:2])
#
# plotmlr_perkm(uccle.dateindex,uYra,regression_output_anomaly['fit_values'],'Total O3 Monthly Anomaly','TotalOzone_totalcolumnilt_monthlyanomaly_otherpredictor')
#
# plotmlr_perkm(uccle12m.index,uY12m,regression_output_12m['fit_values'],'Total O3 Yearly Means','TotalOzone_totalcolumnilt_yearly_otherpredictor')
# plotmlr_perkm(uccle12m.index,uYra12m,regression_output_12manomaly['fit_values'],'Total O3 Yearly Anomaly','TotalOzone_totalcolumnilt_yearlyanomaly_otherpredictor')
#
#
#
# #Monthly
# # test = predictors12m[predictors12m.index < '1998-07-31']['linear_pre'].tolist()
# pretrend = predictors[predictors.index < '1998-07-31']['linear_pre'].tolist()
# # pretrend = predictors['linear_pre'].tolist()
# pretrendm = [i * trend_pre_anomaly for i in pretrend]
# pre_const = param_list_anomaly['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# # print('pretrend', len(pretrendmp), pretrendmp)
#
# posttrend = predictors[predictors.index > '1999-07-31']['linear_post'].tolist()
# posttrendm = [i * trend_post_anomaly for i in posttrend]
# post_const = param_list_anomaly['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=365))   #to get a tick every 15 minutes
# # ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
#
# plt.plot(uccle.index, uccle['anomaly'], color = '#1f77b4', label = 'Total ozone anomaly')
# plt.plot(predictors[predictors.index < '1998-07-31'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors[predictors.index > '1999-07-31'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# # ax.set_xticklabels(360, rotation=0)
#
# # fmt_half_year = mdates.MonthLocator(interval=12)
# # ax.xaxis.set_major_locator(fmt_half_year)
#
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_otherpredictor.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_otherpredictor.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_monthly_otherpredictor.eps')
#
# plt.show()
# plt.close()
# #
# pretrend = predictors[predictors.index < '1998-07-31']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre for i in pretrend]
# pre_const = param_list['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors[predictors.index > '1999-07-31']['linear_post'].tolist()
# posttrendm = [i * trend_post for i in posttrend]
# post_const = param_list['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
# ax.xaxis.set_major_locator(mdates.YearLocator(4))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
#
# plt.plot(uccle.index, uccle['TO'], color = '#1f77b4', label = 'Total Ozone (DU)')
# plt.plot(predictors[predictors.index < '1998-07-31'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors[predictors.index > '1999-07-31'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_otherpredictor.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_otherpredictor.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_otherpredictor.eps')
#
# plt.show()
# plt.close()
# #
# #
# #
# # ## Yearly
# #
# pretrend = predictors12m[predictors12m.index < '1998-07-31']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_12manomaly for i in pretrend]
# pre_const = param_list_12manomaly['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# # print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors12m[predictors12m.index > '1999-07-31']['linear_post'].tolist()
# # posttrend = predictors12m['linear_post'].tolist()
# posttrendm = [i * trend_post_12manomaly for i in posttrend]
# post_const = param_list_12manomaly['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
#
# # ax.set_xlim(1971, 2019)
# ax.xaxis.set_major_locator(mdates.YearLocator(5))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
# plt.plot(uccle12m.index, uccle12m['anomaly'], color = '#1f77b4', label = 'Total ozone anomaly')
# # plt.plot(predictors12m.index, pretrendmp, label = 'ILT pre', color = '#d62728')
# # plt.plot(predictors12m.index ,posttrendmp, label = 'ILT post', color = '#2ca02c')
# plt.plot(predictors12m[predictors12m.index < '1998-07-31'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors12m[predictors12m.index > '1999-07-31'].index,posttrendmp, label = 'ILT post',  color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m_t2_otherpredictor.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m_t2_otherpredictor.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m_t2_otherpredictor.eps')
#
# plt.show()
# plt.close()
#
#
# pretrend = predictors12m[predictors12m.index < '1998-07-31']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_12m for i in pretrend]
# pre_const = param_list_12m['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors12m[predictors12m.index > '1999-07-31']['linear_post'].tolist()
# posttrendm = [i * trend_post_12m for i in posttrend]
# post_const = param_list_12m['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
# ax.xaxis.set_major_locator(mdates.YearLocator(4))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes
#
# plt.plot(uccle12m.index, uccle12m['TO'], color = '#1f77b4', label = 'Total Ozone (DU)')
# plt.plot(predictors12m[predictors12m.index < '1998-07-31'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors12m[predictors12m.index > '1999-07-31'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m_otherpredictor.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m_otherpredictor.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m_otherpredictor.eps')
#
# plt.show()
# plt.close()


####################################################################################################################################################################

# ## Yearly
#
# pretrend = predictors12m[predictors12m.index < '1998-07-31']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_12manomaly for i in pretrend]
# pre_const = param_list_12manomaly['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# # print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors12m[predictors12m.index > '1999-07-31']['linear_post'].tolist()
# posttrendm = [i * trend_post_12manomaly for i in posttrend]
# post_const = param_list_12manomaly['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
# plt.plot(uccle12m.index, uccle12m['anomaly'], color = '#1f77b4', label = 'Total ozone anomaly')
# plt.plot(predictors12m[predictors12m.index < '1998-07-31'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors12m[predictors12m.index > '1999-07-31'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_anomaly_12m.eps')
#
# plt.show()
# plt.close()
#
#
# pretrend = predictors12m[predictors12m.index < '1998-07-31']['linear_pre'].tolist()
# # pretrend = predictors12m['linear_pre'].tolist()
# pretrendm = [i * trend_pre_12m for i in pretrend]
# pre_const = param_list_12m['pre_const']
# pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)
# # print(predictors12m['linear_pre'])
# # print(predictors12m['linear_post'])
# posttrend = predictors12m[predictors12m.index > '1999-07-31']['linear_post'].tolist()
# posttrendm = [i * trend_post_12m for i in posttrend]
# post_const = param_list_12m['post_const']
# posttrendmp = [i + post_const for i in posttrendm]
#
# fig, ax = plt.subplots()
#
# plt.plot(uccle12m.index, uccle12m['TO'], color = '#1f77b4', label = 'Total Ozone (DU)')
# plt.plot(predictors12m[predictors12m.index < '1998-07-31'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
# plt.plot(predictors12m[predictors12m.index > '1999-07-31'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
# ax.legend(loc='lower right', frameon=False, fontsize='small')
#
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m.pdf')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m.png')
# plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_12m.eps')
#
# plt.show()
# plt.close()
#
# #
#


# plotmlr_perkm(uccle.dateindex,uYra,regression_output['fit_values'],'Total O3 Monthly Means','TotalOzone_totalcolumnilt')
#
# plotresidual(uccle.dateindex,regression_output['residual'],'residualmean','Residual_TotalOzone_totalcoulumnilt')
#

#
# trend_pre=param_list['linear_pre']
# trend_pre_err=error_list['linear_pre']
# trend_post=param_list['linear_post']
# trend_post_err=error_list['linear_post']
#
# trend_pre_12m=param_list12m['linear_pre']
# trend_post_12m=param_list12m['linear_post']
#
# plist = ['linear_pre', 'linear_post', 'post_const', 'pre_const', 'gap_const', 'enso', 'qboA', 'qboB', 'solar', 'AOD',
#          'AO', 'pre_tropop', 'temp_100', 'temp_500', 'EAWR', 'NAO']
#
# print('first monthly, second yearly')
# for k in plist :
#     print(k, round(param_list[k],2), round(param_list12m[k],2))
#
#
# # #
#
# print('trend_pre', trend_pre, ' err', trend_pre_err)
# print('trend_post', trend_post, ' err', trend_post_err)
#
# print('trend_pre_12m', trend_pre_12m, ' err', trend_pre_err)
# print('trend_post_12m', trend_post_12m, ' err', trend_post_err)
#
# print('yearly')
# print('pre', trend_pre/10)
# print('post', trend_post/10)
#
# print('monthl;y')
# print('pre', trend_pre/120)
# print('post', trend_post/120)
#
#
# fig, ax = plt.subplots()
#
# # predictors[['solar', 'enso']].plot(figsize=(16, 6))
#
# # plt.plot(uccle12m.index, uccle12m['mean'])
# plt.plot(predictors12m.index, trend_pre_12m * predictors12m['linear_pre'])
# plt.plot(predictors12m.index, trend_post_12m * predictors12m['linear_post'])
#
#
# plt.show()
# plt.close()

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

# print('decade rel anomaly')
# print('pre', trend_prera * 100)
# print('post', trend_postra * 100)
#
# print('month rel anomaly')
# print('pre', trend_prera/120)
# print('post', trend_postra/120 )

# didx = pd.DatetimeIndex(start ='1971-07-01', end = '2018-12-01', freq ='MS')
#
# print('year', didx.year)
# relative anomaly
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


# plt.show()
#
# # plt.plot(uccle.dateindex,regression_output['fit_values'],label='Model',color='black',linewidth=0.75)
# # plt.plot(x,y)
# # plt.plot(uccle.dateindex, y ,label='Model',color='red',linewidth=0.75)
#
#
# # plt.plot(didx.year,y)
#


#
#
# fig, ax = plt.subplots(2, sharex=True, sharey=False, gridspec_kw={'hspace': 0})# plt.plot(uccle.index, uccle['mean'])
# fig.suptitle('Monthly TO and anomalies')
# ax[1].plot(uccle.dateindex_two, uccle['anomaly'])
# ax[0].plot(uccle.dateindex_two, uccle['TO'])
#
# plt.show()
# plt.close()

# fig, ax = plt.subplots(2, sharex=True, sharey=False, gridspec_kw={'hspace': 0})# plt.plot(uccle.index, uccle['mean'])
# fig.suptitle('Yearly TO and anomalies')
# ax[0].plot(uccle12m.index, uccle12m['TO'])
# ax[1].plot(uccle12m.index, uccle12m['anomaly'])
# plt.show()
# plt.close()
# predictors[['linear_pre', 'linear_post']].plot(figsize=(16, 6))