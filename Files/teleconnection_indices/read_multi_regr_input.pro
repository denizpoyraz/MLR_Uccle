PRO read_noaa

; reads the following data in ~/fileserver/home/multiregression:
; qbo_data.txt, nao_data.txt, enso_data.txt, enso_MEI_data.txt, enso_BEST_data.txt and solar_data.txt
; data downloaded from http://www.esrl.noaa.gov/psd/data/climateindices/

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/enso_MEI_data2018UPDATE.txt'

close,1
n=10000
i=0
year=intarr(n)
qbo=fltarr(n)
months=fltarr(12)
month=fltarr(n)
JD=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	readf,1,yearin,qbo01,qbo02,qbo03,qbo04,qbo05,$
	        qbo06,qbo07,qbo08,qbo09,qbo10,qbo11,qbo12;,$
;                format='(I4,F9.3,11F8.3)'
	months[0]=qbo01
	months[1]=qbo02
	months[2]=qbo03
	months[3]=qbo04
	months[4]=qbo05
	months[5]=qbo06
	months[6]=qbo07
	months[7]=qbo08
	months[8]=qbo09
	months[9]=qbo10
	months[10]=qbo11
	months[11]=qbo12	
	mteller=0
	while (mteller lt 12) do begin
  		year[i]=yearin
		month[i]=mteller+1
		qbo[i]=months[mteller]
		JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
		mteller=mteller+1
		i=i+1
	endwhile
endwhile
close,1

idx=where(year ne 0. and qbo gt -90)
enso_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],enso:qbo[idx]}
save,enso_noaa,filename='~/fileserver/home/ARCHIVE_roeland/multiregression/ENSO_MEI2018update.sav'

END

;************************************************************************

PRO read_noaa_daily

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/AAO2018.txt'

close,1
n=30000
i=0
year=intarr(n)
index=fltarr(n)
month=fltarr(n)
day=fltarr(n)
JD=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	readf,1,yearin,monthin,dayin,indexin
	year[i]=yearin
	month[i]=monthin
	day[i]=dayin
	index[i]=indexin
	JD[i]=JULDAY(double(month[i]),double(day[i]),double(year[i]))
	i=i+1
endwhile
close,1

idx=where(year ne 0. and index gt -90)
AAO_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],DD:day[idx],AAO:index[idx]}
save,AAO_noaa,filename='~/fileserver/home/ARCHIVE_roeland/multiregression/AAO_noaa2018.sav'

END

;************************************************************************

PRO read_noaa_monthly

restore,'~/fileserver/home/ARCHIVE_roeland/multiregression/monthly_naootempl.sav'

pna_raw=read_ascii('~/fileserver/home/multiregression/norm.pna.monthly.b5001.current.ascii',template=monthly_naootempl)
n=n_elements(pna_raw.year)
JD=dblarr(n)
FOR i=0,n-1 DO JD[i]=JULDAY(pna_raw.month[i],15.,pna_raw.year[i])
pna_noaa={JD:JD,MM:pna_raw.month,YYYY:pna_raw.year,pna:pna_raw.index}
save,pna_noaa,filename='~/fileserver/home/ARCHIVE_roeland/multiregression/pna_noaa2.sav'

END

;************************************************************************

PRO read_maxUV_daily

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/maxuv_016.txt'

close,1
n=30000
i=0
year=intarr(n)
UVindex=fltarr(n)
month=fltarr(n)
day=fltarr(n)
doy=intarr(n)
hour=intarr(n)
minutes=intarr(n)
sec=intarr(n)
JD=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	readf,1,yearin,monthin,dayin,doyin,hourin,minutesin,secin,UVindexin
	year[i]=yearin
	month[i]=monthin
	day[i]=dayin
	UVindex[i]=UVindexin
	JD[i]=JULDAY(double(month[i]),double(day[i]),double(year[i]))
	i=i+1
endwhile
close,1

idx=where(year ne 0. and UVindex gt -90)
UV={MM:month[idx],YYYY:year[idx],JD:JD[idx],DD:day[idx],UV:UVindex[idx]}
save,UV,filename='~/fileserver/home/ARCHIVE_roeland/multiregression/UV.sav'

END

;************************************************************************

PRO read_monthly_solflux

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/solflux_monthly_average2018.txt'

close,1
n=2000
i=0
year=intarr(n)
obsflux=dblarr(n)
adjflux=dblarr(n)
absflux=dblarr(n)
month=fltarr(n)
day=fltarr(n)
JD=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	readf,1,yearin,monthin,obsfluxin,adjfluxin,absfluxin
	year[i]=yearin
	month[i]=monthin
	obsflux[i]=obsfluxin
	adjflux[i]=adjfluxin
	absflux[i]=absfluxin
	JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
	i=i+1
endwhile
close,1

idx=where(year ne 0.)
sun={MM:month[idx],YYYY:year[idx],JD:JD[idx],obsflux:obsflux[idx],adjflux:adjflux[idx],absflux:absflux[idx]}
save,sun,filename='~/fileserver/home/ARCHIVE_roeland/multiregression/solarflux2018.sav'

END


PRO read_teleconnection_indices


homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/tele_index_nh2018.txt'
i=0
n=1000
close,1
year=intarr(n)
month=intarr(n)
jd=dblarr(n)
nao=fltarr(n)
ea=fltarr(n)
wp=fltarr(n)
epnp=fltarr(n)
pna=fltarr(n)
eawr=fltarr(n)
sca=fltarr(n)
tnh=fltarr(n)
pol=fltarr(n)
pt=fltarr(n)
openr,1,filename
while not(eof(1)) do begin
	readf,1,yearin,monthin,val01,val02,val03,val04,val05,$
	        val06,val07,val08,val09,val10,val11,$
		format='(I4,I3,F7.2,9F6.2,F7.1)'
	year[i]=yearin
	month[i]=monthin
	JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
	ea[i]=val02
	wp[i]=val03
	epnp[i]=val04
	pna[i]=val05
	eawr[i]=val06
	sca[i]=val07
	tnh[i]=val08
	pol[i]=val09
	pt[i]=val10
	i=i+1
endwhile
close,1
idx=where(year ne 0)
ea_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],ea:ea[idx]}
wp_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],wp:wp[idx]}
epnp_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],epnp:epnp[idx]}
pna_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],pna:pna[idx]}
eawr_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],eawr:eawr[idx]}
sca_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],sca:sca[idx]}
tnh_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],tnh:tnh[idx]}
pol_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],pol:pol[idx]}
pt_noaa={MM:month[idx],YYYY:year[idx],JD:JD[idx],pt:pt[idx]}

save,ea_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/ea_noaa2018.sav'
save,wp_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/wp_noaa2018.sav'
save,epnp_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/epnp_noaa2018.sav'
save,pna_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/pna_noaa2018.sav'
save,eawr_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/eawr_noaa2018.sav'
save,sca_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/sca_noaa2018.sav'
save,tnh_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/tnh_noaa2018.sav'
save,pol_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/pol_noaa2018.sav'
save,pt_noaa,filename=homedir+'/home/ARCHIVE_roeland/multiregression/pt_noaa2018.sav'

END

;************************************************************************

PRO read_stratAER_map_netcdf

;.run ~/fileserver/home/idl/lib/ncdf_data_define.pro
;.run ~/fileserver/home/idl/lib/ncdf_browser.pro
;!PATH = Expand_Path('+~/fileserver/home/idl/lib/coyoteprograms/') + ':' + !PATH

file='fileserver/home/multiregression/stratAER_map.nc'

cdf = Obj_New('NCDF_DATA', file)
lat = cdf -> ReadVariable('lat')
month = cdf -> ReadVariable('month')
aod = cdf -> ReadVariable('reff')

Obj_Destroy, cdf

END

;************************************************************************

PRO read_strat_aer

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/STRATAER.txt'

ind = 19  ; this corresponds to the 50°NB latitude
i=0

close,1
n=5000
year=intarr(n)
yearin=0
aod=fltarr(n)
months=fltarr(12)
month=fltarr(n)
JD=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	char = ' '
	readf, 1, char, index, val1, val2, val3, val4, val5, val6, $
	       val7, val8, val9, val10, val11, val12, format='(A5,I3,12F6.4)'
	if index eq 27 then yearin=fix(char)
	if index eq ind then begin
		months[0]=val1
		months[1]=val2
		months[2]=val3
		months[3]=val4
		months[4]=val5
		months[5]=val6
		months[6]=val7
		months[7]=val8
		months[8]=val9
		months[9]=val10
		months[10]=val11
		months[11]=val12
		mteller=0
		while (mteller lt 12) do begin
  			year[i]=yearin
			month[i]=mteller+1
			aod[i]=months[mteller]
			JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
			mteller=mteller+1
			i=i+1
		endwhile
		print,i
	endif	
endwhile	

close,1

idx=where(year ne 0. and aod ne -999.)
strataer={MM:month[idx],YYYY:year[idx],JD:JD[idx],aod:aod[idx]}
save,strataer,filename=homedir+'/home/ARCHIVE_roeland/multiregression/strataer.sav'

END

;************************************************************************

PRO read_AOD_tau

homedir = STRING(getenv("HOME")) + '/fileserver'
filename1 = homedir + '/home/multiregression/AOD_tau_map_15to20km.txt
filename2 = homedir + '/home/multiregression/AOD_tau_map_20to25km.txt
filename3 = homedir + '/home/multiregression/AOD_tau_map_25to30km.txt
filename4 = homedir + '/home/multiregression/AOD_tau_map_30to35km.txt


i=0

close,1
n=2000
year=intarr(n)
yearin=0
aod=fltarr(n)
months=fltarr(12)
month=fltarr(n)
JD=dblarr(n)
openr,1,filename1
while not(eof(1)) do begin
	char = ' '
	readf, 1, char, lat, val1, val2, val3, val4, val5, val6, $
	       val7, val8, val9, val10, val11, val12, format='(A4,F5.1,12F7.4)'
	if lat gt 85 then yearin=fix(char)
	if (lat lt 52 AND lat gt 48) then begin
		months[0]=val1
		months[1]=val2
		months[2]=val3
		months[3]=val4
		months[4]=val5
		months[5]=val6
		months[6]=val7
		months[7]=val8
		months[8]=val9
		months[9]=val10
		months[10]=val11
		months[11]=val12
		mteller=0
		while (mteller lt 12) do begin
  			year[i]=yearin
			month[i]=mteller+1
			aod[i]=months[mteller]
			JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
			mteller=mteller+1
			i=i+1
		endwhile
	endif	
endwhile	

close,1

idx=where(year ne 0. and aod ne -999.)
aant=n_elements(idx)
aod[idx[aant-3:aant-1]]=aod[idx[aant-4]]
AOD15to20={MM:month[idx],YYYY:year[idx],JD:JD[idx],aod:aod[idx]}

; -----------------------------------------------------------

i=0
year=intarr(n)
yearin=0
aod=fltarr(n)
months=fltarr(12)
month=fltarr(n)
JD=dblarr(n)
openr,2,filename2
while not(eof(2)) do begin
	char = ' '
	readf, 2, char, lat, val1, val2, val3, val4, val5, val6, $
	       val7, val8, val9, val10, val11, val12, format='(A4,F5.1,12F7.4)'
	if lat gt 85 then yearin=fix(char)
	if (lat lt 52 AND lat gt 48) then begin
		months[0]=val1
		months[1]=val2
		months[2]=val3
		months[3]=val4
		months[4]=val5
		months[5]=val6
		months[6]=val7
		months[7]=val8
		months[8]=val9
		months[9]=val10
		months[10]=val11
		months[11]=val12
		mteller=0
		while (mteller lt 12) do begin
  			year[i]=yearin
			month[i]=mteller+1
			aod[i]=months[mteller]
			JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
			mteller=mteller+1
			i=i+1
		endwhile
	endif	
endwhile	

close,2

idx=where(year ne 0. and aod ne -999.)
aant=n_elements(idx)
aod[idx[aant-3:aant-1]]=aod[idx[aant-4]]
AOD20to25={MM:month[idx],YYYY:year[idx],JD:JD[idx],aod:aod[idx]}

; -----------------------------------------------------------

i=0
year=intarr(n)
yearin=0
aod=fltarr(n)
months=fltarr(12)
month=fltarr(n)
JD=dblarr(n)
openr,3,filename3
while not(eof(3)) do begin
	char = ' '
	readf, 3, char, lat, val1, val2, val3, val4, val5, val6, $
	       val7, val8, val9, val10, val11, val12, format='(A4,F5.1,12F7.4)'
	if lat gt 85 then yearin=fix(char)
	if (lat lt 52 AND lat gt 48) then begin
		months[0]=val1
		months[1]=val2
		months[2]=val3
		months[3]=val4
		months[4]=val5
		months[5]=val6
		months[6]=val7
		months[7]=val8
		months[8]=val9
		months[9]=val10
		months[10]=val11
		months[11]=val12
		mteller=0
		while (mteller lt 12) do begin
  			year[i]=yearin
			month[i]=mteller+1
			aod[i]=months[mteller]
			JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
			mteller=mteller+1
			i=i+1
		endwhile
	endif	
endwhile	

close,3

idx=where(year ne 0. and aod ne -999.)
aant=n_elements(idx)
aod[idx[aant-3:aant-1]]=aod[idx[aant-4]]
AOD25to30={MM:month[idx],YYYY:year[idx],JD:JD[idx],aod:aod[idx]}

; -----------------------------------------------------------

i=0
year=intarr(n)
yearin=0
aod=fltarr(n)
months=fltarr(12)
month=fltarr(n)
JD=dblarr(n)
openr,4,filename4
while not(eof(4)) do begin
	char = ' '
	readf, 4, char, lat, val1, val2, val3, val4, val5, val6, $
	       val7, val8, val9, val10, val11, val12, format='(A4,F5.1,12F7.4)'
	if lat gt 85 then yearin=fix(char)
	if (lat lt 52 AND lat gt 48) then begin
		months[0]=val1
		months[1]=val2
		months[2]=val3
		months[3]=val4
		months[4]=val5
		months[5]=val6
		months[6]=val7
		months[7]=val8
		months[8]=val9
		months[9]=val10
		months[10]=val11
		months[11]=val12
		mteller=0
		while (mteller lt 12) do begin
  			year[i]=yearin
			month[i]=mteller+1
			aod[i]=months[mteller]
			JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
			mteller=mteller+1
			i=i+1
		endwhile
	endif	
endwhile	

close,4

idx=where(year ne 0. and aod ne -999.)
aant=n_elements(idx)
aod[idx[aant-3:aant-1]]=aod[idx[aant-4]]
AOD30to35={MM:month[idx],YYYY:year[idx],JD:JD[idx],aod:aod[idx]}

if (n_elements(AOD15to20.JD) eq n_elements(AOD20to25.JD)) AND $
   (n_elements(AOD20to25.JD) eq n_elements(AOD25to30.JD)) AND $
   (n_elements(AOD25to30.JD) eq n_elements(AOD30to35.JD)) then begin
	n=n_elements(AOD15to20.JD)
	aodtot=dblarr(n)
	FOR j=0,n-1 DO aodtot[j]=AOD15to20.aod[j]+AOD20to25.aod[j]+AOD25to30.aod[j]+AOD30to35.aod[j]
	AODstrat={MM:AOD15to20.MM,YYYY:AOD15to20.YYYY,JD:AOD15to20.JD,$
          	  km15to20:AOD15to20.aod,km20to25:AOD20to25.aod,km25to30:AOD25to30.aod,km30to35:AOD30to35.aod,$
	  	  aod:aodtot}
	save,AODstrat,filename=homedir+'/home/ARCHIVE_roeland/multiregression/AODstrat.sav'
endif

END


;************************************************************************

PRO read_QBO_Berlin

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/qbo_Berlin.txt'

close,1
n=10000
i=0
yyyy=intarr(n)
mm=intarr(n)
JD=dblarr(n)
hPa70=dblarr(n)
hPa50=dblarr(n)
hPa40=dblarr(n)
hPa30=dblarr(n)
hPa20=dblarr(n)
hPa15=dblarr(n)
hPa10=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	line = ''
	readf, 1, line
	reads,line, station,yymm,N70,N50,N40,$
                    N30,N20,N15,N10,$
	      format='(I5,I5,I6,I7,I7,I7,I7,I7,I7)
	yy=fix(yymm/100)
	if yy lt 50 then yyyy[i]=yy+2000 else $
	yyyy[i]=yy+1900
	mm[i]=yymm-yy*100
	print,yy
	JD[i]=JULDAY(double(mm[i]),15.d0,double(yyyy[i]))
	hPa70[i]=double(N70)
	hPa50[i]=double(N50)	
	hPa40[i]=double(N40)	
	hPa30[i]=double(N30)	
	hPa20[i]=double(N20)	
	hPa15[i]=double(N15)	
	hPa10[i]=double(N10)
	i=i+1
endwhile

idx=where(yyyy ne 0)
qbo_berlin={MM:mm[idx],YYYY:yyyy[idx],JD:JD[idx],hPa70:hPa70[idx],hPa50:hPa50[idx],$
hPa40:hPa40[idx],hPa30:hPa30[idx],hPa20:hPa20[idx],hPa15:hPa15[idx],hPa10:hPa10[idx]}
save,qbo_berlin,filename=homedir+'/home/home/ARCHIVE_roeland_roeland/multiregression/qbo_berlin2018.sav'

END

;************************************************************************

PRO read_EP_flux

homedir = STRING(getenv("HOME")) + '/fileserver'
filename = homedir + '/home/multiregression/epflux_tropo4575_ira_monthly.dat

close,1
n=10000
i=0
yyyy=intarr(n)
mm=intarr(n)
JD=dblarr(n)
EP_N=dblarr(n)
EP_S=dblarr(n)
openr,1,filename
while not(eof(1)) do begin
	line = ''
	readf, 1, line
	reads,line,Year,Month,EPfluxN,EPfluxS,$
	      format='(I4,I3,F12.8,F12.8)
	yyyy[i]=Year
	mm[i]=Month
	JD[i]=JULDAY(double(mm[i]),15.d0,double(yyyy[i]))
	EP_N[i]=EPfluxN
	EP_S[i]=EPfluxS
	i=i+1
endwhile

idx=where(yyyy ne 0)
EPflux={MM:mm[idx],YYYY:yyyy[idx],JD:JD[idx],N:EP_N[idx],S:EP_S[idx]}
save,EPflux,filename=homedir+'/home/ARCHIVE_roeland/multiregression/EPflux.sav'

END

;************************************************************************

PRO read_NOI

restore,'~/fileserver/home/multiregression/NOI_templ.sav'
NOI_raw=read_ascii('~/fileserver/home/multiregression/NOI_NOAA2018.txt',template=NOI_templ)
n=n_elements(NOI_raw.index)
JD=dblarr(n)
year=intarr(n)
month=intarr(n)
NOI=dblarr(n)
FOR i=0,n-1 DO begin
	year[i]=floor(NOI_raw.yearfrac[i])
;	if strcmp(strmid(NOI_raw.date[i],3,3),'JAN' eq 1) then month[i]=1
;	if strcmp(strmid(NOI_raw.date[i],3,3),'FEB' eq 1) then month[i]=2
;	if strcmp(strmid(NOI_raw.date[i],3,3),'MAR' eq 1) then month[i]=3
;	if strcmp(strmid(NOI_raw.date[i],3,3),'APR' eq 1) then month[i]=4
;	if strcmp(strmid(NOI_raw.date[i],3,3),'MAY' eq 1) then month[i]=5
;	if strcmp(strmid(NOI_raw.date[i],3,3),'JUN' eq 1) then month[i]=6
;	if strcmp(strmid(NOI_raw.date[i],3,3),'JUL' eq 1) then month[i]=7
;	if strcmp(strmid(NOI_raw.date[i],3,3),'AUG' eq 1) then month[i]=8
;	if strcmp(strmid(NOI_raw.date[i],3,3),'SEP' eq 1) then month[i]=9
;	if strcmp(strmid(NOI_raw.date[i],3,3),'OCT' eq 1) then month[i]=10
;	if strcmp(strmid(NOI_raw.date[i],3,3),'NOV' eq 1) then month[i]=11
;	if strcmp(strmid(NOI_raw.date[i],3,3),'DEC' eq 1) then month[i]=12	
	hlp=round((NOI_raw.yearfrac[i]-year[i])*24)
	CASE hlp OF
	   1: month[i]=1
	   3: month[i]=2
	   5: month[i]=3
	   7: month[i]=4
           9: month[i]=5
	  11: month[i]=6
	  13: month[i]=7
	  15: month[i]=8
	  17: month[i]=9
	  19: month[i]=10
	  21: month[i]=11
	  23: month[i]=12
	ENDCASE
	JD[i]=JULDAY(double(month[i]),15.d0,double(year[i]))
	NOI[i]=NOI_raw.index[i]
ENDFOR
NOI_NOAA={JD:JD,YYYY:year,MM:month,NOI:NOI}
save,NOI_NOAA,filename='~/fileserver/home/ARCHIVE_roeland/multiregression/NOI_NOAA.sav'

END

;************************************************************************

PRO prepare_monthly_means_regression

restore,'~/fileserver/home/ARCHIVE_roeland/O3Sdata/bestall/O3new.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/multiregression/totO3day.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/O3Sdata/bestall/dateascnew.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/O3Sdata/bestall/tempascnew.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/O3Sdata/bestall/tropoascnew.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/multiregression/AAO_noaa2018.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/multiregression/AO_noaa2018.sav'
restore,'~/fileserver/home/ARCHIVE_roeland/multiregression/UV.sav'
restore,'~/fileserver/home/time_analysis/ozone/groundO3/NO_Ukkel.sav'
restore,'~/fileserver/home/time_analysis/ozone/groundO3/NO2_Ukkel.sav'
restore,'~/fileserver/home/time_analysis/ozone/groundO3/O3_Ukkel.sav'
restore,'~/fileserver/home/time_analysis/ozone/groundO3/CO_Elsene.sav'

O3BL=calc_monthly_anomalies(dateasc,O3.BL,/noplot,/noprint)
O3UStr=calc_monthly_anomalies(dateasc,O3.UStr,/noplot,/noprint)
O3LStr=calc_monthly_anomalies(dateasc,O3.LStr,/noplot,/noprint)
O3Str=calc_monthly_anomalies(dateasc,O3.Str,/noplot,/noprint)
O3Tr=calc_monthly_anomalies(dateasc,O3.Tr,/noplot,/noprint)
O3Trtot=calc_monthly_anomalies(dateasc,O3.Trtot,/noplot,/noprint)
O3Tr38=calc_monthly_anomalies(dateasc,O3.Tr38,/noplot,/noprint)
O3UTr=calc_monthly_anomalies(dateasc,O3.UTr,/noplot,/noprint)
O3UTLS=calc_monthly_anomalies(dateasc,O3.UTLS,/noplot,/noprint)
O3Stot=calc_monthly_anomalies(dateasc,O3.tot,/noplot,/noprint)

O3Brew=calc_monthly_anomalies(totO3day,totO3day.O3,/noplot,/noprint)

Tsurf=calc_monthly_anomalies(dateasc,tempasc.surface,/noplot,/noprint)
T100=calc_monthly_anomalies(dateasc,tempasc.t100,/noplot,/noprint)
T150=calc_monthly_anomalies(dateasc,tempasc.t150,/noplot,/noprint)
T200=calc_monthly_anomalies(dateasc,tempasc.t200,/noplot,/noprint)
T300=calc_monthly_anomalies(dateasc,tempasc.t300,/noplot,/noprint)
T500=calc_monthly_anomalies(dateasc,tempasc.t500,/noplot,/noprint)
T700=calc_monthly_anomalies(dateasc,tempasc.t700,/noplot,/noprint)
T950=calc_monthly_anomalies(dateasc,tempasc.t950,/noplot,/noprint)
Ttrop=calc_monthly_anomalies(dateasc,tropoasc.t,/noplot,/noprint)

AOmon=calc_monthly_anomalies(AO_noaa,AO_noaa.AO,/noplot,/noprint)
AAOmon=calc_monthly_anomalies(AAO_noaa,AAO_noaa.AAO,/noplot,/noprint)
UVmon=calc_monthly_anomalies(UV,UV.UV,/noplot,/noprint)


NOsurf=calc_monthly_anomalies(NO_Ukkel,NO_Ukkel.launch,/noplot,/noprint)
NO2surf=calc_monthly_anomalies(NO2_Ukkel,NO2_Ukkel.launch,/noplot,/noprint)
O3surf=calc_monthly_anomalies(O3_Ukkel,O3_Ukkel.launch,/noplot,/noprint)
COsurf=calc_monthly_anomalies(CO_Elsene,CO_Elsene.launch,/noplot,/noprint)

