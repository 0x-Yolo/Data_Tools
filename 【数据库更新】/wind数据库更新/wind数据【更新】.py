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

from WindPy import w

def upload_date(name):
    """
    输出需要更新的起始时间（数据库最后日期+1天）和终止时间（今天日期）
    """
    
    dir_date = []
    df = pd.read_sql('select * from {}'.format(name) , conn)
    last_date = df.iloc[-1 , -1]
    
    # start_date = last_date + dt.timedelta(days = 1)
    # end_date = dt.datetime.now()
    # return start_date , end_date
    return last_date 


def daily_fig_SRDI():
    name = 'fig_SRDI'
    last_date = upload_date(name)
    today_date = dt.datetime.now()

    err, df=w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',
               last_date,today_date.strftime("%Y-%m-%d"), "Fill=Previous",usedf=True)
    
    if df.shape[1] == 1:
        return [],name,[]

    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M']
    df['date'] = df.index
    df = df.dropna(axis = 0)
    df = df.loc[df.date > last_date]

    columns_type=[Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def daily_fig_liquidity_premium():
    name = 'fig_liquidity_premium'
    
    last_date = upload_date(name)
    today_date = dt.datetime.now()

    err,df=w.edb('M0017139,M0041653,M0220163,M0017142,M0048486,M1010889,M1010892,M0329545', 
                        last_date,today_date,"Fill=Previous",usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                                      "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年"]
    df['date'] = df.index
    df = df.dropna(axis = 0)
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

def daily_fig_bond_leverage():
    name = 'fig_bond_leverage'
    last_date = upload_date(name)
    today_date = dt.datetime.now()

    err, df=w.edb('M0041739,M5639029',last_date,today_date,"Fill=Previous",usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns = ['成交量:银行间质押式回购', '债券市场托管余额']
    df = df.dropna(axis = 0)
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

    err,df=w.edb('S0059749,S0059747,M1004267,M1004271,S0059744,S0059746,M1004263,M1004265',
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
    
    err,df=w.edb("M0048434,M0048424,M1004265,S0059746,M1010706,M1015080,S0059738",
                 last_date,today_date,"Fill=Previous",usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AA+):3年","中债国开债到期收益率:3年","中债国债到期收益率:3年",
                        "中债商业银行二级资本债到期收益率(AAA-):3年","中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
    df['date'] = df.index
    df = df.dropna(axis = 0)
    df = df.loc[df.date > last_date]

    columns_type=[Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

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
    db_path = "/Users/wdt/Desktop/tpy/db.txt"
    conn , engine = get_db_conn(db_path)

    l =    [daily_fig_SRDI(),
            daily_fig_bond_leverage(),
            daily_fig_credit_premium(),
            daily_fig_liquidity_premium(),
            daily_fig_rates()]


    for a,b,c in l:
        if len(np.array(a)) == 0:
            print(b , '已是最新，无需更新')
            continue
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print('成功更新表',name)

if __name__=='__main__':
    main()