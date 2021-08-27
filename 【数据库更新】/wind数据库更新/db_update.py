import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pymysql
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do

from WindPy import w


def cash_amt_prc():
    # 资金现券与成交量
    name = 'cash_amt_prc'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("M0041652,M0041653,M0041655,M1004511,M1004515,M0220162,M0220163,M0330244,M0041739,M0041740",
        last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['R001','R007','R021','GC001','GC007','DR001','DR007',\
        '成交量:R001','成交量:银行间质押式回购','成交量:银行间债券现券']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]
    
    columns_type=[Float(),Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def spreads():
    # 息差与杠杆
    name = 'spreads'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("M0220162,M0220163,M1004515,M0048486,M0048490,M1004007,M1004900,S0059722,S0059724,S0059725,M1004271,M1004300", \
        last_date, today_date, usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['DR001','DR007','GC007','IRS_1y_FR007','IRS_5y_FR007',\
        'IRS_5y_shibor3m','cd_AAA_6m',\
        '中短票_AA+_1y','中短票_AA+_3y','中短票_AA+_5y',\
        '国开10年','地方债_AAA_3y']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def cash_cost():
    name = 'cash_cost'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1006336,M1006337,M1004515,M0017142,M1001795',
               last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['DR001','DR007','GC007','shibor_3m','R007']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]


    columns_type=[Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def policy_rate():
    name = 'policy_rate'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041371,M0041373,M0041377,M0329656,\
            M0329543,M0329544,M0329545',
               last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['逆回购利率：7天', '逆回购利率：14天', '逆回购利率：28天',\
         '逆回购利率：63天', 'MLF：3m', 'MLF：6m',
         'MLF：1y']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def monetary_policy_tools():
    name = 'monetary_policy_tools'
    last_date = do.get_latest_date(name)
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
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1001794,M0330244,M0330245,M0330246,\
    M0330247,M0330248,M0330249,M0330250,\
    M0330251,M0330252,M0330253,M0330254,\
        M0041739',\
       last_date,today_date.strftime("%Y-%m-%d"),usedf=True)
    
    if df.shape[1] == 1:
        return [],name,[]

    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M','成交量:R1Y',\
                  '成交量:银行间质押式回购']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def interbank_deposit():
    name = 'interbank_deposit'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb('M1006645,M0329545', last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['存单_股份行_1y', 'MLF：1y']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

    columns_type=[Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def rates():
    name = 'rates'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("S0059744,S0059746,S0059747,S0059748,S0059749,\
            M1004298,M1004300,M1004302,M1004304,M1004306,\
            M1004263,M1004265,M1004267,M1004269,M1004271,\
            M0048432,M0048434,M0048435,M0048436,\
            M0048422,M0048424,M0048425,M0048426,\
            M0048412,M0048414,M0048415,M0048416,\
            S0059736,S0059738,S0059739,\
            S0059722,S0059724,S0059725,\
            S0059715,S0059717,S0059718,\
            S0059729,S0059731,S0059732,\
            M1007675,S0059838,S0059752,\
            S0059741,S0059742,S0059751,\
            M1004260,M1004261,M1004273,M1004274,\
            M1006615,S0059745",\
         last_date,today_date,usedf = True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns=['国债1年','国债3年','国债5年','国债7年','国债10年',\
        '地方1年','地方3年','地方5年','地方7年','地方10年',\
        '国开1年','国开3年','国开5年','国开7年','国开10年',\
        '城投_AAA_1y','城投_AAA_3y','城投_AAA_5y','城投_AAA_7y',\
        '城投_AA+_1y','城投_AA+_3y','城投_AA+_5y','城投_AA+_7y',\
        '城投_AA_1y','城投_AA_3y','城投_AA_5y','城投_AA_7y',\
        '中票_AAA_1y','中票_AAA_3y','中票_AAA_5y',\
        '中票_AA+_1y','中票_AA+_3y','中票_AA+_5y',\
        '中票_AA_1y','中票_AA_3y','中票_AA_5y',\
        '中票_AA-_1y','中票_AA-_3y','中票_AA-_5y',
        '农发10年','口行10年','国债30年',
        '国债3月','国债6月','国债20年',\
        '国开3月','国开6月','国开20年','国开30年',
        'cd_3m_aaa+','国债2年']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),
    Float(),Float(),Float(),
    Float(),Float(),Float(),
    Float(),Float(),Float(),Float(),
    Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist
##############
def daily_fig_liquidity_premium():
    name = 'fig_liquidity_premium'
    
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb('M0017139,M0041653,M0220163,\
    M0017142,M0048486,M1010889,M1010892,M0329545,\
    M1011048', \
        last_date,today_date,usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年",
                 "国股银票转贴现收益率_3m"]
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]


    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def monthly_fig_bond_leverage():
    name = 'fig_bond_leverage'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041754,M0041746',last_date,today_date,usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns =['银行间质押式回购余额', '中债托管余额']
    # df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]
    columns_type=[Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def monthly_sq():
    name = 'sq_dps_amt'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb("M0096412,M0341750,M0096433,M0329565,M0329612,M0096484,\
            M0096505,M0096547,M0096526,M0096307,M0329591,M0340603,\
            M0340624,M0340645,M0340666,M0340687,M0340708",\
                last_date,today_date,usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    # df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
                Float(),Float(),Float(),Float(), Float(),Float(), 
                Float(),Float(),Float(),Float(), Float(),        
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_netfinancing_amt():
    name = 'net_financing_amt'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df= w.wset("bondissuanceandmaturity",\
            "startdate={};enddate={};frequency=day;\
            maingrade=all;zxgrade=all;datetype=startdate;type=default;\
            bondtype=default;bondid=1000008489000000,a101020100000000,\
            a101020200000000,a101020300000000,1000011872000000,a101020400000000,\
            a101020700000000,a101020800000000,a101020b00000000,a101020500000000,\
            1000013981000000,1000002993000000,1000004571000000,1000040753000000,\
            a101020a00000000,a101020600000000,1000016455000000,a101020900000000;\
            field=startdate,netfinancingamount".format\
                ((last_date.date().strftime('%Y-%m-%d')), \
                (today_date.date().strftime('%Y-%m-%d'))),\
            usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns =['date', 'netfinancingamount']
    df = df.loc[(df.date > last_date) & (df.date <= today_date)]
    columns_type=[
                  DateTime(),Float()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_rates():
    name = 'fig_rates'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb('S0059744,S0059746,S0059747,S0059749,M1004263,M1004265,M1004267,M1004271',
                 last_date,today_date,usedf=True)
        
    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]
    df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

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
    last_date = do.get_latest_date(name)
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
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist


def rates_us():
    name = 'rates_us'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("G0000886,G0000887,G0000891,G8455661,M0000185,G0000898", \
        last_date, today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['美债1年','美债2年','美债10年','美债10-2','美元兑人民币','libor_3m']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())].dropna()

    columns_type=[Float(),Float(),Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def gz_issue_amt():
    name = 'gz_issue_amt'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wset("nationaldebtissueandclosesub",\
        "startdate={};enddate={};\
        frequency=day;maingrade=all;zxgrade=all;\
        datetype=startdate;type=default;bondtype=governmentbonds;\
        bondid=1000008489000000,a101020100000000,a101020200000000,a101020300000000,1000011872000000,a101020400000000,a101020700000000,a101020800000000,a101020b00000000,a101020500000000,1000013981000000,1000002993000000,1000004571000000,a101020a00000000,a101020600000000,1000016455000000,a101020900000000;\
        field=startdate,windcode,issueprice,term,issuer".format\
        ((last_date.date().strftime('%Y-%m-%d')), \
         (today_date.date().strftime('%Y-%m-%d'))),usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['date','windcode','issueprice','term','issuer']
    # df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date)]
    columns_type=[DateTime(),VARCHAR(20),Float(),Float(),VARCHAR(15)]
    dtypelist = dict(zip(df.columns,columns_type))
    
    return df , name , dtypelist

def zj_issue_amt():
    name = 'zj_issue_amt'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wset("nationaldebtissueandclosesub",\
        "startdate={};enddate={};\
        frequency=day;maingrade=all;zxgrade=all;\
        datetype=startdate;type=default;bondtype=policybankbonds;\
        bondid=1000008489000000,a101020100000000,a101020200000000,a101020300000000,1000011872000000,a101020400000000,a101020700000000,a101020800000000,a101020b00000000,a101020500000000,1000013981000000,1000002993000000,1000004571000000,a101020a00000000,a101020600000000,1000016455000000,a101020900000000;\
        field=startdate,windcode,issueprice,term,issuer".format\
        ((last_date.date().strftime('%Y-%m-%d')), \
         (today_date.date().strftime('%Y-%m-%d'))),usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['date','windcode','issueprice','term','issuer']
    # df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date)]
    columns_type=[DateTime(),VARCHAR(20),Float(),Float(),VARCHAR(15)]
    dtypelist = dict(zip(df.columns,columns_type))
    
    return df , name , dtypelist


def net_bond_daily_volume():
    # 具体个券每日成交量
    def namelist2str_gz(l):
        # name_list to name_string
        strr = ''
        for i in range(len(l)):
            name = l[i]
            if 'x' in name or 'X' in name or 'IB' not in name:
                continue
            strr = strr + name + ','
        return strr
    def namelist2str_zj(l):
        # name_list to name_string
        strr = ''
        for i in range(len(l)):
            name = l[i]
            if 'z' in name or 'Z' in name or 'H' in name:
                continue
            strr = strr + name + ','
        return strr
    def get_gz_issue():
        gz_issue = do.get_data('gz_issue_amt')
        gz_issue.index = gz_issue.date
        for j in range(gz_issue.shape[0]):
            idx = gz_issue.index[j] ; n = gz_issue.iloc[j,1] # windcode
            t = gz_issue.iloc[j,3]# term
            if ('x' in n) or ('X' in n):
                continue
            gz_issue.loc[(gz_issue.date==idx)&(gz_issue.windcode==n) \
                ,'到期日'] = idx.date() + dt.timedelta(days=365 * t)
        for j in range(gz_issue.shape[0]):
            idx = gz_issue.index[j] ; n = gz_issue.iloc[j,1] # windcode
            t = gz_issue.iloc[j,3]# term
            if 'x' not in n and 'X' not in n:
                continue
            if 'x' in n :
                idxx = n.index('x')
            else:
                idxx = n.index('X')
            main_name = n[:idxx] + n[-3:]
            gz_issue.loc[(gz_issue.date==idx)&(gz_issue.windcode==n) \
                ,'到期日'] = gz_issue.loc[(gz_issue.windcode==main_name) \
                ,'到期日'][0]
        ii=[]
        for i in range(gz_issue.shape[0]):
            if gz_issue.iloc[i,1][-3:]=='.IB':
                ii.append(i)
        gz_issue = gz_issue.iloc[ii]
        return gz_issue
    def get_zj_issue():
        zj_issue = do.get_data('zj_issue_amt')
        zj_issue.index = zj_issue.date
        for j in range(zj_issue.shape[0]):
            idx = zj_issue.index[j] ; n = zj_issue.iloc[j,1]
            t = zj_issue.iloc[j,3]
            if (('z' in n[:-3]) | ('Z' in n[:-3]) | ('H' in n[:-3])) :
                continue
            zj_issue.loc[(zj_issue.date==idx)&(zj_issue.windcode==n) \
                ,'到期日'] = idx.date() + dt.timedelta(days=365 * t)
            
        for j in range(zj_issue.shape[0]):
            idx = zj_issue.index[j] ; n = zj_issue.iloc[j,1] # windcode
            t = zj_issue.iloc[j,3] # term
            if (('z' not in n[:-3]) & ('Z' not in n[:-3])) :
                continue
            if 'z' in n :
                idxx = n.index('z')
            elif 'Z' in n:
                idxx = n.index('Z')
            elif 'H' in n:
                idxx = n.index('H')
            main_name = n[:idxx] + n[-3:]
            zj_issue.loc[(zj_issue.date==idx)&(zj_issue.windcode==n) \
                ,'到期日'] = zj_issue.loc[(zj_issue.windcode==main_name) \
                ,'到期日'][0]
        jj=[]
        for i in range(zj_issue.shape[0]):
            if zj_issue.iloc[i,1][-3:]=='.IB':
                jj.append(i)
        zj_issue = zj_issue.iloc[jj]
        return zj_issue
    gz_issue = get_gz_issue()
    zj_issue = get_zj_issue()

    gz_all = pd.read_excel('Z:\\Users\\wdt\\Desktop\\tpy\\Signals\\个券成交量\\gz_all.xlsx',index_col=0)
    last_date = dt.datetime.strptime(gz_all.columns.max(),'%Y%m%d')
    today_date = dt.datetime.now()

    # * get all-year-gz namelist
    gz_names = gz_issue.windcode.tolist(); gz_name_list = []
    for i in range(len(gz_names)):
        name = gz_names[i]
        if 'x' in name or 'X' in name or 'IB' not in name:
            continue
        gz_name_list.append(name)
    # * get from wind
    d = pd.DataFrame([],index = gz_name_list)
    for date in do.get_data('rates')['date']:
        if date <= last_date:
            continue
        print(date)
        names=gz_issue.loc[(gz_issue.index<=date)&(gz_issue['到期日']>date.date()),'windcode'].tolist()
        names_str = namelist2str_gz(names)

        da = date.date().strftime(format='%Y%m%d')
        err, df= w.wss(names_str, "volume",\
            "tradeDate={};cycle=D".format(int(da)),\
                usedf=True)
        df.columns=[da]
        d[da] = df
    d[gz_all.columns] = gz_all
    d.to_excel('gz_all_update.xlsx')
    #######################
    zj_all = pd.read_excel('Z:\\Users\\wdt\\Desktop\\tpy\\Signals\\个券成交量\\zj_all.xlsx',index_col=0)
    last_date = dt.datetime.strptime(zj_all.columns.max(),'%Y%m%d')
    today_date = dt.datetime.now()
    # * get all-year-zj namelist
    zj_names = zj_issue.windcode.tolist(); zj_name_list = []
    for i in range(len(zj_names)):
        name = zj_names[i]
        if 'Z' in name[:-3] or 'z' in name[:-3] or 'H' in name[:-3]:
            continue
        zj_name_list.append(name)
    # * get from wind
    d = pd.DataFrame([],index = zj_name_list)
    for date in do.get_data('rates')['date']:
        if date <= last_date:
            continue

        names=zj_issue.loc[(zj_issue.index<=date)&(zj_issue['到期日']>date.date()),'windcode'].tolist()
        names_str = namelist2str_zj(names)

        da = date.date().strftime(format='%Y%m%d')
        err, df= w.wss(names_str, "volume",\
            "tradeDate={};cycle=D".format(int(da)),\
                usedf=True)
        df.columns=[da]
        d[da] = df
    d[gz_all.columns] = zj_all
    d.to_excel('zj_all_update.xlsx')



def main():
    w.start()

    # @ 读取db.txt内的邮箱信息
    
    l =    [
            monthly_fig_bond_leverage(),monthly_sq(),daily_netfinancing_amt(),
            daily_fig_credit_premium(),
            daily_fig_liquidity_premium(),
            daily_fig_rates(),
            cash_cost(),policy_rate(),monetary_policy_tools(),\
            repo_volume(),interbank_deposit(),rates(),
            cash_amt_prc(),spreads(),]
    l =   [monthly_fig_bond_leverage(),monthly_sq()]

    conn , engine = do.get_db_conn()
    for a,b,c in l:
        if len(np.array(a)) == 0:
            print(b , '已是最新，无需更新')
            continue
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print('成功更新表',b, '至', do.get_latest_date(b))

if __name__=='__main__':
    main()