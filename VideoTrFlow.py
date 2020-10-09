import numpy as np
import pandas as pd
from pandas import DataFrame as df

if __name__ == "__main__":
    a = pd.read_csv("C:\\Users\\jhong\\Documents\\GitHub\\OpenITS-HeFei-Analyzation\\黄天路口视频交通流检测数据(2016.06.22~2016.06.30).csv")
    a['FTIME']=pd.to_datetime(a['FTIME'])
    a['TTIME']=pd.to_datetime(a['TTIME'])
    flitered=a.loc[(a['FTIME']>='2016/6/25 8:00')&(a['TTIME']<='2016/6/25 9:00')&(a['DEVICECODE'].isin(['hte001','hte002','hts001','htw001','htw002','htn001']))]
    output=pd.DataFrame(columns=['路段','流量（辆）','速度(km/h)','车头时距(s/辆)'])
    output['路段']=['hte001','hte002','hts001','htw001','htw002','htn001']
    output.set_index(['路段'])
    
    print(output)