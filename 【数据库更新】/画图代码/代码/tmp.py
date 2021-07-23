import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False

### * 资金数据与息差情况
def RepoRate():
    df = do.get_data('cash_amt_prc')
    df.index = df.date

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['R001','R007','R021']].dropna()['2019':].plot(ax=ax)
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
    df[['DR001']].plot(ax=ax_)
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
    df[['DR007']].plot(ax=ax_)
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
    
def R_GC_7D():
    df = do.get_data('cash_cost')
    df.index = df.date
    df = df['2016-01':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['R007','GC007']].plot(ax=ax)
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.15,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
    
    return

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
        label = 'R007-DR007',color='lightgrey',alpha=1)
    ax.fill_between(df.date, 0, df['七天回购占比'], \
        label = 'R007-DR007',color='orange',alpha=1)

def irs():
    df = do.get_data('spreads')
    df.index = df.date
    df = df['2009':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
    df[['IRS_1y_FR007', 'IRS_5y_FR007','IRS_5y_shibor3m']].plot(ax=ax)
    ax.set_xlabel('')
    ax.legend(ncol=3,loc=3, bbox_to_anchor=(-0.15,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)

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
    a.iloc[:,0].plot(ax=ax,label='')
    ax.axhline(y=q25,ls='--',color='lightgrey')
    ax.axhline(y=q75,ls='--',color='lightgrey')
    ax.axhline(y=med,ls='-',color='orange')
    ax.set_xlabel('')

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
    ax.set_xlabel('')

def CurveChange(base,bond='gz'):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2021':]
    
    base = df.index[0].date()
    end = df.index[-1].date()

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
    ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.6,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
    
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

def cd_r007():
    cash = do.get_data('cash_cost');cash.index = cash.date
    df = do.get_data('rates1')
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


def msP():
    df = do.get_data('rates1')
    df.index = df.date
    df = df['2010':]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['中票_AAA_1y','中票_AAA_5y','中票_AA+_1y','中票_AA+_5y']].plot(ax=ax)
    ax.axhline(y=np.median(df['中票_AAA_5y']),ls='--',color='grey',label='5Y:AAA:中位数')
    ax.axhline(y=np.median(df['中票_AA+_5y']),ls='--',color='black',label='5Y:AA+:中位数')
    ax.set_xlabel('')
    ax.set_title('中短票收益率')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.05,-1),borderaxespad = 0.,fontsize=10,frameon=False)
    



#### * tmp（投决会
def bpChange():
    rates = do.get_data('rates1')
    rates.index = rates.date

    name = '国债'
    m = [ '1年', '3年', '5年','7年', '10年']
    l = [name+x for x in m]

    df = rates[l]

    dateRange = ['11.19-1.14','1.14-2.18','2.18-6.1','6.1-6.18']
    
    stat = pd.DataFrame([], columns = l, index = dateRange)

    stat.loc[dateRange[0]]=(df.loc['2021-01-14']-df.loc['2020-11-19'])*100
    stat.loc[dateRange[1]]=(df.loc['2021-02-18']-df.loc['2021-01-14'])*100
    stat.loc[dateRange[2]]=(df.loc['2021-06-01']-df.loc['2021-02-18'])*100
    stat.loc[dateRange[3]]=(df.loc['2021-06-18']-df.loc['2021-06-01'])*100

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    stat.plot(kind='bar',ylim=(-80,40),ax=ax,color = ["#3778bf","lightsteelblue","lightgray","peachpuff","#f0833a"],\
        edgecolor='black')
    ax.grid(ls='--', axis='y')
    ax.set_axisbelow(True)
    ax.legend(['1Y','3Y','5Y','7Y','10Y'],\
        ncol=5,loc=3, bbox_to_anchor=(-0.02,-0.2),borderaxespad = 0.,frameon=False)
    plt.xticks(rotation = 0)

    return fig

def rateVolatility():
    rates = do.get_data('rates1')
    rates.index = rates.date

    df = rates[['国债10年','国开10年']]['2003':]

    stat = pd.DataFrame([], columns=['国债10年','国开10年'],index=range(2003,2022))
    for year in range(2003,2021+1):
        d1 = str(year)+'-'+'01'
        d2 = str(year)+'-'+'06'
        df_year = df[d1:d2]
        stat.loc[year,'国债10年'] = (df_year['国债10年'].max()-df_year['国债10年'].min())*100
        stat.loc[year,'国开10年'] = (df_year['国开10年'].max()-df_year['国开10年'].min())*100

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    stat.plot(kind='bar',ax=ax,color=["#3778bf","lightsteelblue"],edgecolor='black')
    ax.legend(
        ncol=5,loc=3, bbox_to_anchor=(0.2,-0.25),borderaxespad = 0.,frameon=False)
    plt.xticks(rotation = 45)

    return fig

def rollingStd():
    rates = do.get_data('rates1')
    rates.index = rates.date

    df = rates[['国债10年','国开10年']]['2005':]

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    df['国债10年'].rolling(20).std().plot(ax=ax,label='10Y国债收益率:滚动标准差(20天)')
    df['国开10年'].rolling(20).std().plot(ax=ax,label='10Y国开收益率:滚动标准差(20天)')
    ax.set_xlabel('')
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.15,-0.35),borderaxespad = 0.,frameon=False)

    return fig

def local():
    df = do.get_data('localbond_issue')
    df.index=df.date

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    # 2019
    df_2019 = df['2019':'2019']
    amt=(107685 - 86185)
    ax.plot(range(12),df_2019.iloc[:,1] / amt,ls='--',color='#3778bf')
    # 2020
    df_2020 = df['2020':'2020']
    amt=145185 - 107685
    ax.plot(range(12),df_2020.iloc[:,1] / amt,color="lightsteelblue")
    # 2021
    df_2021 = df['2021':'2021']
    amt=34676
    ax.plot(range(5),np.append([0,0],df_2021.iloc[:,1].tolist())/ amt,\
        color = '#f0833a')

    ax.legend([2019,2020,2021],\
        ncol=3,loc=3, bbox_to_anchor=(0.15,-0.2),borderaxespad = 0.,frameon=False)
    ax.set_xticks(range(12))
    ax.set_xticklabels(['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月',\
        '11月','12月'])

    return fig

def financeDraw():
    df = do.get_data('fundAmt')
    df.index = df.date
    df = df[['货币当局:政府存款']].diff(1)

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)

    colors = ['#3778bf',"lightsteelblue","lightgray","#f0833a"]
    ax.axhline(y=0,ls='--',color = 'black',alpha=0.5)
    for year in range(2018,2021):
        # year=2017
        df_year = df[str(year):str(year)]

        ax.plot(range(12),df_year.iloc[:,0].tolist(),color=colors[year-2018])

    year = 2021
    df_year = df[str(year):str(year)]
    ax.plot(range(5),df_year.iloc[:,0].tolist(),color=colors[-1])
    ax.scatter(1, df_year.iloc[:,0].tolist()[1],c=sns.xkcd_rgb['dull red'])
    
    ax.set_xticks(range(12))
    ax.set_xticklabels(['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月',\
        '11月','12月'])
    ax.legend([2018,2019,2020,2021],\
        ncol=4,loc=3, bbox_to_anchor=(0.05,-0.2),borderaxespad = 0.0,frameon=False)
    return fig

def fyck():
    df = do.get_data('fundAmt')
    df.index = df.date

    stat = pd.DataFrame([],columns=['fyck'],index = range(2018,2022))
    for year in range(2018,2022):
        d1 = str(year)+'-01'
        d2 = str(year)+'-04'

        df_year = df[d1:d2]
        stat.loc[year,'fyck'] = df_year.iloc[:,1].sum()
    

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    stat.plot(kind='bar',color = '#3778bf',ax=ax,edgecolor='black')
    ax.grid(ls='--', axis='y')
    ax.set_axisbelow(True)
    ax.legend(['非银存款增加值'],\
        ncol=1,loc=3, bbox_to_anchor=(0.3,-0.2),borderaxespad = 0.0,frameon=False)
    ax.set_xticklabels(['2018年1-4月','2019年1-4月','2020年1-4月','2021年1-4月'])
    plt.xticks(rotation=0)

    return fig

def fundamt():
    df = do.get_data('fundAmt')
    df.index = df.date
    df = df[['货币基金份额', '股票基金份额', '混合型基金份额']]['2020':]

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    ax.plot(df)
    plt.xticks(rotation=45)
    ax.legend(['货币基金份额', '股票基金份额', '混合型基金份额'],\
        ncol=3,loc=3, bbox_to_anchor=(-0.07,-0.3),borderaxespad = 0.0,frameon=False)
    
    return fig


def savePics():
    # 保存图片
    pic_list = [bpChange(),rateVolatility(),rollingStd(),\
        local(),financeDraw(),fyck(),fundamt()]
    name = ['利率变动','上半年利率波动大小','20日滚动波动率','地方专项债发行','财政存款',\
        '非银存款','基金份额']
    for i in range(len(pic_list)):
        p = pic_list[i]
        p.savefig('./tmp/'+'{}.jpg'.format(name[i]),bbox_inches='tight',dpi=300)

 

def indices():
    # 指数涨跌幅热力图

    df = do.get_data('bond_indices')
    df.index = df.date

    months=['2020-10','2020-11','2020-12','2021-01','2021-02',\
        '2021-03','2021-04','2021-05','2021-06'] 
    years = range(2017,2022)

    stat = pd.DataFrame([],index = months,columns = df.columns[:-1])
    for m in months:
        df_tmp = df[m:m]
        stat.loc[m] = (df_tmp.iloc[-1,:-1]-df_tmp.iloc[0,:-1]) / df_tmp.iloc[0,:-1]
    for y in years:
        df_tmp = df[str(y):str(y)].fillna(method='ffill')
        stat.loc[y] = (df_tmp.iloc[-1,:-1]-df_tmp.iloc[0,:-1]) / df_tmp.iloc[0,:-1]

    stat = stat.astype(float)*100
    plt.style.use({'font.size' : 12})     
    fig, ax = plt.subplots(nrows=1,ncols=1,\
        figsize=(10,6), dpi=300)
    sns.heatmap(stat,cmap="bwr",linewidths=1,ax=ax,\
                cbar=True, annot=True)
    plt.xticks(rotation=30)
    plt.yticks(rotation=0)
    

def p1():
    df = do.get_data('rates1')
    df.index = df.date
    
    ### 1
    plt.style.use({'font.size' : 12})     
    fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(6,4), dpi=300)
    df['国债利差：30Y-10Y'] = (df['国债30年']-df['国债10年'])*100
    df[['国债利差：30Y-10Y']]['2020':].plot(ax=ax,color='#3778bf')
    ax.set_xlabel('')
    ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.25,-0.3),borderaxespad = 0.,fontsize=12,frameon=False)
    return fig
def p2():  
    ### 2
    df['口行-国开：10Y'] = (df['口行10年'] - df['国开10年'])*100
    df['农发-国开：10Y'] = (df['农发10年'] - df['国开10年'])*100
    plt.style.use({'font.size' : 12})     
    fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(6,4), dpi=300)
    df[['口行-国开：10Y','农发-国开：10Y']]['2019':].plot(ax=ax,color=['#3778bf','#f0833a'])
    ax.set_xlabel('')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.1,-0.3),borderaxespad = 0.,fontsize=12,frameon=False)
    return fig
def p3():
    ### 3
    dff = pd.DataFrame([])
    dff['中票信用利差(AAA):3年'] = (df['中票_AAA_3y'] - df['国开3年'])*100
    dff['q25_aaa']= dff['中票信用利差(AAA):3年'].rolling(250*3).quantile(0.25)
    dff['q50_aaa']= dff['中票信用利差(AAA):3年'].rolling(250*3).quantile(0.5)
    dff['q75_aaa']= dff['中票信用利差(AAA):3年'].rolling(250*3).quantile(0.75)
    
    fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(6,4), dpi=300)
    dff[['中票信用利差(AAA):3年']]['2018':].plot(ax=ax)
    dff.iloc[:,-3:]['2018':].plot(ls='--',ax=ax,label=[1,2,3])
    ax.set_xlabel('')
    ax.legend(['中票信用利差(AAA):3年','3年滚动25分位数','3年滚动中位数','3年滚动75分位数'],\
        ncol=2,loc=3, bbox_to_anchor=(0.02,-0.4),borderaxespad = 0.,fontsize=12,frameon=False)
    return fig
def p4():
    dff = pd.DataFrame([])
    dff['中票信用利差(AA-):3年'] = (df['中票_AA-_3y'] - df['国开3年'])*100
    dff['q25_aa-']= dff['中票信用利差(AA-):3年'].rolling(250*3).quantile(0.25)
    dff['q50_aa-']= dff['中票信用利差(AA-):3年'].rolling(250*3).quantile(0.5)
    dff['q75_aa-']= dff['中票信用利差(AA-):3年'].rolling(250*3).quantile(0.75)
    fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(6,4), dpi=300)
    dff[['中票信用利差(AA-):3年']]['2018':].plot(ax=ax)
    dff.iloc[:,-3:]['2018':].plot(ls='--',ax=ax,label=[1,2,3])
    ax.set_xlabel('')
    ax.legend(['中票信用利差(AA-):3年','3年滚动25分位数','3年滚动中位数','3年滚动75分位数'],\
        ncol=2,loc=3, bbox_to_anchor=(0.02,-0.4),borderaxespad = 0.,fontsize=12,frameon=False)
    return fig 

def savepics():
    pic_list = [p1(),p2(),p3(),p4()]
    name = ['1','2','3','4']
    for i in range(len(pic_list)):
        p = pic_list[i]
        p.savefig('./tmp/'+'{}.jpg'.format(name[i]),bbox_inches='tight',dpi=300)

def rate_syn():
    df = do.get_data('rate_syn')
    rates = do.get_data('rates')

    df.index=df.date; rates.index=rates.date
    rates = rates[['国债10年']]

    # p1 挖机销量
    fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['挖掘机销量同比']].dropna().rolling(6).mean().dropna()
    # dff['国债10年'] = rates['国债10年'][dff.index[0]:]
    rates['国债10年'][dff.index[0]:].plot(ax=ax[0,0])
    ax00_ = ax[0,0].twinx()
    ax00_.plot(dff.index,dff['挖掘机销量同比'],color='#f0833a',label='挖掘机销量同比(6MMA)')
    ax[0,0].set_xlabel('')
    ax00_.legend()


    # p2 水泥价格同比
    dff = df[['水泥价格指数']].dropna().pct_change(periods=230).dropna()
    rates[dff.index[0]:].plot(ax=ax[0,1])
    ax_ = ax[0,1].twinx()
    dff['水泥价格指数'].plot(ax=ax_,color='#f0833a')
    ax[0,1].set_xlabel('')
    ax_.legend(['水泥价格指数同比(6MMA)'])
    
    # p3 
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['重点企业粗钢产量']].dropna().pct_change(periods=12).\
        rolling(6).mean().dropna()
    # dff['国债10年'] = rates['国债10年']
    rates[dff.index[0]:].plot(ax=ax[1,0])
    ax_ = ax[1,0].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[1,0].set_xlabel('')
    ax_.legend(['重点企业粗钢产量同比(6MMA)'])

    # P4
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['重点电厂煤耗总量']].dropna().pct_change(periods=12).\
        rolling(6).mean().dropna()
    # dff['国债10年'] = rates['国债10年']
    rates[dff.index[0]:].plot(ax=ax[1,1])
    ax_ = ax[1,1].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[1,1].set_xlabel('')
    ax_.legend(['重点电厂煤耗总量同比(6MMA)'])

    # P5
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['国内铁矿石港口库存量']].dropna()
    # dff['国债10年'] = rates['国债10年']
    rates[dff.index[0]:].plot(ax=ax[2,0])
    ax_ = ax[2,0].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[2,0].set_xlabel('')
    ax_.legend(['国内铁矿石港口库存量'])

    # todo P6
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['电影票房收入']][:'2020'].dropna().pct_change(periods=52).\
        rolling(6*4).mean().dropna()
    # dff['国债10年'] = rates['国债10年']
    rates[dff.index[0]:].plot(ax=ax[2,1])
    ax_ = ax[2,1].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[2,1].set_xlabel('')
    ax_.legend(['电影票房收入同比(6MMA)'])

    # P7
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['PMI']].dropna().pct_change(periods=12).rolling(6).mean().dropna()
    rates[dff.index[0]:].plot(ax=ax[3,0])
    ax_ = ax[3,0].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[3,0].set_xlabel('')
    ax_.legend(['PMI同比(6MMA)'])


    # todo P8 画逆序
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = pd.DataFrame([])
    dff['银行总资产/央行总资产'] = df['其他存款性公司:总资产'].div(df['货币当局:总资产'],axis=0).\
        dropna().pct_change(periods=12).rolling(1).mean().dropna()

    rates[dff.index[0]:].plot(ax=ax[3,1])
    ax_ = ax[3,1].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[3,1].set_xlabel('')
    ax_.legend(['银行总资产/央行总资产'])

    # P9
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = df[['美元指数']].dropna()
    rates[dff.index[0]:].plot(ax=ax[4,0])
    ax_ = ax[4,0].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[4,0].set_xlabel('')
    ax_.legend(['美元指数'])

    # P10
    # fig,ax = plt.subplots(nrows=5,ncols=2,figsize=(12,20),dpi=300)
    dff = pd.DataFrame([])
    dff['铜金比'] = df['铜价'].div(df['金价'],axis=0).\
        dropna()
    rates[dff.index[0]:].plot(ax=ax[4,1])
    ax_ = ax[4,1].twinx()
    ax_.plot(dff,color='#f0833a')
    ax[4,1].set_xlabel('')
    ax_.legend(['铜金比'])
