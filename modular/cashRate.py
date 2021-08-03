import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False

#### * 资金数据与息差情况
def RepoRate(start='2019-01-01',end='2099-05-29'):
    df = do.get_data('cash_amt_prc',start,end)
    df.index = df.date
    df = df[['R001','R007','R021']]
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['R001','R007','R021']].dropna()['2019':].plot(ax=ax,\
        color=['#3778bf','#f0833a','grey'])
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(0.2,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_xlabel('')
    ax.set_title('质押式回购资金利率')
    plt.show()
    return df

def cashrate_1D(start='2019-01-01',end='2099-05-29'):
    df = do.get_data('cash_amt_prc',start,end)
    df.index = df.date
    df = df[['R001','GC001','DR001',]]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['DR001','GC001']].dropna().plot(ax=ax)
    # ax_ = ax.twinx()
    # df[['DR001']].plot(ax=ax_,color='grey')
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.2,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    # ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.7,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    
    ax.set_title('隔夜利率')
    plt.show()
    
    return df

def cashrate_7D(start='2019-01-01',end='2099-05-29'):
    df = do.get_data('cash_amt_prc',start,end)
    df.index = df.date
    df = df[['R007','GC007','DR007',]]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['DR007','GC007']].dropna().plot(ax=ax)
    # ax_ = ax.twinx()
    # df[['DR007']].plot(ax=ax_,color='grey')
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.2,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.7,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    
    ax.set_title('7天资金利率')
    ax.set_xlabel('')
    plt.show()
    
    return df

def vol_1D(start='2019-01-01',end='2099-05-29'):
    df = do.get_data('cash_amt_prc',start,end)
    df.index = df.date
    df = df[['成交量:银行间质押式回购','R001','date']]
    
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date, 0, df['成交量:银行间质押式回购'], \
        label = '成交量:银行间质押式回购',color='lightgrey',alpha=1)
    plt.xticks(rotation=30)
    ax_=ax.twinx()
    df[['R001']].plot(ax=ax_)
    
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.2,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.7,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_title('隔夜成交量')
    plt.show()
    
    return df

def r_dr_7D(start='2015-01-01'):
    df = do.get_data('cash_cost',start)
    df.index = df.date
    df = df['2015':]
    df['R007-DR007'] = (df['R007']-df['DR007'])*100
    df = df[['R007','DR007','R007-DR007','date']]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date, 0, df['R007-DR007'], \
        label = 'R007-DR007(左,BP)',color='lightgrey',alpha=1)
    ax_=ax.twinx()
    df[['R007','DR007']].plot(ax=ax_)
    ax.set_title('R007-DR007')
    ax.legend(loc=2,frameon=False)
    ax_.legend(loc=1,ncol=2,frameon=False)
    # ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.1,-0.2),borderaxespad = 0.,fontsize=10,frameon=False)
    # ax_.legend(ncol=2,loc=3, bbox_to_anchor=(0.5,-0.2),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.show()
    
    return df

def r_gc_7D(start='2016-01',end='2099-05-29'):
    df = do.get_data('cash_cost',start,end)
    df.index = df.date
    df = df[['R007','GC007']]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['R007','GC007']].plot(ax=ax,alpha=0.8)
    ax.set_xlabel('')
    ax.set_title('银行间与交易所资金利率')
    ax.legend(loc=9,ncol=2,frameon=False)
    # ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.25,-0.2),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.show()
    
    return df

def repoVolRatio(start='2015-01-01',end='2099-05-29'):
    df = do.get_data('repo_volume',start,end)
    df.index = df.date

    # df['tmp_sum'] = 
    df[['隔夜回购占比','七天回购占比']]=\
        df[['成交量:R001','成交量:R007']].div(df[['成交量:银行间质押式回购']].sum(axis=1),axis=0)
    df = df[['隔夜回购占比','七天回购占比','date']]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date, 0, df['隔夜回购占比'], \
        label = '隔夜回购占比(R001)',color='lightgrey',alpha=1)
    ax.fill_between(df.date, 0, df['七天回购占比'], \
        label = '七天回购占比(R007)',color='orange',alpha=1)
    ax.legend(ncol=2,loc=0,frameon=False)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    # ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.2,-0.2),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_title('隔夜与七天')
    plt.show()
    
    return df

def irs(start='2009-01-01',end='2099-05-29'):
    df = do.get_data('spreads',start,end)
    df.index = df.date
    df = df[['IRS_1y_FR007', 'IRS_5y_FR007','IRS_5y_shibor3m']].dropna()

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['IRS_1y_FR007', 'IRS_5y_FR007','IRS_5y_shibor3m']].plot(ax=ax,\
        ylim=(0,7),color=['#3778bf','#f0833a','grey'])
    ax.set_xlabel('')
    ax.legend(['IRS:1年(FR007)','IRS:5年(FR007)','IRS:5年(3M SHIBOR)'],\
        ncol=2,loc=9,frameon=False)
    # ax.legend(ncol=3,loc=3, bbox_to_anchor=(0.05,-0.25),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_title('IRS')
    plt.show()
    
    return df

def cd6M(start='2015-01-01',end='2099-05-29'):
    df = do.get_data('spreads',start,end)
    cash = do.get_data('cash_cost');cash.index = cash.date
    df.index = df.date
    df['cd:6M-R007'] = (df['cd_AAA_6m']-cash['R007'])*100
    df['R007'] = cash['R007']
    df = df[['cd:6M-R007','cd_AAA_6m','R007','date']]
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date,0,df['cd:6M-R007'],\
        label='同业存单:6个月-R007(左:BP)',color='lightgrey',alpha=1)
    ax.set_ylim([-300,300])
    ax_=ax.twinx()
    df[['R007','cd_AAA_6m']].plot(ax=ax_,ylim=(0,8),\
        label=['R007','同业存单:6个月:AAA'],color=['#3778bf','#f0833a'])
    ax.legend(loc=2,frameon=False)
    ax_.legend(['R007','同业存单:6个月:AAA'],loc=1,ncol=1,frameon=False)
    # ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.1,-0.2),borderaxespad = 0.,fontsize=10,frameon=False)
    # ax_.legend(ncol=2,loc=3, bbox_to_anchor=(0.4,-0.2),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_title('6M存单-R007')
    plt.show()
    
    return df

def msPaper(start='2016-01-01',end='2099-05-29'):
    cash = do.get_data('cash_cost');cash.index=cash.date
    df = do.get_data('spreads',start,end)
    df.index = df.date

    df['1年'] = df['中短票_AA+_1y']-cash['R007']
    df['3年'] = df['中短票_AA+_3y']-cash['R007']
    df['5年'] = df['中短票_AA+_5y']-cash['R007']
    df = df[[ '1年', '3年','5年']]
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[[ '1年', '3年','5年']].plot(ax=ax,color=['#3778bf','#f0833a','grey'],ylim=(-3,4))
    ax.set_xlabel('')
    ax.legend(ncol=3,loc=9,frameon=False)
    ax.set_title('中短票:AA+-R007')
    plt.show()
    
    return df

def gk_local(start='2016-01-01',end='2099-05-29'):
    cash = do.get_data('cash_cost');cash.index=cash.date
    df = do.get_data('spreads',start,end)
    df.index = df.date

    df['国开债:10年-R007'] = (df['国开10年']-cash['R007'])
    df['地方债:3年:AAA-R007'] = (df['地方债_AAA_3y']-cash['R007'])

    df = df[['国开债:10年-R007','地方债:3年:AAA-R007']]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['国开债:10年-R007','地方债:3年:AAA-R007']].plot(ax=ax,color=['#3778bf','#f0833a'],ylim=(-3,3))
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=9 ,frameon=False)
    ax.set_title('国开10年与地方债3年-R007')
    plt.show()
    
    return df

def cd_mlf(start='2020-01-01' , end = '2099-05-29'):
    interbank_deposit = do.get_data('interbank_deposit',start,end)
    interbank_deposit.index = interbank_deposit.date

    plt.style.use({'font.size' : 10})     
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.grid(ls='--', axis='y')
    ax.set_axisbelow(True)
    ax.plot(interbank_deposit[['存单_股份行_1y']],'#3778bf',label="1年股份行存单利率")
    # ax.scatter(interbank_deposit.index,interbank_deposit['MLF：1y'],\
    #     label='MLF利率：1年', marker='o',color = '#f0833a',s=10)
    interbank_deposit['MLF：1y'].fillna(method='ffill').\
        plot(ls='--',color = '#f0833a', lw=1.5)
    ax.set_ylim([1.5,3.75])
    # ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.5,-0.18),borderaxespad = 0.)  
    ax.legend(ncol=2,loc=9,frameon=False,)
    ax.set_xlabel('')
    ax.set_title('MLF与同业存单')
    plt.show()
            
    return df[['存单_股份行_1y','MLF：1y']]


