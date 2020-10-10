import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    a = pd.read_csv("C:\\Users\\jhong\\Documents\\GitHub\\OpenITS-HeFei-Analyzation\\示范区地磁检测数据(2016.06.22~2016.06.30).csv")
    a['INTIME']=pd.to_datetime(a['INTIME'])
    a=a.loc[(a['INTIME']>='2016/6/25 8:00:00')&(a['INTIME']<='2016/6/25 9:00:00')&(a['DETECT_ID'].isin(['0002']))]
    a=(a.sort_values(by="INTIME")).reset_index(drop=True)
    print(a)