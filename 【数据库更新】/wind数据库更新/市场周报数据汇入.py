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
years = 20
end = dt.datetime.today()
start=dt.datetime.now() - dt.timedelta(days=years*365)


#### 流动性 ####
def cash_cost():

    err, df=w.edb('M1006336,M1006337,M1004515,M0017142,M1001795',
               start,end,usedf=True) 
    df.columns = ['DR001','DR007','GC007','shibor_3m','R007']
    df['date'] = df.index

    df = df.loc[df.date<end.date()]

    name = 'cash_cost'
    columns_type=[Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def policy_rate():
    # 政策利率
    err, df=w.edb('M0041371,M0041373,M0041377,M0329656,\
            M0329543,M0329544,M0329545',
               start,end,usedf=True)
    df.columns = ['逆回购利率：7天', '逆回购利率：14天', '逆回购利率：28天',\
         '逆回购利率：63天', 'MLF：3m', 'MLF：6m',
         'MLF：1y']
    df['date'] = df.index

    df = df.loc[df.date<end.date()]

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
    df = df.loc[df.date < dt.datetime.now().date()]
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
    df = df.loc[df.date < end.date()]
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
    df = df.loc[df.date < end.date()]

    name = 'interbank_deposit'
    columns_type=[Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name , dtypelist

##############
def rates():
    err,df = w.edb("S0059744,S0059746,S0059747,S0059748,S0059749,\
            M1004298,M1004300,M1004302,M1004304,M1004306,\
            M1004263,M1004265,M1004267,M1004269,M1004271,\
            M0048432,M0048434,M0048435,M0048436,\
            M0048422,M0048424,M0048425,M0048426,\
            M0048412,M0048414,M0048415,M0048416,\
            S0059736,S0059738,S0059739,\
            S0059722,S0059724,S0059725,\
            S0059715,S0059717,S0059718,\
            S0059729,S0059731,S0059732",\
            # M1002654,M1002656,M1002658,\
            # M1003631,M1003633,M1003635,\
            # M1003639,M1003641,M1003643,\
            # M1003623,M1003625,M1003627,\
         start,end,usedf = True)

    df.columns=['国债1年','国债3年','国债5年','国债7年','国债10年',\
        '地方1年','地方3年','地方5年','地方7年','地方10年',\
        '国开1年','国开3年','国开5年','国开7年','国开10年',\
        '城投_AAA_1y','城投_AAA_3y','城投_AAA_5y','城投_AAA_7y',\
        '城投_AA+_1y','城投_AA+_3y','城投_AA+_5y','城投_AA+_7y',\
        '城投_AA_1y','城投_AA_3y','城投_AA_5y','城投_AA_7y',\
        '中票_AAA_1y','中票_AAA_3y','中票_AAA_5y',\
        '中票_AA+_1y','中票_AA+_3y','中票_AA+_5y',\
        '中票_AA_1y','中票_AA_3y','中票_AA_5y',\
        '中票_AA-_1y','中票_AA-_3y','中票_AA-_5y']

    df['date'] = df.index
    df = df.loc[df.date < end.date()]

    name = 'rates'
    columns_type=[Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name , dtypelist



conn,engine = do.get_db_conn()
l = [policy_rate(), monetary_policy_tools(), repo_volume(),\
    interbank_deposit(), rates()]
for a,b,c in l:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
    print(b, '写入完成')
