import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import pandas as pd
import numpy as np
import datetime as dt#准备工作，配置环境。

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime

from pylab import mpl
plt.rcParams['font.family']=['STKaiti']
mpl.rcParams['axes.unicode_minus']=False

import data_organize as do

global rates


def term1():
    # 期限利差1
    # 国债国开7-10
    rates = do.get_data('rates'); rates.index = rates.date
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin1 = rates0['国债10年']-rates0['国债7年']
    margin2 = rates0['国开10年']-rates0['国开7年']
    df = pd.DataFrame([margin1,margin2])
    df.index = ['国债10Y-7Y','国开10Y-7Y']
    df  = df.T
    
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates0['date'],margin1*100,'#3778bf',label="国债10Y-7Y")
    ax.plot(rates0['date'],margin2*100,'#f0833a',label='国开10Y-7Y')
    ax.set_title('期限利差1', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    ax.set_ylim([-30,30])
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（BP）',fontsize=10)
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return df

def term2():
    #绘制期限利差2
    rates = do.get_data('rates'); rates.index = rates.date
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin3 = rates0['国债30年']-rates0['国债10年']
    margin4 = rates0['国债10年']-rates0['国债1年']
    margin5 = rates0['国债3年']-rates0['国债1年']
    df = pd.DataFrame([margin3,margin4,margin5])
    df.index = ['国债30Y-10Y','国开10Y-1Y','国开3Y-1Y']
    df  = df.T
    
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates0['date'],margin3*100,'#3778bf',label="国债30Y-10Y")
    ax.plot(rates0['date'],margin4*100,'#f0833a',label='国开10Y-1Y')
    ax.plot(rates0['date'],margin5*100,'gray',label='国开3Y-1Y')
    ax.set_title('期限利差2', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（BP）',fontsize=10)
    ax.set_ylim([-50,200])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return df

def implicitRate():
    #国开与国债的隐含税率 (1-10年国债/10年国开)
    rates = do.get_data('rates'); rates.index = rates.date
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    tax_rate = 1 - rates0['国债10年']/rates0['国开10年']

    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates0['date'],tax_rate,'#3778bf',label="隐含税率(%)")
    ax.set_title('国开与国债的隐含税率', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([0.05,0.20])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return tax_rate

def gk_nf_kh():
    #绘制国开与非国开的利差
    rates = do.get_data('rates'); rates.index = rates.date
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin6 = rates0['农发10年'] - rates0['国开10年']
    margin7 = rates0['口行10年'] - rates0['国开10年']
    df = pd.DataFrame([margin6,margin7])
    df.index = ['农发10Y-国开10Y','进出口10Y-国开10Y']
    df  = df.T    

    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates0['date'],margin6,'#3778bf',label="农发10Y-国开10Y")
    ax.plot(rates0['date'],margin7,'#f0833a',label='进出口10Y-国开10Y')
    ax.set_title('国开与非国开的利差', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（%）',fontsize=10)
    ax.set_ylim([-0.1,0.5])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return df

def term_gz():
    rates = do.get_data('rates'); rates.index = rates.date    
    rates1 = rates.loc[rates['date'] >= '2007-01-01']
    #计算利差
    margin1 = rates1['国债10年']-rates1['国债1年']
    margin2 = rates1['国债10年']-rates1['国债5年']
    margin3 = rates1['国债3年']-rates1['国债1年']
    df = pd.DataFrame([margin1,margin2,margin3])
    df.index = ['10Y-1Y','10Y-5Y','3Y-1Y']
    df  = df.T    
    #国债期限利差
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates1['date'],margin1,'#3778bf',label="10Y-1Y")
    ax.plot(rates1['date'],margin2,'#f0833a',label='10Y-5Y')
    ax.plot(rates1['date'],margin3,'gray',label='3Y-1Y')
    ax.set_title('国债期限利差', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（%）',fontsize=10)
    ax.set_ylim([-1,3])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return df

def term_10_1():
    #国债、国开债10年-1年
    rates = do.get_data('rates'); rates.index = rates.date    
    rates2 = rates.loc[rates['date'] >= '2008-01-01']
    margin4 = rates2['国债10年']-rates2['国债1年']
    margin5 = rates2['国开10年']-rates2['国开1年']
    df = pd.DataFrame([margin4,margin5])
    df.index = ['国债10Y-1Y','国开10Y-1Y']
    df  = df.T  

    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates2['date'],margin4,'#3778bf',label="国债10Y-1Y")
    ax.plot(rates2['date'],margin5,'#f0833a',label='国开10Y-1Y')
    ax.set_title('国债、国开债10年-1年', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（%）',fontsize=10)
    ax.set_ylim([-1,3])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return df

def termSpots_10_1():
    #绘制国债1年收益率与10年-1年利差
    rates = do.get_data('rates'); rates.index = rates.date       
    rates3 = rates.loc[rates['date'] >= '2009-01-01']
    margin6 = rates3['国债10年']-rates3['国债1年']

    fig,ax =plt.subplots(figsize=(6,4),dpi=300, facecolor='w')
    ax.grid(ls='--')
    plt.rc('axes', axisbelow=True)
    ax.scatter(rates3['国债1年'][:-1],margin6[:-1], marker='o',color = '', edgecolors='#3778bf')
    ax.scatter(rates3['国债1年'][:1],margin6[:1], marker='o',color = '', edgecolors='#f0833a')
    ax.set_title('国债1年收益率与10年-1年利差', fontsize=12)
    ax.annotate('当前值',xy=(rates3['国债1年'][:1],margin6[:1]),xytext=(rates3['国债1年'][:1],margin6[:1]-1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax.set_ylabel('（%）',fontsize=10)
    plt.show()
    return margin6 

def termSpots_30_10():
    #绘制国债10年收益率与30年-10年利差  
    rates = do.get_data('rates'); rates.index = rates.date    
    rates3 = rates.loc[rates['date'] >= '2009-01-01']
    margin7 = rates3['国债30年']-rates3['国债10年']

    fig,ax = plt.subplots(figsize=(6,4),dpi=300, facecolor='w')
    ax.grid(ls='--')
    plt.rc('axes', axisbelow=True)
    ax.scatter(rates3['国债10年'][:-1],margin7[:-1], marker='o',color = '', edgecolors='#3778bf')
    ax.scatter(rates3['国债10年'][:1],margin7[:1], marker='o',color = '', edgecolors='#f0833a')
    ax.set_title('国债10年收益率与30年-10年利差', fontsize=12)
    ax.annotate('当前值',xy=(rates3['国债10年'][:1],margin7[:1]),xytext=(rates3['国债10年'][:1],margin7[:1]-0.1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax.set_ylabel('（%）',fontsize=10)
    plt.show()
    return margin7 

def gz_barbell():
    rates = do.get_data('rates'); rates.index = rates.date      
    rates4 = rates.loc[rates['date'] >= '2015-10-08']
    #国债2*5Y-(1Y+10Y)
    gz = rates4['国债5年']*2 - ( rates4['国债1年'] + rates4['国债10年'])

    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates4['date'],gz,'#3778bf',label="2*5Y-(1Y+10Y)")
    ax.set_title('国债2*5Y-(1Y+10Y)', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([-0.5,1])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax.set_ylabel('（%）',fontsize=10)
    plt.show()
    return gz

def gk_barbell():
    rates = do.get_data('rates'); rates.index = rates.date      
    rates4 = rates.loc[rates['date'] >= '2015-10-08']
    # 国开债2*5Y-(1Y+10Y)
    gkz = rates4['国开5年']*2 - ( rates4['国开1年'] + rates4['国开10年'])
    
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates4['date'],gkz,'#3778bf',label="2*5Y-(1Y+10Y)")
    ax.set_title('国开债2*5Y-(1Y+10Y)', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([-0.5,1.5])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax.set_ylabel('（%）',fontsize=10)
    plt.show()    
    return gkz 

def termSpots_gk_gz():
    #10年期国债与国开债-国债利差
    rates = do.get_data('rates'); rates.index = rates.date 
    rates1 = rates.loc[rates['date'] >= '2009-01-05']
    margin1 = rates1['国开10年']-rates1['国债10年']

    fig,ax = plt.subplots(figsize=(6,4),dpi=300, facecolor='w')
    ax.grid(ls='--')
    plt.rc('axes', axisbelow=True)
    ax.scatter(rates1['国债10年'][:-1],margin1[:-1], marker='o',color = '', edgecolors='#3778bf')
    ax.scatter(rates1['国债10年'][:1],margin1[:1], marker='o',color = '', edgecolors='#f0833a')
    ax.set_title('10年期国债与国开债-国债利差', fontsize=12)
    ax.annotate('当前值',xy=(rates1['国债10年'][:1],margin1[:1]),xytext=(rates1['国债10年'][:1],margin1[:1]+0.5),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax.set_ylabel('（%）',fontsize=10)
    plt.show()   
    return margin1 

def spreads_gk_gz_1d():
    rates = do.get_data('rates'); rates.index = rates.date    
    rates1 = rates.loc[rates['date'] >= '2009-01-05']
    rates1.index = rates1['date']
    keymargin1 = rates1[['国债6月', '国债1年', '国债3年','国债5年', '国债7年', '国债10年']]
    keymargin1.columns = ['6M', '1Y', '3Y','5Y', '7Y', '10Y']
    keymargin2 = rates1[['国开6月', '国开1年', '国开3年','国开5年', '国开7年', '国开10年']]
    keymargin2.columns = ['6M', '1Y', '3Y','5Y', '7Y', '10Y']
    keymargin = pd.concat([keymargin1[-1:],keymargin2[-1:]],axis=0)
    keymargin.index = ['国债', '国开债']
    keymargin= pd.DataFrame(keymargin.values.T, index=keymargin.columns, columns=keymargin.index)
    keymargin['国开债-国债'] = (keymargin['国开债'] - keymargin['国债'])*100

    #国开债-国债关键期限利差
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(keymargin.index,keymargin['国债'],'#3778bf',label="国债")
    ax.plot(keymargin.index,keymargin['国开债'],'#f0833a',label='国开债')
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([1.5,4])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax.set_ylabel('（%）',fontsize=10)
    
    ax_=ax.twinx()
    ax_.bar(keymargin.index,keymargin['国开债-国债'], width=0.7, color='gray',alpha = 0.2,label='国开债-国债')
    ax_.set_ylim([0,50])
    ax_.legend(ncol=3,loc=1,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    ax_.set_title('国开债-国债关键期限利差', fontsize=12)
    plt.show()    
    return keymargin

def nf_kh_gk_10y():
    rates = do.get_data('rates'); rates.index = rates.date    
    rates2 = rates.loc[rates['date'] >= '2016-01-04']
    rates2.index = rates2['date']
    rates2 = rates2[['国开10年', '农发10年', '口行10年']]
    rates2['农发-国开'] = (rates2['农发10年'] - rates2['国开10年'])*100
    rates2['口行-国开'] = (rates2['口行10年'] - rates2['国开10年'])*100

    #农发、口行-国开利差:10年
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates2.index,rates2['国开10年'],'#3778bf',label="国开10年",linewidth=1)
    ax.plot(rates2.index,rates2['农发10年'],'#f0833a',label='农发10年',linewidth=1)
    ax.plot(rates2.index,rates2['口行10年'],'gray',label='口行10年',linewidth=1)
    ax.set_ylim([2.5,6])
    ax.legend(ncol=1,loc=2,fontsize=10,frameon=False)
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（%）',fontsize=10)

    ax_=ax.twinx()
    ax_.bar(rates2.index,rates2['农发-国开'], width=1, color='#f0833a',alpha = 0.2,label='农发-国开')
    ax_.bar(rates2.index,rates2['口行-国开'], width=1, color='gray',alpha = 0.2,label='口行-国开')
    ax_.set_ylim([0,40])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    ax_.set_title('农发、口行-国开利差:10年', fontsize=12)
    plt.show()
    return rates2

def new_gk_old():
    secondary_rate_sec = do.get_data('secondary_rate_sec')
    #筛选200205
    secondary_rate_sec1 = secondary_rate_sec.loc[secondary_rate_sec['代码'] == '200205.IB']
    a = secondary_rate_sec1.groupby(['date'])['价格'].mean()
    #筛选200210
    secondary_rate_sec1 = secondary_rate_sec.loc[secondary_rate_sec['代码'] == '200210.IB']
    b = secondary_rate_sec1.groupby(['date'])['价格'].mean()
    df = pd.concat([a,b],axis=1)
    df.columns = ['200205','200210']
    df['200205-200210'] = (df['200205'] - df['200210'])*100

    date = df.index
    date = date.strftime('%m-%d') 
    df.index = date
    tick_spacing = 5

    #国开债新老券利差
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(df.index,df['200205'],'#3778bf',label="200205")
    ax.plot(df.index,df['200210'],'#f0833a',label='200210')
    ax.set_ylim([3,4])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.set_ylabel('（%）',fontsize=10)

    ax_=ax.twinx()
    ax_.bar(df.index,df['200205-200210'], width=1, color='gray',alpha = 0.2,label='200205-200210')
    ax_.set_ylim([-1.5,1])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    ax_.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax_.set_title('国开债新老券利差', fontsize=12)
    plt.show()      
    return df

def creditSpreads():
    rates = do.get_data('rates'); rates.index = rates.date  
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y','中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y', '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05']
    credit1  = rates1[-1:]
    credit2 = rates1.describe()[4:7]
    credit3 = rates1.loc[rates1.index == '2020-12-31']
    credit = pd.concat([credit1,credit2,credit3],axis=0)
    credit.index = [['现值','25分位数','中位数','75分位数','2020年底']]
    #转置
    credit= pd.DataFrame(credit.values.T, index=credit.columns, columns=credit.index)
    #信用利差水平
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(credit[['现值']],'#3778bf',label="现值")
    ax.plot(credit[['25分位数']],'#f0833a',label='25分位数')
    ax.plot(credit[['中位数']],'gray',label='中位数')
    ax.plot(credit[['75分位数']],'tomato',label='75分位数')
    ax.plot(credit[['2020年底']],'yellow',label='2020年底')
    ax.set_ylabel('（%）',fontsize=10)
    ax.set_title('信用利差水平', fontsize=12)
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return credit 

def gradeSpreads():
    rates = do.get_data('rates'); rates.index = rates.date 
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y','中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y', '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05']
    #分评级信用利差
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates1.index,rates1['中票_AAA_1y'],'#3778bf',label="AAA1年")
    ax.plot(rates1.index,rates1['中票_AAA_5y'],'#f0833a',label='AAA5年')
    ax.plot(rates1.index,rates1['中票_AA+_1y'],'gray',label='AA+1年')
    ax.plot(rates1.index,rates1['中票_AA+_5y'],'tomato',label='AA+5年')

    ax.set_title('分评级信用利差', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([1.5,6.5])
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    plt.show()
    return rates1 

def spreads_cn_us_10y():
    rates = do.get_data('rates'); rates.index = rates.date
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    #计算利差
    margin1 = (rates1['国债10年']-rates_us1['美债10年']) * 100
    df = pd.DataFrame([rates1['国债10年'],rates_us1['美债10年'],margin1])
    df.index = ['国债10年','美债10年','中美利差10年']
    df  = df.T

    #中美利差:10年
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates1['date'],rates1['国债10年'],'#3778bf',label="国债10年")
    ax.plot(rates_us1['date'],rates_us1['美债10年'],'#f0833a',label='美债10年')
    ax.set_ylabel('（%）',fontsize=10)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([0,6])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    
    ax_=ax.twinx()
    ax_.bar(margin1.index,margin1, width=1, color='gray',alpha = 0.2,label='中美利差10年')
    ax_.set_ylim([0,300])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:10年', fontsize=12)
    plt.show()
    return df

def spreads_cn_us_2y():
    rates = do.get_data('rates'); rates.index = rates.date
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    #计算利差
    margin2 = (rates1['国债2年']-rates_us1['美债2年']) * 100
    df = pd.DataFrame([rates1['国债2年'],rates_us1['美债2年'],margin2])
    df.index = ['国债2年','美债2年','中美利差2年']
    df  = df.T

    #中美利差:10年
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates1['date'],rates1['国债2年'],'#3778bf',label="国债2年")
    ax.plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label='美债2年')
    ax.set_ylabel('（%）',fontsize=10)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([0,5])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    
    ax_=ax.twinx()
    ax_.bar(margin2.index,margin2, width=1, color='gray',alpha = 0.2,label='中美利差2年')
    ax_.set_ylim([-50,500])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:2年', fontsize=12)
    plt.show()
    return df

def spreads_cn_us_1y():
    rates = do.get_data('rates'); rates.index = rates.date
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    #计算利差
    margin3 = (rates1['国债1年']-rates_us1['美债1年']) * 100
    df = pd.DataFrame([rates1['国债1年'],rates_us1['美债1年'],margin3])
    df.index = ['国债1年','美债1年','中美利差1年']
    df  = df.T

    #中美利差:10年
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates1['date'],rates1['国债1年'],'#3778bf',label="国债1年")
    ax.plot(rates_us1['date'],rates_us1['美债1年'],'#f0833a',label='美债1年')
    ax.set_ylabel('（%）',fontsize=10)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([-0.5,5])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    
    ax_=ax.twinx()
    ax_.bar(margin3.index,margin3, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    ax_.set_ylim([-50,500])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:1年', fontsize=12)
    plt.show()
    return df

def spreads_exchange():
    rates = do.get_data('rates'); rates.index = rates.date  
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates2 = rates.loc[rates['date'] >= '2011-01-04']
    rates2.index = rates2['date']
    rates_us2 = rates_us.loc[rates_us['date'] >= '2011-01-04']
    rates_us2.index = rates_us2['date']
    #计算利差
    margin4 = (rates2['国债10年']-rates_us2['美债10年']) * 100
    df = pd.DataFrame([rates_us2['美元兑人民币'],margin4])
    df.index = ["美元兑人民币","中美利差10年"]
    df = df.T
    
    #中美利差与人民币汇率
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates_us2['date'],rates_us2['美元兑人民币'],'#3778bf',label="美元兑人民币")
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylim([5,8])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)

    ax_=ax.twinx()
    ax_.plot(margin4.index,margin4,'#f0833a',label="中美利差10年")
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差与人民币汇率', fontsize=12)
    ax_.set_ylim([0,300])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    plt.show()   
    return df 

def spreads_cn_us_mkt():
    cash_cost = do.get_data('cash_cost');cash_cost.index = cash_cost.date
    rates = do.get_data('rates'); rates.index = rates.date
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    cash_cost1 = cash_cost.loc[cash_cost['date'] >= '2010-06-21']
    cash_cost1.index = cash_cost1['date']
    #计算利差
    margin5 = (cash_cost1['shibor_3m']-rates_us1['libor_3m']) * 100
    df = pd.DataFrame([rates_us1['libor_3m'],cash_cost1['shibor_3m'],margin5])
    df.index = ["美元libor3个月",'人民币shibor3个月','中美利差1年']
    df  = df.T
    
    #中美市场利差
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates_us1['date'],rates_us1['libor_3m'],'#3778bf',label="美元libor3个月")
    ax.plot(cash_cost1['date'],cash_cost1['shibor_3m'],'#f0833a',label='人民币shibor3个月')
    ax.set_ylim([0,8])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（%）',fontsize=10)
    
    ax_=ax.twinx()
    ax_.bar(margin5.index,margin5, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_ylim([0,700])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_title('中美市场利差', fontsize=12)
    plt.show()   
    return df 

def termUS():
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    margin6 = (rates_us1['美债10年']-rates_us1['美债2年']) * 100    
    df = pd.DataFrame([rates_us1['美债10年'],rates_us1['美债2年'],margin6])
    df.index = ["美债10年",'美债2年','美债10-2年']
    df  = df.T
    
    #美债期限利差
    fig,ax = plt.subplots(figsize=(6,4),dpi = 300)
    ax.plot(rates_us1['date'],rates_us1['美债10年'],'#3778bf',label="美债10年")
    ax.plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label="美债2年")
    ax.set_ylim([0,4.5])
    ax.legend(ncol=3,loc=2,fontsize=10,frameon=False)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    ax.set_ylabel('（%）',fontsize=10)
    
    ax_=ax.twinx()
    ax_.bar(margin6.index,margin6, width=1, color='gray',alpha = 0.2,label='美债10-2年')
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_ylim([0,400])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_title('美债期限利差', fontsize=12)
    plt.show()   
    return df

