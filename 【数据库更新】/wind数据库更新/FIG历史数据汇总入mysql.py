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

from WindPy import w
w.start()
years = 10
end = dt.datetime.today()
start=dt.datetime.now() - dt.timedelta(days=years*365)
start=start.strftime("%Y-%m-%d")
end=end.strftime("%Y-%m-%d")

# test
# err, df=w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',
#               '2021-04-20','2021-04-20',usedf=True) 

'''



# SRDI
err, df_SRDI=w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',
               start,end, "Fill=Previous",usedf=True) 
df_SRDI.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M']

# fig_liquidity_premium
err,df_fig_liquidity_premium=w.edb('M0017139,M0041653,M0220163,M0017142,M0048486,M1010889,M1010892,M0329545', 
                    start,end,"Fill=Previous",usedf=True)
df_fig_liquidity_premium.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                                  "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年"]

# fig_bond_leverage
err, df_fig_bond_leverage=w.edb('M0041739,M5639029',start,end,"Fill=Previous",usedf = True)
df_fig_bond_leverage.columns = ['成交量:银行间质押式回购', '债券市场托管余额']

# fig_rates
err,df_fig_rates=w.edb('S0059749,S0059747,M1004267,M1004271,S0059744,S0059746,M1004263,M1004265',start,end,"Fill=Previous",usedf=True)
df_fig_rates.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]

# fig_credit_premium
err,df_fig_credit_premium=w.edb("M0048434,M0048424,M1004265,S0059746,M1010706,M1015080,S0059738",start,end,"Fill=Previous",usedf=True)
df_fig_credit_premium.columns=["中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AA+):3年","中债国开债到期收益率:3年","中债国债到期收益率:3年",
                    "中债商业银行二级资本债到期收益率(AAA-):3年","中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
'''
def daily_fig_SRDI():
    err, df=w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',
               start,end, "Fill=Previous",usedf=True) 
    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M']
    df['date'] = df.index
    df = df.dropna(axis = 0)

    name = 'fig_SRDI'
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
    err,df=w.edb('M0017139,M0041653,M0220163,M0017142,M0048486,M1010889,M1010892,M0329545', 
                        start,end,"Fill=Previous",usedf=True)
    df.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                                      "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年"]
    df['date'] = df.index
    df = df.dropna(axis = 0)

    name = 'fig_liquidity_premium'
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
    err, df=w.edb('M0041739,M5639029',start,end,"Fill=Previous",usedf = True)
    df.columns = ['成交量:银行间质押式回购', '债券市场托管余额']
    df = df.dropna(axis = 0)
    df['date'] = df.index

    name = 'fig_bond_leverage'
    columns_type=[Float(4),
                  Float(1),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_rates():
    err,df=w.edb('S0059749,S0059747,M1004267,M1004271,S0059744,S0059746,M1004263,M1004265',start,end,"Fill=Previous",usedf=True)
    df.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]
    df = df.dropna(axis = 0)
    df['date'] = df.index

    name = 'fig_rates'
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
    err,df=w.edb("M0048434,M0048424,M1004265,S0059746,M1010706,M1015080,S0059738",start,end,"Fill=Previous",usedf=True)
    df.columns=["中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AA+):3年","中债国开债到期收益率:3年","中债国债到期收益率:3年",
                        "中债商业银行二级资本债到期收益率(AAA-):3年","中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
    df['date'] = df.index
    df = df.dropna(axis = 0)

    name = 'fig_credit_premium'
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

# a,b,c = daily_fig_credit_premium()
conn = pymysql.connect(	
    host = '47.116.3.109',	
    user = 'dngj',	
    passwd = '603603',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8'	
)	
df_mine = pd.read_sql('show tables',conn)	

def main():
    engine = create_engine('mysql+pymysql://dngj:603603@47.116.3.109:3306/finance?charset=utf8')
    l = [daily_fig_SRDI(),
     daily_fig_liquidity_premium(),
     daily_fig_bond_leverage(),
     daily_fig_rates(),
     daily_fig_credit_premium()
    ]
    for a,b,c in l:
        # for i in range(len(a)):
            # try: 
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
        print(b, '写入完成')
        
# main()