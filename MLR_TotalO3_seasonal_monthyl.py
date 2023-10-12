#!/usr/bin/env python

from LOTUS_regression.regression import mzm_regression
from matplotlib.ticker import AutoMinorLocator
from LOTUS_regression.predictors import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import LOTUS_regression.predictors as predictors
import matplotlib.dates as mdates



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


def add_seasonal_components(basis_df, num_components):
    for column in basis_df:
        n_harmonic = num_components.get(column, 0)

        for i in range(n_harmonic):
            basis_df[column + '_sin' + str(i)] = basis_df[column] * np.sin(2*np.pi * (basis_df.dateindex_func.dt.dayofyear-1) / 365.25 * (i+1))
            basis_df[column + '_cos' + str(i)] = basis_df[column] * np.cos(2*np.pi * (basis_df.dateindex_func.dt.dayofyear-1) / 365.25 * (i+1))

    return basis_df


# In[ ]:





# In[116]:


predictors = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/Extended_ilt.csv')


predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['dateindex'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors['dateindex'] = predictors['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))

predictors['dateindex_two'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors['dateindex_func'] = pd.to_datetime(predictors['date'], format='%Y-%m-%d')

predictors['dindex'] = predictors['dateindex_two'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
predictors = add_seasonal_components(predictors, {'pre_const': 4, 'post_const':4, 'gap_const':4 })
# print('after', predictors[0:3])
predictors.set_index('dindex', inplace=True)

predictors = predictors.loc['1972-01':'2018-12']



l2 = predictors.dateindex.tolist()

predictors = predictors.drop(['date', 'dateindex', 'dateindex_two', 'dateindex_func'], axis=1)

print(list(predictors))

predictors = predictors.drop(['enso', 'qboA', 'qboB',
                              'solar', 'AOD', 'post_const_sin0', 'post_const_cos0', 'post_const_sin1', 'post_const_cos1',
                              'post_const_sin2', 'post_const_cos2', 'post_const_sin3', 'post_const_cos3', 'pre_const_sin0',
                              'pre_const_cos0', 'pre_const_sin1', 'pre_const_cos1', 'pre_const_sin2', 'pre_const_cos2',
                              'pre_const_sin3', 'pre_const_cos3', 'gap_const_sin0', 'gap_const_cos0', 'gap_const_sin1',
                              'gap_const_cos1', 'gap_const_sin2', 'gap_const_cos2', 'gap_const_sin3', 'gap_const_cos3'], axis=1)


predictors.plot(figsize=(18, 5))
plt.show()


uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_monthly.csv')
# uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_smoothed.csv')

print(uccle[0:3])

uccle = uccle[(uccle.Date < '2019-01-01') & (uccle.Date >= '1972-01-01')]
print(uccle.Date.min(), uccle.Date.max())


uccle['dateindex'] = pd.to_datetime(uccle['Date'], format='%Y-%m-%d')
uccle['dindex'] = uccle['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
uccle['dateindex_two'] = uccle['dateindex'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
uccle.set_index('dindex', inplace=True)

l1 = uccle['dateindex_two'].tolist()

uccle_pre = uccle.loc['1971-12-01':'1996-12-01']
uccle_post = uccle.loc['2000-01-01':'2018-12-01']

mean_pre = np.nanmean(uccle_pre['TO'].values)
mean_post = np.nanmean(uccle_post['TO'].values)



# In[123]:


common_dates12 = list(set(l1).intersection(set(l2)))
uccle = uccle[uccle.index.isin(common_dates12)]
predictors = predictors[predictors.index.isin(common_dates12)]


predictors, uccle = pd.DataFrame.align(predictors, uccle, axis=0)



uY = uccle['TO'].values
uX = predictors.values
regression_output = mzm_regression(uX, uY)
param_list = dict(zip(list(predictors), regression_output['gls_results'].params))
error_list = dict(zip(list(predictors), regression_output['gls_results'].bse))
pl = regression_output['gls_results'].params
pl[0] = round(pl[0]* 100 / (mean_pre ),3)
pl[1] = round(pl[1]* 100 / (mean_pre ),3)
pl = [round(i, 3) for i in pl]
pl = dict(zip(list(predictors),pl))
# print('pl', pl)
print('param_list',pl)
# print('predictors', predictors[0:3])
pl = regression_output['gls_results'].bse
pl[0] = round(pl[0]* 100 / (mean_pre ),3)
pl[1] = round(pl[1]* 100 / (mean_pre ),3)
pl = [round(i, 3) for i in pl]
pl = dict(zip(list(predictors),pl))
# print('pl', pl)
print('error_list',pl)


plotmlr_perkm(uccle.dateindex,uY,regression_output['fit_values'],'Total O3 Monthly Means','TotalOzone_monthly_mean_onlyilt')

trend_pre=param_list['linear_pre'] * 100 / mean_pre
trend_post=param_list['linear_post'] * 100 / mean_post

trend_pre=param_list['linear_pre']
trend_post=param_list['linear_post']

print('monthly trends anomaly', trend_pre, trend_post)

#Monthly
# test = predictors12m[predictors12m.index < '1997-01-01']['linear_pre'].tolist()
pretrend = predictors[predictors.index < '1997-01-01']['linear_pre'].tolist()
# pretrend = predictors['linear_pre'].tolist()
pretrendm = [i * trend_pre for i in pretrend]
pre_const = param_list['pre_const']
pretrendmp = [i + pre_const for i in pretrendm]
# print('pretrend', len(pretrendmp), pretrendmp)

posttrend = predictors[predictors.index > '2000-01-01']['linear_post'].tolist()
posttrendm = [i * trend_post for i in posttrend]
post_const = param_list['post_const']
posttrendmp = [i + post_const for i in posttrendm]

fig, ax = plt.subplots()

ax.xaxis.set_major_locator(mdates.DayLocator(interval=365))   #to get a tick every 15 minutes
# ax.xaxis.set_minor_locator(mdates.YearLocator(1))   #to get a tick every 15 minutes

plt.plot(uccle.index, uccle['TO'], color = '#1f77b4', label = 'Total ozone monthly means')
plt.plot(predictors[predictors.index < '1997-01-01'].index, pretrendmp, label = 'ILT pre', color = '#d62728')
plt.plot(predictors[predictors.index > '2000-01-01'].index,posttrendmp, label = 'ILT post', color = '#2ca02c')
ax.legend(loc='lower right', frameon=False, fontsize='small')

# ax.set_xticklabels(360, rotation=0)

# fmt_half_year = mdates.MonthLocator(interval=12)
# ax.xaxis.set_major_locator(fmt_half_year)


plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_trend_onlyilt.pdf')
plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_trend_onlyilt.png')
plt.savefig('/home/poyraden/Analysis/MLR_Uccle/Plots/Paper_Reviews/TO_monthly_trend_onlyilt.eps')

plt.show()
plt.close()
