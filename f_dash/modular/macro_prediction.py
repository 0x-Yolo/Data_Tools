# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 09:29:35 2020

@author: User
"""


import re
import sys
import datetime as dt
import pandas as pd
import numpy as np
import  pymysql

#导入plotly库
import plotly.express as px
import plotly.graph_objects as go

#导入模型库
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.stattools as st
from statsmodels.tsa.arima_model import ARMA,ARIMA
from itertools import product


#
from datetime import datetime
#
sys.path.append('C:/Users/User/Desktop/tpy/Data_Tools/f_dash/modular')
import db_management.data_organize as do

#%%
def change_freq(df,freq = 'M',how = 'mean', percent = None):
    '''
    变频并计算同/环比。注意index必须为pd.DatetimeIndex

    Parameters
    ----------
    df : pandas df
        需要转换频率的变量.
    freq : TYPE, optional
        想要转换的频率. 默认'M'，可选'W','M','Y'
    how : method, optional
        想要聚合的方法. 默认'mean'，详情见dir(df.resample('M'))
    percent : method, optional
        是否转换成同比或环比. 默认'None'，可选'mom','yoy'
    Returns
    -------
    df2 : 需要转换频率的变量

    '''
    df.index = pd.DatetimeIndex(df.index)
    df2 = df.resample(freq).agg([how])
    d = {'W':'周','M':'月','Y':'年'}
    df2.columns = [i+':'+d[freq] for i in df.columns]
    if percent == 'mom':
        df3 = (df2-df2.shift(1))*100/df2.shift(1)
        df3.columns = [i+':环比' for i in df2.columns]
        return df3
    elif percent == 'yoy':
        df3 = (df2-df2.shift(12))*100/df2.shift(2)
        df3.columns = [i+':同比' for i in df2.columns]
        return df3
    else:
        return df2

#%%
def add_SF(df):
    '''
    给回归变量添加春节哑变量。
    df的index一定要是date。
    '''
    df['春节'] = 0
    df.loc['2011-02-28','春节']= 1
    df.loc['2012-01-31','春节']= 1
    df.loc['2013-02-28','春节']= 1
    df.loc['2014-01-31','春节']= 1
    df.loc['2015-02-28','春节']= 1
    df.loc['2016-02-29','春节']= 1
    df.loc['2017-01-31','春节']= 1
    df.loc['2018-02-28','春节']= 1 
    df.loc['2019-02-28','春节']= 1
    df.loc['2020-01-31','春节']= 1     

    return df

#%%

def seasonal(series):
    '''
    用历史每个月的平均值计算季节项，并返回序列的季节项。

    '''
    series.index = pd.DatetimeIndex(series.index)
    sea = pd.Series(0,index = series.index)
    for i in range(1,13):
        data_month = series[series.index.month == i]
        n = len(data_month)
        weights = np.arange(1,n+1)/(n*(n+1)/2)
        sea[sea.index.month == i] = np.average(np.asarray(data_month,'float32'), weights=weights)
    return sea



