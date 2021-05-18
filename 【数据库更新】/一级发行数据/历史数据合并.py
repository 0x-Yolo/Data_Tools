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

path = '/Users/wdt/Desktop/tmp'

dir_list = []
for dir in os.listdir(path):
    if '新发行债券' in dir:
        dir_list.append(dir)
d = pd.DataFrame([])
for dir in dir_list:
    df = pd.read_excel(path+'/'+dir).iloc[:-3,:]
    print(dir)
    print(df.shape)
    d = d.append(df)

df['date'] = df.index
df = df.dropna(axis = 0)

list(df.columns).index('特殊期限')
(d.iloc[849, 8])

columns_type = []
for i in range(73):
    x = df.iloc[0,i]
    if 'str' in str(type(x)):
        columns_type.append(VARCHAR(30))
    if 'float' in str(type(x)):
        columns_type.append(Float())
    if 'pandas' in str(type(x)):
        columns_type.append(DateTime())
dtypelist = dict(zip(df.columns,columns_type))

d.to_csv('yijishichang.csv',index = False)

d['募集资金用途'] = np.nan
d['招标时间'] = np.nan
d['特殊期限'] = np.nan
d['承销团成员'] = np.nan


conn, engine = do.get_db_conn()
for a,b,c in [(d ,'primary market' ,dtypelist)]:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
    print('成功更新表',b)

dtypelist['债券评级'] = VARCHAR(30)
dtypelist['债券全称'] = VARCHAR(100)
dtypelist['发行人简称'] = VARCHAR(50)
dtypelist['发行人全称'] = VARCHAR(300)


dtypelist['募集资金用途'] = Float() # np.nan
dtypelist['招标时间'] = Float() # np.nan
dtypelist['特殊期限'] = Float() # np.nan
dtypelist['承销团成员'] = Float()


dtypelist['特殊条款'] = VARCHAR(30)
dtypelist['增信方式'] = VARCHAR(30)
dtypelist['评级机构'] = VARCHAR(100)
dtypelist['担保人'] = VARCHAR(60)
dtypelist['发行时担保人评级'] = VARCHAR(30)
dtypelist['担保人企业性质'] = VARCHAR(30)
dtypelist['担保条款'] = VARCHAR(200)
dtypelist['主承销商'] = VARCHAR(300)
dtypelist['承销金额主承分摊'] = VARCHAR(300)
dtypelist['副主承销商'] = VARCHAR(200)
dtypelist['簿记管理人'] = VARCHAR(200)
dtypelist['承销方式'] = VARCHAR(30)

dtypelist['招标标的'] = VARCHAR(30)
dtypelist['招标方式'] = VARCHAR(30)
dtypelist['投标区间'] = VARCHAR(30)

dtypelist['债券代码列表'] =  VARCHAR(100)

dtypelist['浮动利率(%)'] = VARCHAR(100)
for c in ['招标时间','中标价位','中标区间','承销团成员',\
    '上网认购代码','次级债或混合资本债']:
    dtypelist[c] = VARCHAR(30)


