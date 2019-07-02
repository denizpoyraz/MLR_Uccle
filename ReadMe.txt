Make_DeBiltDF.py  Make_IagosDF.py  Make_UccleDF.py  ->  Codes to read data from Roeland and convert it to a format for me to analyse in a csv file


DeSeasonalize*py -> To deseseasonalize these time series (Uccle, DeBilt, IAGOS)

Extendpredictors.py -> To extend LOTUS ILT time period to Uccle time series period

Add_Preditors.py -> To add new proxies to the ILT model

MLR_Uccle*py  -> To apply the MLR. 
3 models:
-Tropospheric proxies(temp@surface, NOI) do not have any impact.
-Stratospheric proxies:  EA and tropopause pressure are significant for the pre-period, AO and tropopause pressure are significant for the post-period
-Total column: T@100, AO, NAO for the pre-period and EAWR(in the negative direction), NAO, AO for the post-period


