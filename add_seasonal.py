#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[20]:


from LOTUS_regression.regression import mzm_regression
from matplotlib.ticker import AutoMinorLocator
from LOTUS_regression.predictors import load_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import LOTUS_regression.predictors as predictors


# In[115]:


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


print(list(predictors))


predictors = predictors.drop(['date', 'dateindex', 'dateindex_two', 'dateindex_func'], axis=1)


predictors.plot(figsize=(18, 5))
plt.show()


uccle = pd.read_csv('/home/poyraden/Analysis/MLR_Uccle/Files/TO_dobson_monthly.csv')
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

