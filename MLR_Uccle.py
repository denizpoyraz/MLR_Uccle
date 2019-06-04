from LOTUS_regression.regression import mzm_regression
from LOTUS_regression.predictors import load_data
from LOTUS_regression.predictors.seasonal import add_seasonal_components
import LOTUS_regression.tests as tests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels as sm
from datetime import datetime
from scipy import stats

predictors = load_data('pred_baseline_ilt.csv')
# add the constant term by hand, since it has pre and post constant terms with a gap in the middle

predictors['constant'] = predictors['gap_cons'] +1

const_with_seasons = add_seasonal_components(predictors, {'constant': 4})

uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean.csv',index_col =0)

alt = ['']*36
uY = [0]*36
uc = {}
uct = {}

regression_output = [0]*36
uX = [0]*36

for i in range(36):
    alt[i] = str(i) + 'km'
    uc[i] = uccle[uccle[alt[i]]>0]
    uct[i] = uc[i].loc['1977-02-01':'2017-06-01']
    uY[i] = uct[i][alt[i]].values



print('a', uY[6][0:10])


################################# test code beloew


uccle1 = uccle[uccle['5km']>0]
uccle_time = uccle1.loc['1977-02-01':'2017-06-01']

Y = uccle_time['6km'].values

print(Y[0:10])

# print('Y2', )
# predictors, uccle_time = pd.DataFrame.align(predictors, uccle_time, axis=0)
#
# # (nsamples, npredictors) matrix
# X = predictors.values
#
# # (nsamples) array of observations
# Y = uccle_time['5km'].values
# print('Y',len(Y))
#
# ut = uccle_time.index
#
# regression_output = mzm_regression(X, Y)
#
# param_list =  dict(zip(list(predictors), regression_output['gls_results'].params))
#
# print(param_list)