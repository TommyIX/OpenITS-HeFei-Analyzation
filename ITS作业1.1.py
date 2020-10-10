import numpy as np
import pandas as pd

if __name__ == "__main__":
    a = pd.read_csv("C:\\Users\\jhong\\Documents\\GitHub\\OpenITS-HeFei-Analyzation\\黄天路口视频交通流检测数据(2016.06.22~2016.06.30).csv")
    a['FTIME']=pd.to_datetime(a['FTIME'])
    a['TTIME']=pd.to_datetime(a['TTIME'])
    timecodeflitered=a.loc[(a['FTIME']>='2016/6/25 8:00')&(a['TTIME']<='2016/6/25 9:00')&(a['DEVICECODE'].isin(['hte001','hte002','hts001','htw001','htw002','htn001']))]
    flitered=timecodeflitered[['DEVICECODE','LANENUMBER','FLOW','SPEED','INTERVAL']]
    pathnum = [2,2,2,2,3,2]
    device = ['hte001','hte002','hts001','htw001','htw002','htn001']
    output=pd.DataFrame(columns=['路段','FLOW','SPEED','INTERVAL'])
    for i in range(0,6):
        for j in range(1,pathnum[i]+1):
            indname = (device[i]+'(车道'+str(j)+')')
            new=pd.DataFrame({'路段':indname,'FLOW':0,'SPEED':0,'INTERVAL':0},index=[1])
            output=output.append(new)
    output=output.set_index('路段')
    dividerate=pd.DataFrame(columns=device,index=[1]).fillna(0)
    
    for index,row in flitered.iterrows():
        laneNum = row['LANENUMBER']
        FLOWS = row['FLOW'].split('_',laneNum-1)
        SPEEDS = row['SPEED'].split('_',laneNum-1)
        INTERVALS = row['INTERVAL'].split('_',laneNum-1)
        dividerate.loc[1,row['DEVICECODE']] = dividerate.loc[1,row['DEVICECODE']]+1
        for i in range(0,laneNum):
            odname = (row['DEVICECODE']+'(车道'+str(i+1)+')')
            output.loc[odname].loc['FLOW']=int(output.loc[odname].loc['FLOW'])+int(FLOWS[i])
            output.loc[odname].loc['SPEED']=int(output.loc[odname].loc['SPEED'])+int(SPEEDS[i])
            output.loc[odname].loc['INTERVAL']=float(output.loc[odname].loc['INTERVAL'])+float(INTERVALS[i])
    
    for i in range(0,6):
        for j in range(1,pathnum[i]+1):
            indname = (device[i]+'(车道'+str(j)+')')
            output.loc[indname].loc['SPEED'] = output.loc[indname].loc['SPEED']/dividerate.loc[1,device[i]]
            output.loc[indname].loc['INTERVAL'] = output.loc[indname].loc['INTERVAL']/dividerate.loc[1,device[i]]

    output.columns = ['流量(辆)','平均速度(km/h)','平均车头时距(s/辆)']
    output.to_excel("ITS作业1.1.xls")