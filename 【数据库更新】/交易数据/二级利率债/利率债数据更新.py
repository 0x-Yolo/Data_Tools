import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do

# 汇入
path = '/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/交易数据/raw_data'
path='/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/交易数据/二级信用债/tmp_data'
d = pd.DataFrame([])
for dir in os.listdir(path):
    if ('~' in dir) | ('xlsx' not in dir):
        continue
    date = do.get_date(dir)
    print(date)
    df = pd.read_excel(path+'/'+dir,sheet_name='利率债成交',header=1)
    df = df.iloc[:,:-2]
    df['date'] = date
    d = d.append(df)
d = d.reset_index(drop=True)

for idx in d.index:
    if type(d.loc[idx,'价格']) == str:
        # print(idx)
        d.drop(idx,axis=0,inplace = True)

name = 'secondary_rate_sec'
columns_type = [VARCHAR(10),VARCHAR(10),VARCHAR(30),\
    VARCHAR(30),VARCHAR(30),VARCHAR(30),VARCHAR(30),\
    Float(),VARCHAR(30),Float(),Float(),VARCHAR(30),\
    VARCHAR(30),Float(),Float(),Float(),Float(),\
    VARCHAR(30),DateTime()]
dtypelist = dict(zip(d.columns,columns_type))

conn,engine = do.get_db_conn()
for a,b,c in [(d,name,dtypelist)]:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
