from typing import List, Any

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

def plotmlr_perkm(pX, pY, pRegOutput, pltitle, plname):

    plt.close('all')

    fig, ax = plt.subplots()
    plt.title(pltitle)
    plt.xlabel('Years')
    plt.ylabel('PO3 (hPa)')

    plt.plot(pX, pY, label='Data', color='blue')
    plt.plot(pX, pRegOutput, label='Model', color='orange')

    ax.legend(loc='upper right', frameon=True, fontsize='small')

    plt.savefig('/home/poyraden/MLR_Uccle/Plots/v2/' + plname + '.pdf')
    plt.savefig('/home/poyraden/MLR_Uccle/Plots/v2/' + plname + '.eps')
    plt.close()


######################################################################################################################

#predictors = load_data('pred_baseline_ilt.csv')
predictors = load_data('pred_baseline_pwlt.csv')

pre_name = 'Baseline_pwlt'
plname = 'Trend_' + pre_name
tag = ''


# predictors = pd.read_csv('/home/poyraden/MLR_Uccle/predictors/pred_baseline_ilt.csv')
# add the constant term by hand, since it has pre and post constant terms with a gap in the middle

# seasonalization for ilt_model
#predictors['constant'] = predictors['gap_cons'] + 1
predictors_with_seasons = add_seasonal_components(predictors, {'constant': 4})
#predictors_with_seasons_before = add_seasonal_components(predictors, {'pre_const': 4, 'post_const': 4})
#predictors_with_seasons = add_seasonal_components(predictors, {'pre_const': 4, 'post_const': 4})


# test to check trends if it is due to missing values

# predictors1 =  predictors_with_seasons_before.loc['1977-02-01':'1983-01-01']
# predictors2 =  predictors_with_seasons_before.loc['1985-02-01':'2017-06-01']
# predictors_with_seasons = predictors1.append(predictors2)

#predictors_with_seasons =  predictors_with_seasons_before.loc['1985-02-01':'2017-06-01']


#predictors_with_seasons = add_seasonal_components(predictors, {'constant': 4})

uccle = pd.read_csv('/home/poyraden/MLR_Uccle/Files/1km_monthlymean.csv', index_col=0)

alt = [''] * 36
uc = {}
uct = {}

regression_output = [0] * 36
uX = [0] * 36
uY = [0] * 36
param_list = [0] * 36
error_list = [0] * 36
ut = [0]*36

trend_pre = [0]*36
trend_pre_err = [0]*36
trend_post = [0]*36
trend_post_err = [0]*36

mY = []


for i in range(36):
    mY.append(i)
    alt[i] = str(i) + 'km'
    uc[i] = uccle[uccle[alt[i]] > 0]

    # tmp1 = uc[i].loc['1977-02-01':'1983-01-01']
    # tmp2 = uc[i].loc['1985-02-01':'2017-06-01']
    # uct[i] = tmp1.append(tmp2)


    uct[i] = uc[i].loc['1977-02-01':'2017-06-01']
    #uct[i] = uc[i].loc['1985-02-01': '2017-06-01']

    predictors_with_seasons, uct[i] = pd.DataFrame.align(predictors_with_seasons, uct[i], axis=0)

    uY[i] = uct[i][alt[i]].values
    uX[i] = predictors_with_seasons.values

    print(i, len(uX[i]), len(uY[i]) )


    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors_with_seasons), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors_with_seasons), regression_output[i]['gls_results'].bse))

    ut[i] = uct[i].index
    ptitle = str(alt[i])
    pname = pre_name + tag + str(alt[i])
    if(i == 24): print(i, len(ut[i]), len(uY[i]), len(regression_output[i]))

    #plotmlr_perkm(ut[i], uY[i], regression_output[i]['fit_values'], ptitle, pname)

    trend_pre[i] =  param_list[i]['linear_pre']
    trend_pre_err[i] =  error_list[i]['linear_pre']
    trend_post[i] =  param_list[i]['linear_post']
    trend_post_err[i] = error_list[i]['linear_post']



# plt.close('all')
#
# fig, ax = plt.subplots()
# plt.title('Uccle Lotus Regression Trends')
# plt.xlabel('Ozone Trend (%)')
# plt.ylabel('Altitude (km)')
# plt.xlim(-2,2)
# ax.axvline(x=0, color='grey', linestyle='--')
#
#
# ax.errorbar(trend_pre, mY, xerr= trend_pre_err, label='pre-1997', color='black', linewidth=1,
#             elinewidth=0.5, capsize=1, capthick=0.5)
# ax.errorbar(trend_post, mY, xerr= trend_post_err, label='post-2000', color='green', linewidth=1,
#             elinewidth=0.5, capsize=1, capthick=0.5)
# ax.legend(loc='upper right', frameon=True, fontsize='small')
#
#
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/v2/' + plname + '.pdf')
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/v2/' + plname + '.eps')
# plt.close()