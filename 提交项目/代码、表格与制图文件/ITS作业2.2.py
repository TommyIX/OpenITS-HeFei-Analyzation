import numpy as np
import pandas as pd
import datetime
import math

if __name__ == "__main__":
    print('选择车道:1,14')
    a = pd.read_csv("C:\\Users\\jhong\\Documents\\GitHub\\OpenITS-HeFei-Analyzation\\示范区地磁检测数据(2016.06.22~2016.06.30).csv")
    a['INTIME']=pd.to_datetime(a['INTIME'])
    a=a.loc[(a['INTIME']>='2016/6/25 8:00:00')&(a['INTIME']<='2016/6/25 9:00:00')&(a['DETECT_ID'].isin(['0002'])&(a['DETECTOR_NUMBER'].isin(['1','14'])))]
    a=(a.sort_values(by="INTIME"))[['DETECTOR_NUMBER','OCC_TIME','INTIME']].reset_index(drop=True)
    
    car_length = 3.5
    circuit_length = 1.0

    timelags=[] #用于形成数据切片
    for i in range(0,12):
        timelags.append(datetime.datetime.strptime('2016/6/25 8:00:00', '%Y/%m/%d %H:%M:%S')+i*datetime.timedelta(minutes=5))
    b=pd.DataFrame(columns=['FLOW','SPEED','DENSITY'],index=[])
    b.insert(0,'时间段(起始)', timelags)
    b=b.set_index('时间段(起始)').fillna(0.0)
    for index,row in a.iterrows():
        for i in timelags:
            if (row['INTIME']>i and row['INTIME']<=(i+datetime.timedelta(minutes=5))):
                b.loc[i,'FLOW']=b.loc[i,'FLOW']+1
                b.loc[i,'SPEED']=b.loc[i,'SPEED']+float((car_length+circuit_length)/(row['OCC_TIME']/1000))
    flowsum = 0
    for index,row in b.iterrows():
        row['SPEED']=row['SPEED']/row['FLOW']
        row['FLOW']=math.ceil(row['FLOW']/2)
        flowsum = flowsum + row['FLOW']
    for index,row in b.iterrows():
        row['DENSITY']=row['FLOW']/5
    b.columns = ['流量(辆)','平均车速(m/s)','车辆密度(辆/min)']
    b.to_excel('ITS作业2.2.xls')