import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer, VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do
from WindPy import w

data = do.get_data('primary_market_llz')

# 证券代码写入
for idx in data.index:
    print(idx)
    dealcode = data.loc[idx, '交易代码']

    if '.SZ' in dealcode and 'Z' not in dealcode[:-3] and 'X' not in dealcode[:-3]:
        sec_code = dealcode
        df.loc[idx,'证券代码']=sec_code
        continue
    if 'X' in dealcode:
        z_idx = dealcode.index('X')
    elif 'Z' in dealcode:
        z_idx = dealcode.index('Z')
    else:
        z_idx = -3
    sec_code = dealcode[:z_idx] + dealcode[-3:]
    data.loc[idx,'证券代码'] = sec_code
        

# 久期
idxs = []
for idx in data.index:
    print(idx)
    if data['缴款日'].isnull()[idx] == True:
        idxs .append(idx)
        continue

    code = data.loc[idx, '证券代码']
    pay_date = data.loc[idx, '缴款日']
    
    data.loc[idx, '久期'] = w.wsd(code, "modidura_cnbd", pay_date, pay_date, \
            "credibility=1").Data[0][0]

data.drop(idxs , axis = 0)

# 中债估值
for idx in data.index:
    code = data.loc[idx, '证券代码']
    yesterday= 
    data.loc[idx , '']

do.upload_data(data,'primary_market_llz_v2' , 'replace')