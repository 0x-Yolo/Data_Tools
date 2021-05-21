import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do

from WindPy import w

def upload_date(name):
    """
    输入表名
    输出该表的最新日期
    """
    
    dir_date = []
    df = pd.read_sql('select max(date) from {}'.format(name) , conn)
    last_date = df.iloc[-1 , -1]
    
    today_date = dt.datetime.now()
    
    return last_date 

def cash_cost():
    name = 'cash_cost'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1006336,M1006337,M1004515,M0017142',
               last_date,today_date, "Fill=Previous",usedf=True) 
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['DR001','DR007','GC007','shibor_3m']
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(2),Float(2),Float(2),Float(2),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def policy_rate():
    name = 'policy_rate'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041371,M0041373,M0041377,M0329656,\
            M0329543,M0329544,M0329545',
               last_date,today_date, "Fill=Previous",usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['逆回购利率：7天', '逆回购利率：14天', '逆回购利率：28天',\
         '逆回购利率：63天', 'MLF：3m', 'MLF：6m',
         'MLF：1y']
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def monetary_policy_tools():
    name = 'monetary_policy_tools'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb('M0061614,M0061615,M0061616,\
    M0329540,M0329541,M0329542,M5596597,\
    M0041372,M0041374,M0041378,M0329655,\
    M0062600,M0060446,M0096197,\
    M0134555,M0150207', last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['OMO：净投放', 'OMO：投放', 'OMO：回笼',\
        'MLF_数量_3m','MLF_数量_6m','MLF_数量_1y','MLF_到期',\
        '逆回购_数量_7d','逆回购_数量_14d','逆回购_数量_28d','逆回购_数量_63d',\
        '逆回购_到期','国库现金：中标量','国库现金：到期量',\
        'SLO_投放','SLO_回笼']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= dt.datetime.now().date())]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def repo_volume():
    name = 'repo_volume'
    last_date = upload_date(name)
    today_date = dt.datetime.now().date()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1004529,M0330244,M0330245,M0330246,\
    M0330247,M0330248,M0330249,M0330250,\
    M0330251,M0330252,M0330253,M0330254,\
        M0041739',\
       last_date,today_date.strftime("%Y-%m-%d"), "Fill=Previous",usedf=True)
    
    if df.shape[1] == 1:
        return [],name,[]

    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M','成交量:R1Y',\
                  '成交量:银行间质押式回购']
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def interbank_deposit():
    name = 'interbank_deposit'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb('M1006645,M0329545', last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['存单_股份行_1y', 'MLF：1y']
    df['date'] = df.index
    df = df.loc[df.date > last_date]
    columns_type=[Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

##############
def daily_fig_liquidity_premium():
    name = 'fig_liquidity_premium'
    
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb('M0017139,M0041653,M0220163,\
    M0017142,M0048486,M1010889,M1010892,M0329545,\
    M1011048', \
        last_date,today_date,"Fill=Previous",usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年",
                 "国股银票转贴现收益率_3m"]
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_bond_leverage():
    name = 'fig_bond_leverage'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041739,M5639029',last_date,today_date,usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns = ['成交量:银行间质押式回购', '债券市场托管余额']
    # df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(4),
                  Float(1),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name, dtypelist

def daily_fig_rates():
    name = 'fig_rates'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb('S0059744,S0059746,S0059747,S0059749,M1004263,M1004265,M1004267,M1004271',
                 last_date,today_date,"Fill=Previous",usedf=True)
        
    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]
    df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_credit_premium():
    name = 'fig_credit_premium'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))
    
    err,df=w.edb("M0048432,M0048434,M0048435, \
                  M0048422,M0048424,M0048425, \
                  M0048412,M0048414,M0048415, \
                  M1004265,S0059746,          \
                  M1010704,M1010706,M1010708, \
                  M1015080,S0059738",
                 last_date,today_date,usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["中债城投债到期收益率(AAA):1年","中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AAA):5年",
                "中债城投债到期收益率(AA+):1年","中债城投债到期收益率(AA+):3年","中债城投债到期收益率(AA+):5年",
                "中债城投债到期收益率(AA):1年","中债城投债到期收益率(AA):3年","中债城投债到期收益率(AA):5年",
                "中债国开债到期收益率:3年","中债国债到期收益率:3年",
                "中债商业银行二级资本债到期收益率(AAA-):1年","中债商业银行二级资本债到期收益率(AAA-):3年","中债商业银行二级资本债到期收益率(AAA-):5年",
                "中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def industial_premium():
    name = 'fig_industries_premium'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("M1008950,M1008953,M1008973,M1008971,M1008964", 
                   start, end, usedf = True) 
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ["信用利差_地产","信用利差_钢铁","信用利差_煤炭",\
                  "信用利差_有色","信用利差_汽车"]
    df['date'] = df.index
    df=df.loc[df.date>last_date]

    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df,name,dtypelist



def get_db_conn(io):
    with open(io, 'r') as f1:
        config = f1.readlines()
    for i in range(0, len(config)):
        config[i] = config[i].rstrip('\n')

    host = config[0]  
    username = config[1]  # 用户名 
    password = config[2]  # 密码
    schema = config[3]
    port = int(config[4])
    engine_txt = config[5]

    conn = pymysql.connect(	
        host = host,	
        user = username,	
        passwd = password,	
        db = schema,	
        port=port,	
        charset = 'utf8'	
    )	
    engine = create_engine(engine_txt)
    return conn, engine

def main():
    w.start()

    # @ 读取db.txt内的邮箱信息
    conn , engine = do.get_db_conn()
    '''
    l =    [daily_fig_SRDI(),
            daily_fig_bond_leverage(),
            daily_fig_credit_premium(),
            daily_fig_liquidity_premium(),
            daily_fig_rates(),industial_premium()
            ]
    # 宏观周报数据
    l2 =    [
            fig_industrial_production(),
            fig_cpi_ppi_related(),
            fig_upstream(),fig_downstream(),fig_midstream()
            ]
    '''
    # 流动性
    l = [cash_cost(),policy_rate(),monetary_policy_tools(),\
        repo_volume(),interbank_deposit()]

    for a,b,c in l:
        if len(np.array(a)) == 0:
            print(b , '已是最新，无需更新')
            continue
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print('成功更新表',b)

if __name__=='__main__':
    main()