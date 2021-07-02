import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False

#### * 利率水平
def yieldCurve(bond='gz'):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2007':]

    today = df.index[-1]
    base = df['2020':'2020'].index[-1]

    if bond=='gz':
        name = '国债'  
    elif bond=='gk':
        name = '国开'
    else:
        print('error')
        return 

    m = ['3月', '6月', '1年', '3年', '5年', \
        '7年', '10年', '20年', '30年']
    l = [name+x for x in m]
    
    d = pd.DataFrame(columns=[0,1,2,3,6,9,12,24,36])
    d.loc[today.date()] = df.loc[today,l].tolist()
    d.loc[base.date()] = df.loc[base,l].tolist()
    d.loc['25分位数'] = [np.quantile(df[x],0.25) for x in l]
    d.loc['75分位数'] = [np.quantile(df[x],0.75) for x in l]
    d.loc['中位数'] = [np.quantile(df[x],0.5) for x in l]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    d.loc[today.date()].plot(ax=ax,label='现值')
    d.loc[base.date()].plot(ax=ax,color='red',label='2020年底')
    d.loc['25分位数'].plot(ax=ax,ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=ax,ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=ax,color='orange',alpha=0.3)

    ax.set_xticks([0,3,6,9,12,24,36])
    ax.set_xticklabels(['3M','3Y','5Y','7Y','10Y','20Y','30Y'])
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(-0.02,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)

    ax.set_title(name+'到期收益率曲线')
    return fig

def gz(year=1):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2007':]

    a = df[['国债'+str(year)+'年']   ]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    a.iloc[:,0].plot(ax=ax,)
    ax.axhline(y=q25,ls='--',color='lightgrey')
    ax.axhline(y=q75,ls='--',color='lightgrey')
    ax.axhline(y=med,ls='-',color='orange')
    ax.set_xlabel('')
    ax.legend(['国债'+str(year)+'年'],ncol=1,loc=3, bbox_to_anchor=(0.3,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig 

def gk(year=1):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2007':]

    a = df[['国开'+str(year)+'年']   ]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    a.iloc[:,0].plot(ax=ax,label='')
    ax.axhline(y=q25,ls='--',color='lightgrey')
    ax.axhline(y=q75,ls='--',color='lightgrey')
    ax.axhline(y=med,ls='-',color='orange')
    ax.legend(['国开'+str(year)+'年'],ncol=1,loc=3, bbox_to_anchor=(0.3,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_xlabel('')
    return fig 

def CurveChange(bond='gz'):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2021':]
    
    base = df.index[0]
    end = df.index[-1]

    if bond=='gz':
        name = '国债'  
    elif bond=='gk':
        name = '国开'
    else:
        print('error')
        return 
    m = [ '6月', '1年', '3年', '5年','7年', '10年']
    l = [name+x for x in m]

    d = pd.DataFrame([],columns=range(6))
    d.loc[base] = df.loc[base,l].tolist()
    d.loc[end] = df.loc[end,l].tolist()
    d.loc['期间变动(BP)'] =( d.loc[end]-d.loc[base] )*100

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    d.loc['期间变动(BP)'].plot(ax=ax,kind='bar',color='lightgrey')
    ax_=ax.twinx()
    d.loc[end].plot(ax=ax_)
    d.loc[base].plot(ax=ax_)
    ax.set_xticklabels(['6M','1Y','3Y','5Y','7Y','10Y'],rotation=0)
    ax.set_title(name+'收益率变动')
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.05,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend([base.date(),end.date()],ncol=1,loc=3, bbox_to_anchor=(0.6,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def local_gz():
    df = do.get_data('rates')
    df.index = df.date
    df = df['2013':]
    df['地方债-国债'] = (df['地方5年']-df['国债5年'])*100

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date,0,df['地方债-国债'],\
        label='地方债-国债',color='lightgrey',alpha=1)
    ax_=ax.twinx()
    df[['地方5年','国债5年']].plot(ax=ax_)
    ax_.set_yticks(np.arange(1,6))
    ax.set_yticks(range(0,100,20))
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.05,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(['地方债:5年:AAA','国债:5年'],\
        ncol=1,loc=3, bbox_to_anchor=(0.45,-0.7),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig

def gk_gz():
    df = do.get_data('rates')
    df.index = df.date
    df = df['2009':]
    df['国开债-国债'] = (df['国开10年']-df['国债10年'])*100
        
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date,0,df['国开债-国债'],\
        label='国开债-国债',color='lightgrey',alpha=1)
    ax_= ax.twinx()
    df[['国开10年','国债10年']].plot(ax=ax_)

    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.05,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(['国开债:10年','国债:10年'],\
        ncol=1,loc=3, bbox_to_anchor=(0.45,-0.7),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig 

def cd_r007():
    cash = do.get_data('cash_cost');cash.index = cash.date
    df = do.get_data('rates')
    df.index = df.date
    df = df['2015':]
    df['存单-DR007'] = (df['cd_3m_aaa+']-cash['DR007'])*100
    df['DR007'] = cash['DR007']

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    ax.fill_between(df.date,0,df['存单-DR007'],\
        label='存单-DR007',color='lightgrey',alpha=1)
    ax_= ax.twinx()
    df[['cd_3m_aaa+','DR007']].plot(ax=ax_)

    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.05,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    ax_.legend(['存单:3个月:AAA+','DR007'],\
        ncol=1,loc=3, bbox_to_anchor=(0.45,-0.7),borderaxespad = 0.,fontsize=10,frameon=False)
    return fig 

def msP():
    df = do.get_data('rates')
    df.index = df.date
    df = df['2010':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['中票_AAA_1y','中票_AAA_5y','中票_AA+_1y','中票_AA+_5y']].plot(ax=ax)
    ax.axhline(y=np.median(df['中票_AAA_5y']),ls='--',color='grey',label='5Y:AAA:中位数')
    ax.axhline(y=np.median(df['中票_AA+_5y']),ls='--',color='black',label='5Y:AA+:中位数')
    ax.set_xlabel('')
    ax.set_title('中票收益率')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.05,-1),borderaxespad = 0.,fontsize=10,frameon=False)
    
    return fig 

    