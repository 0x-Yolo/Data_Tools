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

data = pd.read_excel('/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/交易数据/examples/21010426-0430.xlsm',\
    sheet_name='数据')

# 提取原数据主键
d = pd.DataFrame([])
for dir in os.listdir('./examples'):
    if '成交统计' in dir:
        x= int(re.findall(r'\d+', dir)[0])
        y= int(re.findall(r'\d+', dir)[1])
        z= int(re.findall(r'\d+', dir)[2])
        date = dt.datetime(int(x),int(y),int(z))
        dirr = pd.read_excel('./examples'+'/'+dir,\
            sheet_name='信用债成交',header=1)
        dirr['时间'] = date
        dirr['估值时间'] = dirr['时间'] - dt.timedelta(days=1)
        d = d.append(dirr[['方向','代码','价格','时间','估值时间']])

engine = create_engine('mysql+pymysql://dngj:603603@47.116.3.109:3306/finance?charset=utf8')
add_cols = ['名字','到期估值','行权估值','行权日','price','type','估值偏离',\
    '剩余期限','rating','债券期限','城投','行业','发行人','企业性质','隐含评级','发行方式']
for c in add_cols:
    d[c]=np.nan

columns_type = [VARCHAR(30),VARCHAR(30),Float(),DateTime(),DateTime(),
                  VARCHAR(30),Float(),Float(),DateTime(),
                  Float(),VARCHAR(30),Float(),Float(),
                  VARCHAR(30),VARCHAR(30),VARCHAR(30),
                  VARCHAR(30),VARCHAR(30),VARCHAR(30),
                  VARCHAR(30),VARCHAR(30)]
dtypelist = dict(zip(d.columns,columns_type))

l=[(d , 'CreditBondTrading_v3' ,dtypelist)]
for a,b,c in l:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
    

