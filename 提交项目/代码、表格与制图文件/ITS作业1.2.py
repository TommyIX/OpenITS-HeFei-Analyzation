import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    print('选择车道：hte001车道1')
    a = pd.read_csv("C:\\Users\\jhong\\Documents\\GitHub\\OpenITS-HeFei-Analyzation\\黄天路口视频交通流检测数据(2016.06.22~2016.06.30).csv")
    a['FTIME']=pd.to_datetime(a['FTIME'])
    a['TTIME']=pd.to_datetime(a['TTIME'])
    timecodeflitered=a.loc[(a['FTIME']>='2016/6/25 8:00')&(a['TTIME']<='2016/6/25 9:00')&(a['DEVICECODE'].isin(['hte001']))]
    flitered=timecodeflitered[['DEVICECODE','FLOW','FTIME','TTIME']].reset_index(drop=True)
    for i in range(0,(flitered.shape[0])):
        flitered.loc[i,'FLOW'] = (flitered.loc[i].loc['FLOW']).split('_',1)[0]
    flitered=flitered[['FLOW','FTIME']]
    print(flitered)
    flownum =  [int(x) for x in flitered['FLOW']]
    plt.plot(flitered['FTIME'],flownum)
    plt.show()