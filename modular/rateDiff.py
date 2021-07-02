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

cash_cost = do.get_data('cash_cost');cash_cost.index = cash_cost.date
rates = do.get_data('rates'); rates.index = rates.date
rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
rates0 = rates.loc[rates['date'] >= '2019-01-01']
#计算利差
margin1 = rates0['国债7年']-rates0['国债10年']
margin2 = rates0['国开7年']-rates0['国开10年']
margin3 = rates0['国债30年']-rates0['国债10年']
margin4 = rates0['国债10年']-rates0['国债1年']
margin5 = rates0['国债3年']-rates0['国债1年']
margin6 = rates0['国开10年']-rates0['农发10年']
margin7 = rates0['国开10年']-rates0['口行10年']

def term1():
    # 期限利差1
    # 国债国开7-10
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates0['date'],margin1*100,'#3778bf',label="国债7Y-10Y")
    plt.plot(rates0['date'],margin2*100,'#f0833a',label='国开7Y-10Y')

    plt.title('期限利差1', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.08,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def term2():
    #绘制期限利差2
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates0['date'],margin3*100,'#3778bf',label="国债30Y-10Y")
    plt.plot(rates0['date'],margin4*100,'#f0833a',label='国开10Y-1Y')
    plt.plot(rates0['date'],margin5*100,'gray',label='国开3Y-1Y')

    plt.title('期限利差2', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.1,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def implicitRate():
    tax_rate = 1 - rates0['国债10年']/rates0['国开10年']
    #国开与国债的隐含税率 (1-10年国债/10年国开)
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates0['date'],tax_rate,'#3778bf',label="隐含税率(%)")

    plt.title('国开与国债的隐含税率', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.3,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def gk_nf_kh():
    #绘制国开与非国开的利差
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates0['date'],margin6,'#3778bf',label="国开10Y-农发10Y")
    plt.plot(rates0['date'],margin7,'#f0833a',label='国开10Y-进出口10Y')

    plt.title('国开与非国开的利差', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def term_gz():
    rates1 = rates.loc[rates['date'] >= '2007-01-01']
    #计算利差
    margin1 = rates1['国债10年']-rates1['国债1年']
    margin2 = rates1['国债10年']-rates1['国债5年']
    margin3 = rates1['国债3年']-rates1['国债1年']
    #国债期限利差
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates1['date'],margin1,'#3778bf',label="10Y-1Y")
    plt.plot(rates1['date'],margin2,'#f0833a',label='10Y-5Y')
    plt.plot(rates1['date'],margin3,'gray',label='3Y-1Y')

    plt.title('国债期限利差', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.05,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def term_10_1():
    rates2 = rates.loc[rates['date'] >= '2008-01-01']
    margin4 = rates2['国债10年']-rates2['国债1年']
    margin5 = rates2['国开10年']-rates2['国开1年']

    #国债、国开债10年-1年
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates2['date'],margin4,'#3778bf',label="国债")
    plt.plot(rates2['date'],margin5,'#f0833a',label='国开债')

    plt.title('国债、国开债10年-1年', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.25,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def termSpots_10_1():
    rates3 = rates.loc[rates['date'] >= '2009-01-01']
    margin6 = rates3['国债10年']-rates3['国债1年']

    #绘制国债1年收益率与10年-1年利差
    fig,ax =plt.subplots(figsize=(10,4),dpi=300, facecolor='w')
    plt.grid(ls='--')
    plt.rc('axes', axisbelow=True)
    plt.scatter(rates3['国债1年'][:-1],margin6[:-1], marker='o',color = '', edgecolors='#3778bf')
    plt.scatter(rates3['国债1年'][:1],margin6[:1], marker='o',color = '', edgecolors='#f0833a')
    plt.title('国债1年收益率与10年-1年利差', fontsize=12)
    plt.annotate('当前值',xy=(rates3['国债1年'][:1],margin6[:1]),xytext=(rates3['国债1年'][:1],margin6[:1]-1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)

    return fig 

def termSpots_30_10():
    rates3 = rates.loc[rates['date'] >= '2009-01-01']
    margin7 = rates3['国债30年']-rates3['国债10年']

    #绘制国债10年收益率与30年-10年利差
    fig,ax = plt.subplots(figsize=(10,4),dpi=300, facecolor='w')
    plt.grid(ls='--')
    plt.rc('axes', axisbelow=True)
    plt.scatter(rates3['国债10年'][:-1],margin7[:-1], marker='o',color = '', edgecolors='#3778bf')
    plt.scatter(rates3['国债10年'][:1],margin7[:1], marker='o',color = '', edgecolors='#f0833a')
    plt.title('国债10年收益率与30年-10年利差', fontsize=12)
    plt.annotate('当前值',xy=(rates3['国债10年'][:1],margin7[:1]),xytext=(rates3['国债10年'][:1],margin7[:1]-0.1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    plt.savefig('国债10年收益率与30年-10年利差.jpg', dpi=300, bbox_inches = 'tight')

    return fig

def gz_barbell():
    rates4 = rates.loc[rates['date'] >= '2015-10-08']
    # 计算2*5Y-(1Y+10Y)
    gz = rates4['国债5年']*2 - ( rates4['国债1年'] + rates4['国债10年'])
    gkz = rates4['国开5年']*2 - ( rates4['国开1年'] + rates4['国开10年'])
    
    #国债2*5Y-(1Y+10Y)
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates4['date'],gz,'#3778bf',label="2*5Y-(1Y+10Y)")

    plt.title('国债2*5Y-(1Y+10Y)', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.25,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def gk_barbell():
    # 国开债2*5Y-(1Y+10Y)
    rates4 = rates.loc[rates['date'] >= '2015-10-08']
    # 计算2*5Y-(1Y+10Y)
    gz = rates4['国债5年']*2 - ( rates4['国债1年'] + rates4['国债10年'])
    gkz = rates4['国开5年']*2 - ( rates4['国开1年'] + rates4['国开10年'])
    
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates4['date'],gkz,'#3778bf',label="2*5Y-(1Y+10Y)")

    plt.title('国开债2*5Y-(1Y+10Y)', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.25,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig 

def termSpots_gk_gz():
    rates1 = rates.loc[rates['date'] >= '2009-01-05']
    margin1 = rates1['国开10年']-rates1['国债10年']
    #10年期国债与国开债-国债利差
    fig,ax = plt.subplots(figsize=(10,4),dpi=300, facecolor='w')
    plt.grid(ls='--')
    plt.rc('axes', axisbelow=True)
    plt.scatter(rates1['国债10年'][:-1],margin1[:-1], marker='o',color = '', edgecolors='#3778bf')
    plt.scatter(rates1['国债10年'][:1],margin1[:1], marker='o',color = '', edgecolors='#f0833a')
    plt.title('10年期国债与国开债-国债利差', fontsize=12)
    plt.annotate('当前值',xy=(rates1['国债10年'][:1],margin1[:1]),xytext=(rates1['国债10年'][:1],margin1[:1]+0.5),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    return fig 

def spreads_gk_gz_1d():
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
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(keymargin.index,keymargin['国债'],'#3778bf',label="国债")
    plt.plot(keymargin.index,keymargin['国开债'],'#f0833a',label='国开债')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)

    plt.twinx()
    plt.bar(keymargin.index,keymargin['国开债-国债'], width=0.7, color='gray',alpha = 0.2,label='国开债-国债')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.6,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    plt.title('国开债-国债关键期限利差', fontsize=12)

    return fig

def nf_kh_gk_10y():
    rates2 = rates.loc[rates['date'] >= '2016-01-04']
    rates2.index = rates2['date']
    rates2 = rates2[['国开10年', '农发10年', '口行10年']]
    rates2['农发-国开'] = (rates2['农发10年'] - rates2['国开10年'])*100
    rates2['口行-国开'] = (rates2['口行10年'] - rates2['国开10年'])*100

    #农发、口行-国开利差:10年
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates2.index,rates2['国开10年'],'#3778bf',label="国开10年",linewidth=1)
    plt.plot(rates2.index,rates2['农发10年'],'#f0833a',label='农发10年',linewidth=1)
    plt.plot(rates2.index,rates2['口行10年'],'gray',label='口行10年',linewidth=1)
    plt.legend(ncol=1,loc=3, bbox_to_anchor=(0.1,-1),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)

    plt.twinx()
    plt.bar(rates2.index,rates2['农发-国开'], width=1, color='#f0833a',alpha = 0.2,label='农发-国开')
    plt.bar(rates2.index,rates2['口行-国开'], width=1, color='gray',alpha = 0.2,label='口行-国开')
    plt.legend(ncol=1,loc=3, bbox_to_anchor=(0.6,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    plt.title('农发、口行-国开利差:10年', fontsize=12)

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

    #国开债新老券利差
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(df.index,df['200205'],'#3778bf',label="200205")
    plt.plot(df.index,df['200210'],'#f0833a',label='200210')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0,-0.9),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.xticks(fontsize=10 ,rotation=45)
    plt.yticks(fontsize=10,rotation=0)

    plt.twinx()
    plt.bar(df.index,df['200205-200210'], width=1, color='gray',alpha = 0.2,label='200205-200210')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.6,-0.9),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    plt.title('国开债新老券利差', fontsize=12)

    return fig 

def creditSpreads():
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
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(credit[['现值']],'#3778bf',label="现值")
    plt.plot(credit[['25分位数']],'#f0833a',label='25分位数')
    plt.plot(credit[['中位数']],'gray',label='中位数')
    plt.plot(credit[['75分位数']],'tomato',label='75分位数')
    plt.plot(credit[['2020年底']],'yellow',label='2020年底')

    plt.title('信用利差水平', fontsize=12)
    plt.xticks(fontsize=10 ,rotation=45)
    #
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=5,loc=3, bbox_to_anchor=(-0.15,-1),borderaxespad = 0.,fontsize=10,frameon=False)

    return fig 

def gradeSpreads():
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y','中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y', '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05']
    #分评级信用利差
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates1.index,rates1['中票_AAA_1y'],'#3778bf',label="AAA1年")
    plt.plot(rates1.index,rates1['中票_AAA_5y'],'#f0833a',label='AAA5年')
    plt.plot(rates1.index,rates1['中票_AA+_1y'],'gray',label='AA+1年')
    plt.plot(rates1.index,rates1['中票_AA+_5y'],'tomato',label='AA+5年')

    plt.title('分评级信用利差', fontsize=12)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.legend(ncol=4,loc=3, bbox_to_anchor=(-0.15,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)

    return fig 

def spreads_cn_us_2y():
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    #计算利差
    margin1 = (rates1['国债10年']-rates_us1['美债10年']) * 100
    margin2 = (rates1['国债2年']-rates_us1['美债2年']) * 100
    margin3 = (rates1['国债1年']-rates_us1['美债1年']) * 100
    #中美利差:10年
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates1['date'],rates1['国债10年'],'#3778bf',label="国债10年")
    plt.plot(rates_us1['date'],rates_us1['美债10年'],'#f0833a',label='美债10年')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.1,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.ylabel('（%）',fontsize=10)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.twinx()
    plt.bar(margin1.index,margin1, width=1, color='gray',alpha = 0.2,label='中美利差10年')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.65,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.ylabel('（BP）',fontsize=10)
    plt.title('中美利差:10年', fontsize=12)
    return fig 

def spreads_cn_us_1y():
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    #计算利差
    margin1 = (rates1['国债10年']-rates_us1['美债10年']) * 100
    margin2 = (rates1['国债2年']-rates_us1['美债2年']) * 100
    margin3 = (rates1['国债1年']-rates_us1['美债1年']) * 100
    #中美利差:1年
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates1['date'],rates1['国债1年'],'#3778bf',label="国债1年")
    plt.plot(rates_us1['date'],rates_us1['美债1年'],'#f0833a',label='美债1年')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.1,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.ylabel('（%）',fontsize=10)
    plt.twinx()
    plt.bar(margin3.index,margin3, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.65,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.title('中美利差:1年', fontsize=12)
    return fig 

def spreads_exchange():
    rates2 = rates.loc[rates['date'] >= '2011-01-04']
    rates2.index = rates2['date']
    rates_us2 = rates_us.loc[rates_us['date'] >= '2011-01-04']
    rates_us2.index = rates_us2['date']
    #计算利差
    margin4 = (rates2['国债10年']-rates_us2['美债10年']) * 100
    #中美利差与人民币汇率
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates_us2['date'],rates_us2['美元兑人民币'],'#3778bf',label="美元兑人民币")
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.1,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)

    plt.twinx()
    plt.plot(margin4.index,margin4,'#f0833a',label="中美利差10年")
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.5,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.title('中美利差与人民币汇率', fontsize=12)
    return fig 

def spreads_cn_us_mkt():
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    cash_cost1 = cash_cost.loc[cash_cost['date'] >= '2010-06-21']
    cash_cost1.index = cash_cost1['date']
    #计算利差
    margin5 = (cash_cost1['shibor_3m']-rates_us1['libor_3m']) * 100
    #中美市场利差
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates_us1['date'],rates_us1['libor_3m'],'#3778bf',label="美元libor3个月")
    plt.plot(cash_cost1['date'],cash_cost1['shibor_3m'],'#f0833a',label='人民币shibor3个月')
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.3,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)

    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.ylabel('（%）',fontsize=10)
    plt.twinx()
    plt.bar(margin5.index,margin5, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.8,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.title('中美市场利差', fontsize=12)
    return fig 

def termUS():
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    cash_cost1 = cash_cost.loc[cash_cost['date'] >= '2010-06-21']
    cash_cost1.index = cash_cost1['date']
    margin6 = (rates_us1['美债10年']-rates_us1['美债2年']) * 100
    #美债期限利差
    fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
    plt.plot(rates_us1['date'],rates_us1['美债10年'],'#3778bf',label="美债10年")
    plt.plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label="美债2年")
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.1,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)

    plt.xticks(fontsize=10,rotation=45)
    plt.yticks(fontsize=10,rotation=0)
    plt.ylabel('（%）',fontsize=10)
    plt.twinx()
    plt.bar(margin6.index,margin6, width=1, color='gray',alpha = 0.2,label='美债10-2年')
    plt.ylabel('（BP）',fontsize=10)
    plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.7,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    plt.title('美债期限利差', fontsize=12)

    return fig 

