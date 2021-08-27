from numpy.lib import financial
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer,DECIMAL,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do
from WindPy import w
w.start()

def namelist2str(l):
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
    gz_issue.index = gz_issue.startdate
    for j in range(gz_issue.shape[0]):
        idx = gz_issue.index[j] ; n = gz_issue.iloc[j,1] # windcode
        t = gz_issue.iloc[j,3]# term
        if ('x' in n) or ('X' in n):
            continue
        gz_issue.loc[(gz_issue.startdate==idx)&(gz_issue.windcode==n) \
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
        gz_issue.loc[(gz_issue.startdate==idx)&(gz_issue.windcode==n) \
            ,'到期日'] = gz_issue.loc[(gz_issue.windcode==main_name) \
            ,'到期日'][0]
    return gz_issue

def get_zj_issue():
    zj_issue = do.get_data('policy_issue_amt')
    zj_issue.index = zj_issue.startdate
    for j in range(zj_issue.shape[0]):
        idx = zj_issue.index[j] ; n = zj_issue.iloc[j,1]
        t = zj_issue.iloc[j,4]
        if (('z' in n[:-3]) | ('Z' in n[:-3]) | ('H' in n[:-3])) :
            continue
        zj_issue.loc[(zj_issue.startdate==idx)&(zj_issue.windcode==n) \
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
        zj_issue.loc[(zj_issue.startdate==idx)&(zj_issue.windcode==n) \
            ,'到期日'] = zj_issue.loc[(zj_issue.windcode==main_name) \
            ,'到期日'][0]
    
    return zj_issue

# * get data
gz_issue = get_gz_issue()
zj_issue = get_zj_issue()

# * get 30Y name_list
gz30 = gz_issue.loc[gz_issue.term==30]
gz30_names = gz30.windcode.tolist(); gz30_name_list = []
for i in range(len(gz30_names)):
    name = gz30_names[i]
    if 'x' in name or 'X' in name:
        continue
    gz30_name_list.append(name)

# * get 10Y-GK namelist
gk10 = zj_issue.loc[(zj_issue.term==10)&\
    (zj_issue.issuer=='国家开发银行')]
gk10_names = gk10.windcode.tolist(); gk10_name_list = []
for i in range(len(gk10_names)):
    name = gk10_names[i]
    if 'z' in name[:-3] or 'Z' in name[:-3] or 'H' in name[:-3]:
        continue
    gk10_name_list.append(name)

# * get all-year-gz namelist
gz_else = gz_issue.loc[gz_issue.term!=30]
gz_else_names = gz_else.windcode.tolist(); gz_else_name_list = []
for i in range(len(gz_else_names)):
    name = gz_else_names[i]
    if 'x' in name or 'X' in name or 'IB' not in name:
        continue
    gz_else_name_list.append(name)

# * get all-year-zj namelist
zj_names = zj_issue.windcode.tolist(); zj_name_list = []
for i in range(len(zj_names)):
    name = zj_names[i]
    if 'Z' in name[:-3] or 'z' in name[:-3] or 'H' in name[:-3]:
        continue
    zj_name_list.append(name)


# * ++++++++++++++++++++
# * get trade date
dates = pd.read_excel('Z:\\Users\\wdt\\Desktop\\tmp.xlsx',sheet_name='Sheet3',\
    )
date_list = dates.date.tolist()

# * get gz30 daily volume From Wind
d=pd.DataFrame(index = gz30_name_list)
for date in date_list[::-1]:
    print(date)
    names=gz30.loc[(gz30.startdate<=date)&(gz30['到期日']>date),'windcode']
    names_str = namelist2str(names)

    if len(names) == 0:
        continue
    
    da = date.date().strftime(format='%Y%m%d')
    
    err, df= w.wss(names_str, "volume",\
        "tradeDate={};cycle=D".format(int(da)),\
            usedf=True)
    df.columns=[da]
    
    d[da] = df


# * get gk10 daily volume From Wind
d = pd.DataFrame(index = gk10_name_list)
for date in date_list[::-1]:
    print(date)

    # get gk10 namestring on that day market
    names=gk10.loc[(gk10.startdate<=date)&(gk10['到期日']>date),'windcode']
    names_str = namelist2str(names)
    if len(names) == 0:
        continue
    da = date.date().strftime(format='%Y%m%d')
    
    if da < '2015-01-01':
        continue
    # get wind df
    err, df= w.wss(names_str, "volume",\
        "tradeDate={};cycle=D".format(int(da)),\
            usedf=True)
    df.columns=[da]
    
    d[da] = df


# * get gz-else daily volume From Wind
d = pd.DataFrame(index = gz_else_name_list)
for date in date_list[::-1]:
    print(date)

    # get gz-else namestring on that day market
    names=gz_else.loc[(gz_else.startdate<=date)&(gz_else['到期日']>date),'windcode']
    names_str = namelist2str(names)
    if len(names) == 0:
        continue
    da = date.date().strftime(format='%Y%m%d')
    
    if da < '2015-01-01':
        break
    # get wind df
    err, df= w.wss(names_str, "volume",\
        "tradeDate={};cycle=D".format(int(da)),\
            usedf=True)
    df.columns=[da]
    d[da] = df


# * get zj-else daily volume From Wind
d = pd.DataFrame(index = zj_name_list)
for date in date_list[::-1]:
    print(date)

    # get gz-else namestring on that day market
    names=zj_issue.loc[(zj_issue.startdate<=date)&(zj_issue['到期日']>date),'windcode'].tolist()
    names_str = namelist2str_zj(names)
    # print(names_str)
    if len(names) == 0:
        continue
    da = date.date().strftime(format='%Y%m%d')
    
    if da < '2015-01-01':
        break
    # get wind df
    err, df= w.wss(names_str, "volume",\
        "tradeDate={};cycle=D".format(int(da)),\
            usedf=True)
    df.columns=[da]
    d[da] = df
    