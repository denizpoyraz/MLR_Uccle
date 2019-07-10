from LOTUS_regression.regression import mzm_regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime



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

    plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/TotalO3/' + plname + '.pdf')
    plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/TotalO3/' + plname + '.eps')
    # plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.pdf')
    # plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/DataModel/' + plname + '.eps')
    # plt.close()
    plt.close()


######################################################################################################################


# part for using extended predictors
pre_name = 'ilt'
plname = 'Trend_' + pre_name
tag = ''

predictors = pd.read_csv('/Volumes/HD3/KMI/MLR_Uccle/Files/Extended_ilt.csv')

# try new predictors
# predictors= pd.read_csv('/Volumes/HD3/KMI/MLR_Uccle/Files/NewPredictors_ilt.csv')

setp = set(predictors['Unnamed: 0'].tolist())

predictors.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
predictors['date'] = pd.to_datetime(predictors['date'], format='%Y-%m')
predictors.set_index('date', inplace=True)

# For Brewer Mast
predictors = predictors.loc['1971-07-01':'2018-12-01']

uccle = pd.read_csv('/Volumes/HD3/KMI/MLR_Uccle/Files/TotalOzone_monthlymean.csv')
uccle['date'] = pd.to_datetime(uccle['date'], format='%Y-%m')
uccle.set_index('date', inplace=True)
uccle['dateindex'] = pd.to_datetime(uccle['dateindex'], format='%Y-%m')



print(uccle.index)


alt = [''] * 36
alt_ds = [''] * 36

uc = {}
uct = {}
ucm = {}

regression_output = [0] * 12
uX = [0] * 12
uY = [0] * 12
param_list = [0] * 12
error_list = [0] * 12
ut = [0] * 12

trend_pre = [0] * 12
trend_pre_err = [0] * 12
trend_post = [0] * 12
trend_post_err = [0] * 12

mY = []

uct_pre = {}
uct_post = {}

mean_pre = [0]*12
mean_post = [0]*12

dfstr = 'rel_anamoly'
mstr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

pre_m = {}

for j in range(12):

    uct[j] = uccle[uccle.index.month == (j + 1)]
    pre_m[j] = predictors[predictors.index.month == (j+1)]


for i in range(12):


    pre_m[i] , uct[i] = pd.DataFrame.align(pre_m[i], uct[i], axis=0)
    # predictors, uct[i] = pd.DataFrame.align(predictors, uct[i], axis=0)

    uY[i] = uct[i][dfstr].values
    # uX[i] = predictors.values
    uX[i] = pre_m[i].values

    if(i == 2):
        print('uY', len(uY[i]))
        print('uX', len(uX[i]))

    regression_output[i] = mzm_regression(uX[i], uY[i])
    param_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].params))
    error_list[i] = dict(zip(list(predictors), regression_output[i]['gls_results'].bse))

    ut[i] = uct[i].index
    ptitle = str(alt[i])
    pname = pre_name + tag + mstr[i]


    # plotmlr_perkm(uct[i].dateindex, regression_output[i]['residual'], regression_output[i]['fit_values'], ptitle, pname)
    plotmlr_perkm(uct[i].dateindex, uY[i], regression_output[i]['fit_values'], ptitle, pname)

    trend_pre[i] = param_list[i]['linear_pre']
    trend_pre_err[i] = error_list[i]['linear_pre']
    trend_post[i] = param_list[i]['linear_post']
    trend_post_err[i] = error_list[i]['linear_post']

    # # for % in decade for relative montly anamoly
    # trend_pre[i] = trend_pre[i] * 100
    # trend_pre_err[i] = 2 * trend_pre_err[i] * 100
    # trend_post[i] = trend_post[i] * 100
    # trend_post_err[i] = 2 * trend_post_err[i] *100

    # for % in years for relative montly anamoly
    trend_pre[i] = trend_pre[i] * 10
    trend_pre_err[i] = 2 * trend_pre_err[i] * 10
    trend_post[i] = trend_post[i] * 10
    trend_post_err[i] = 2 * trend_post_err[i] * 10

print('pre', trend_pre)
print('post', trend_post)

plt.close('all')


# Set the locator
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
fmt = mdates.DateFormatter('%b')


#
fig, ax = plt.subplots()
plt.title('Trend in total O3 over Uccle 1971-2018')
X = plt.gca().xaxis
X.set_major_locator(locator)
# Specify formatter
X.set_major_formatter(fmt)

# plt.xlabel('Ozone trend [%/dec]')
# plt.ylabel('Total ozone trend  [%/dec]')
plt.ylabel('Total ozone trend  [%/yr]')

ax.axhline(y=0, color='grey', linestyle='--')
#
ax.tick_params(axis='both', which='both', direction='in')
ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax.xaxis.set_minor_locator(AutoMinorLocator(5))
# ax.set_xticks([-10,-5,0,5,10])
#


#
eb1 = ax.errorbar(mstr, trend_pre, yerr=trend_pre_err, label='pre-1997', color='red', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb1[-1][0].set_linestyle('--')
eb2 = ax.errorbar(mstr, trend_post, yerr=trend_post_err, label='post-2000', color='limegreen', linewidth=1,
            elinewidth=0.5, capsize=1.5, capthick=1)
eb2[-1][0].set_linestyle('--')


pt = pd.pivot_table(uccle, index=uccle.index.month, columns=uccle.index.year,
                    aggfunc='sum')
pt.columns = pt.columns.droplevel()

ticklabels = [datetime.date(1900, item, 1).strftime('%b') for item in pt.index]

ax.set_xticks(np.arange(0,12))
ax.set_xticklabels(ticklabels) #add monthlabels to the xaxis



ax.legend(loc='upper right', frameon=True, fontsize='small')
plt.show()

#
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle' + plname + '.pdf')
# plt.savefig('/home/poyraden/MLR_Uccle/Plots/Uccle_50years/Uccle' + plname + '.eps')
plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/TotalO3/Trend_monthly_year.pdf')
plt.savefig('/Volumes/HD3/KMI/MLR_Uccle/Plots/TotalO3/Trend_monthly_year.eps')
# plt.close()
