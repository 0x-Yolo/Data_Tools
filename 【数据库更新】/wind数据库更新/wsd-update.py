# get quarter bond ratio from wind-api
import data_organize as do
import pandas as pd
import numpy as np
from sqlalchemy.types import String, Float, Integer,DECIMAL,VARCHAR
from sqlalchemy import DateTime
import datetime as dt

from WindPy import w
w.start()

from iFinDPy import *
thsLogin = THS_iFinDLogin("tpy1369","510083")

def hs300():
    name = 'hs300Div'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wsd("000300.SH", "dividendyield2", \
        last_date, today_date, usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['股息率']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]
    columns_type=[Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def bond_index():
    name = 'bond_idx'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wsd("CBA05821.CS,CBA05831.CS,CBA05841.CS,CBA05851.CS,CBA02711.CS,CBA02721.CS,CBA02731.CS,CBA02741.CS,CBA02751.CS,CBA05801.CS,CBA02701.CS,CBA01901.CS,CBA03801.CS", "pct_chg", last_date, today_date, "",usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
            Float(),Float(),Float(),Float(), Float(),Float(),Float(),          
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
    
def bond_dura():
    name = 'bond_dura'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wsd("CBA05821.CS,CBA05831.CS,CBA05841.CS,CBA05851.CS,CBA02711.CS,CBA02721.CS,CBA02731.CS,CBA02741.CS,CBA02751.CS,CBA05801.CS,CBA02701.CS,CBA01901.CS,CBA03801.CS", "duration", last_date, today_date, "",usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())]
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
            Float(),Float(),Float(),Float(), Float(),Float(),Float(),          
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def organs_nav():
    name = 'organs_nav'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb("M0265776,M0265774,M0265775,M0265773,M0265777",\
         last_date, today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    # df.columns = ['证券','基金','保险','商业银行','信托']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date <= today_date.date())].dropna()
    columns_type =[DECIMAL(10,4) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def fund_nav():
    name = 'fund_nav'
    last_date = do.get_latest_date(name).strftime(format='%Y-%m-%d')
    today_date = dt.datetime.now().date().strftime(format='%Y-%m-%d')
    print('表{}的最近更新日期为{}'.format(name,last_date))

    nav = do.get_data(name)
    code_list = nav.columns[:-1]

    d = THS_DS(','.join(code_list),'ths_adjustment_nvg_rate_fund',\
        '','',last_date,today_date)

    df = d.data; df.index= df.time
    tmp = pd.DataFrame(index = df.time.unique(),columns = code_list)
    for c in tmp.columns:
        tmp[c] = df.loc[df.thscode==c,'ths_adjustment_nvg_rate_fund']
    tmp['date'] = tmp.index

    columns_type =[DECIMAL(10,6) for _ in range(tmp.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(tmp.columns,columns_type))

    # do.upload_data(tmp, name, dtypelist, 'replace')
    return tmp , name , dtypelist


def fund_risk_dura():
    # 基金季度公布久期
    fund_nav = do.get_data('fund_nav')
    code_list = fund_nav.columns[:-1]

    err,df = w.wsd(','.join(code_list), "risk_duration", \
        "2018-01-01", "2021-08-25", "Period=Q",usedf=True)
    df.dropna().to_excel('quarter_dura.xlsx')


def lunwen():    
    # gz_yield
    gz_all = pd.read_excel('Z:\\Users\\wdt\\Desktop\\tpy\\Signals\\个券成交量\\gz_all.xlsx',index_col=0)
    
    code_list = list(gz_all.index)
    err,df = w.wsd(",".join(code_list),\
         "yield_cnbd", "2018-01-01", "2021-08-25", "credibility=1", usedf=True)
    df

    err,df2 = w.wsd(",".join(code_list),\
         "yield_cnbd", "2015-01-01", "2018-01-01", "credibility=1", usedf=True)
    df2
    dff = df2.append(df)

    err,df3 = w.wsd(",".join(code_list),\
         "yield_cnbd", "2012-01-01", "2015-01-01", "credibility=1", usedf=True)
    dff=df3.append(dff)

    err,df4 = w.wsd(",".join(code_list),\
         "yield_cnbd", "2008-01-01", "2012-01-01", "credibility=1", usedf=True)
    dff=df4.append(dff)

    err,df5= w.wsd(",".join(code_list),\
         "yield_cnbd", "2004-01-01", "2008-01-01", "credibility=1", usedf=True)
    dff=df5.append(dff)

    dff.to_excel('gz_all_yield.xlsx')
    dff

def gk_yield():
    zj_issue = do.get_data('zj_issue_amt')
    zj_issue.index = zj_issue.date
    gk_list = zj_issue.loc[(zj_issue.term==10)&
        (zj_issue['issuer']=='国家开发银行'),'windcode'
        ].unique().tolist()

    def namelist2str_zj(l,rtnlist=False):
        # name_list to name_string
        strr = '' ; listt = []
        for i in range(len(l)):
            name = l[i]
            if 'z' in name[:-3] or 'Z' in name[:-3] or 'H' in name[:-3]:
                continue
            strr = strr + name + ','
            listt.append(name)
        return listt if rtnlist else strr

    _,df = w.wsd(namelist2str_zj(gk_list),\
         "yield_cnbd", "2014-01-01", "2021-08-29", "credibility=1", usedf=True)
    df['date'] = df.index
    columns_type =[DECIMAL(10,6) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    
    do.upload_data(df,'gk10_yield',dtypelist,'replace')





