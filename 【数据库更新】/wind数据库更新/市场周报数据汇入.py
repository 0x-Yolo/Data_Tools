import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do
from WindPy import w
w.start()
years = 10
end = dt.datetime.today()
start=dt.datetime.now() - dt.timedelta(days=years*365)
start=start.strftime("%Y-%m-%d")
end=end.strftime("%Y-%m-%d")

################
def cash_cost():

    err, df=w.edb('M1006336,M1006337,M1004515,M0017142',
               start,end, "Fill=Previous",usedf=True) 
    df.columns = ['DR001','DR007','GC007','shibor_3m']
    df['date'] = df.index
    df = df.dropna(axis = 0)

    name = 'cash_cost'
    columns_type=[Float(2),Float(2),Float(2),Float(2),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def policy_rate():
    # 政策利率
    err, df=w.edb('M0041371,M0041373,M0041377,M0329656,\
            M0329543,M0329544,M0329545',
               start,end, "Fill=Previous",usedf=True)
    df.columns = ['逆回购利率：7天', '逆回购利率：14天', '逆回购利率：28天',\
         '逆回购利率：63天', 'MLF：3m', 'MLF：6m',
         'MLF：1y']
    df['date'] = df.index

    name = 'policy_rate'
    # do.upload_data(df,name,'replace')
    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def monetary_policy_tools():
    # 公开市场投放 周频
    err,df = w.edb('M0061614,M0061615,M0061616,\
    M0329540,M0329541,M0329542,M5596597,\
    M0041372,M0041374,M0041378,M0329655,\
    M0062600,M0060446,M0096197,\
    M0134555,M0150207', start,end,usedf=True)
    df.columns = ['OMO：净投放', 'OMO：投放', 'OMO：回笼',\
        'MLF_数量_3m','MLF_数量_6m','MLF_数量_1y','MLF_到期',\
        '逆回购_数量_7d','逆回购_数量_14d','逆回购_数量_28d','逆回购_数量_63d',\
        '逆回购_到期','国库现金：中标量','国库现金：到期量',\
        'SLO_投放','SLO_回笼']
    df['date'] = df.index
    name = 'monetary_policy_tools'
    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def repo_volume():
    # 质押式回购成交量
    err, df=w.edb('M1004529,M0330244,M0330245,M0330246,\
    M0330247,M0330248,M0330249,M0330250,\
    M0330251,M0330252,M0330253,M0330254,\
        M0041739',\
    start,end,usedf=True) 
    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M','成交量:R1Y',
              '成交量:银行间质押式回购']
    df['date'] = df.index

    name = 'repo_volume'
    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name , dtypelist
def interbank_deposit():
    # 同业存单价格与净融资量
    err,df = w.edb('M1006645,M0329545', start,end,usedf=True)
    df.columns = ['存单_股份行_1y', 'MLF：1y']
    df['date'] = df.index

    name = 'interbank_deposit'
    columns_type=[Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name , dtypelist

################
def




for a,b,c in [interbank_deposit()]:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
    print(b, '写入完成')
