import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False

#### * 资金数据与息差情况
def RepoRate():
    df = do.get_data('cash_amt_prc')
    df.index = df.date

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['R001','R007','R021']].dropna()['2019':].plot(ax=ax,\
        color=['#3778bf','#f0833a','grey'])
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(0.05,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_xlabel('')

    return fig

def rate_1D():
    df = do.get_data('cash_amt_prc')
    df.index = df.date
    df = df['2019':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['R001','GC001']].dropna().plot(ax=ax)
    ax_ = ax.twinx()
    df[['DR001']].plot(ax=ax_,color='grey')
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.05,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.7,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    
    ax.set_xlabel('')
    return fig

def rate_7D():
    df = do.get_data('cash_amt_prc')
    df.index = df.date
    df = df['2019':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['R007','GC007']].dropna().plot(ax=ax)
    ax_ = ax.twinx()
    df[['DR007']].plot(ax=ax_,color='grey')
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.05,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.7,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    
    ax.set_xlabel('')
    return fig

def vol_1D():
    df = do.get_data('cash_amt_prc')
    df.index = df.date
    df = df['2019':].dropna()
    
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date, 0, df['成交量:银行间质押式回购'], \
        label = '成交量:银行间质押式回购',color='lightgrey',alpha=1)
    plt.xticks(rotation=30)
    ax_=ax.twinx()
    df[['R001']].plot(ax=ax_)
    
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.05,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.7,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    
    return fig

def r_dr():
    df = do.get_data('cash_cost')
    df.index = df.date
    df = df['2015':]
    df['R007-DR007'] = df['R007']-df['DR007']

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date, 0, df['R007-DR007'], \
        label = 'R007-DR007',color='lightgrey',alpha=1)
    ax_=ax.twinx()
    df[['R007','DR007']].plot(ax=ax_)

    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.0,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=2,loc=3, bbox_to_anchor=(0.4,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def R_GC_7D():
    df = do.get_data('cash_cost')
    df.index = df.date
    df = df['2016-01':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['R007','GC007']].plot(ax=ax)
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.15,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    
    return fig

def volRatio():
    df = do.get_data('repo_volume')
    df.index = df.date
    df = df['2015':]

    # df['tmp_sum'] = 
    df[['隔夜回购占比','七天回购占比']]=\
        df[['成交量:R001','成交量:R007']].div(df[['成交量:R001','成交量:R007']].sum(axis=1),axis=0)

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date, 0, df['隔夜回购占比'], \
        label = '隔夜回购占比',color='lightgrey',alpha=1)
    ax.fill_between(df.date, 0, df['七天回购占比'], \
        label = '七天回购占比',color='orange',alpha=1)
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.05,-0.45),borderaxespad = 0.,fontsize=10,frameon=False)

    return fig 

def irs():
    df = do.get_data('spreads')
    df.index = df.date
    df = df['2009':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['IRS_1y_FR007', 'IRS_5y_FR007','IRS_5y_shibor3m']].plot(ax=ax)
    ax.set_xlabel('')
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(-0.15,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def cd6M():
    df = do.get_data('spreads')
    cash = do.get_data('cash_cost');cash.index = cash.date
    df.index = df.date
    df = df['2015':]
    df['cd:6M-R007'] = df['cd_AAA_6m']-cash['R007']
    df['R007'] = cash['R007']

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date,0,df['cd:6M-R007'],\
        label='cd:6M-R007',color='lightgrey',alpha=1)
    ax_=ax.twinx()
    df[['R007','cd_AAA_6m']].plot(ax=ax_)
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(-0.05,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=2,loc=3, bbox_to_anchor=(0.35,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig 

def msPaper():
    cash = do.get_data('cash_cost');cash.index=cash.date
    df = do.get_data('spreads')
    df.index = df.date
    df = df['2016':]

    df['1年'] = df['中短票_AA+_1y']-cash['R007']
    df['3年'] = df['中短票_AA+_3y']-cash['R007']
    df['5年'] = df['中短票_AA+_5y']-cash['R007']

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[[ '1年', '3年','5年']].plot(ax=ax)
    ax.set_xlabel('')
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(0.10,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_title('中短票:AA+-R007')
    return fig

def gk_local():
    cash = do.get_data('cash_cost');cash.index=cash.date
    df = do.get_data('spreads')
    df.index = df.date
    df = df['2016':]

    df['国开债:10年-R007'] = df['国开10年']-cash['R007']
    df['地方债:3年:AAA-R007'] = df['地方债_AAA_3y']-cash['R007']

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['国开债:10年-R007','地方债:3年:AAA-R007']].plot(ax=ax,ylim=(-3,3))
    ax.set_xlabel('')
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(-0.05,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)

    return fig 