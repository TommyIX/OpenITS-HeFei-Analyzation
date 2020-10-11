import numpy as np
import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    a = pd.read_csv("C:\\Users\\jhong\\Documents\\GitHub\\OpenITS-HeFei-Analyzation\\示范区地磁检测数据(2016.06.22~2016.06.30).csv")
    a['INTIME']=pd.to_datetime(a['INTIME'])
    a=a.loc[(a['INTIME']>='2016/6/25 8:00:00')&(a['INTIME']<='2016/6/25 9:00:00')&(a['DETECT_ID'].isin(['0002']))]
    a=(a.sort_values(by="INTIME"))[['DETECTOR_NUMBER','OCC_TIME','INTIME']].reset_index(drop=True)
    car_length = 3.5
    circuit_length = 1.0

    circuitaverinfo=pd.DataFrame(columns=['FLOWNUM','OCCUPYTIME','SUMSPEED'],index=range(1,27)).fillna(0.0)
    
    for index,row in a.iterrows():
        circuitaverinfo.loc[row['DETECTOR_NUMBER'],'FLOWNUM']=circuitaverinfo.loc[row['DETECTOR_NUMBER'],'FLOWNUM']+1
        circuitaverinfo.loc[row['DETECTOR_NUMBER'],'OCCUPYTIME']=circuitaverinfo.loc[row['DETECTOR_NUMBER'],'OCCUPYTIME']+row['OCC_TIME']
        circuitaverinfo.loc[row['DETECTOR_NUMBER'],'SUMSPEED']=circuitaverinfo.loc[row['DETECTOR_NUMBER'],'SUMSPEED']+float(car_length/(row['OCC_TIME']/1000))
    OCTIMERATE=[]
    AVESPEED=[]
    for index,row in circuitaverinfo.iterrows():
        OCTIMERATE.append(row['OCCUPYTIME']/(1000.00*3600.00))
        AVESPEED.append(float(row['SUMSPEED']/row['FLOWNUM']))
    SUMDIS=[0.0 for x in range(1,27)]
    LASTTIME=[datetime.strptime('2016/6/25 8:00:00', '%Y/%m/%d %H:%M:%S') for x in range(1,27)]
    for index,row in a.iterrows():
        if (LASTTIME[row['DETECTOR_NUMBER']-1]=='2016/6/25 8:00:00'):
            LASTTIME[row['DETECTOR_NUMBER']-1]=row['INTIME']
        else:
            deltatime=(row['INTIME']-LASTTIME[row['DETECTOR_NUMBER']-1]).total_seconds()
            LASTTIME[row['DETECTOR_NUMBER']-1]=row['INTIME']
            SUMDIS[row['DETECTOR_NUMBER']-1]=SUMDIS[row['DETECTOR_NUMBER']-1]+AVESPEED[row['DETECTOR_NUMBER']-1]*deltatime
    for index,row in circuitaverinfo.iterrows():
        SUMDIS[index-1]=SUMDIS[index-1]/row['FLOWNUM']
    circuitaverinfo.insert(1, 'OCCUPIED_TIMERATE', OCTIMERATE)
    circuitaverinfo.insert(2, 'AVERAGESPEED', AVESPEED)
    circuitaverinfo.insert(3, 'AVERAGEHEADWAY', SUMDIS)
    circuitaverinfo=circuitaverinfo[['FLOWNUM','OCCUPIED_TIMERATE','AVERAGESPEED','AVERAGEHEADWAY']]
    circuitaverinfo.columns = ['流量(辆)','时间占有率','车辆平均速度(m/s)','车头平均间距(m)']
    print(circuitaverinfo)
    circuitaverinfo.to_excel("ITS作业2.1.xls")