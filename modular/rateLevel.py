import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False

#### * 利率水平
def yieldCurve(bond='gz'):
    '''
    各期限(3M-30Y)到期收益率曲线 & 2007年来历史中位数
    现值:2020年底
    国开/国债
    '''

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
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    d.loc[today.date()].plot(ax=ax,label='现值('+today.date().strftime('%Y%m%d')+')',\
        marker='o',color='#3778bf')
    d.loc[base.date()].plot(ax=ax,color='#f0833a',label='2020年底',marker='s')
    d.loc['25分位数'].plot(ax=ax,ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=ax,ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=ax,color='orange',alpha=0.3)

    ax.set_ylim([1.5,4.5])
    ax.set_xticks([0,3,6,9,12,24,36])
    ax.set_xticklabels(['3M','3Y','5Y','7Y','10Y','20Y','30Y'])
    ax.legend(ncol=3,loc='best',frameon=False)
    # ax.legend(ncol=3,loc=3, bbox_to_anchor=(0.1,-0.25),borderaxespad = 0.,fontsize=10,frameon=False)
    ax.set_title(name+'到期收益率曲线')
    plt.show()

    d.columns = ['3M','6M','1Y','3Y','5Y','7Y','10Y','20Y','30Y']
    return d

def gz(year=1):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2007':]

    a = df[['国债'+str(year)+'年']   ]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    a.iloc[:,0].plot(ax=ax,label='国债'+str(year)+'年')
    ax.axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    ax.axhline(y=med,ls='-',color='orange',label='中位数')
    ax.set_xlabel('')
    ax.legend(ncol=3,frameon=False,loc=9)
    ax.axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    # ax.set_ylim([2,5])
    ax.set_title('国债'+str(year)+'年')
    plt.show()
    return fig 

def gk(year=1):
    df = do.get_data('rates')
    df.index = df.date
    df = df['2007':]

    a = df[['国开'+str(year)+'年']]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    a.iloc[:,0].plot(ax=ax,label='国开'+str(year)+'年')
    ax.axhline(y=q25,ls='--',color='lightgrey',label='25分位数')
    ax.axhline(y=q75,ls='--',color='lightgrey',label='75分位数')
    ax.axhline(y=med,ls='-',color='orange',label='中位数')
    ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.2,-0.35),borderaxespad = 0.,fontsize=12,frameon=False)
    ax.set_title('国开'+str(year)+'年')
    ax.set_xlabel('')
    plt.show()
    return a

def CurveChange(base,end,bond='gz',):
    '''
    各期限到期收益率变动
    现值：年初
    '''
    df = do.get_data('rates')
    df.index = df.date
    df = df['2021':]
    
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
    ## plott
    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    d.loc['期间变动(BP)'].plot(ax=ax,kind='bar',color='lightgrey')
    ax_=ax.twinx()
    d.loc[end].plot(ax=ax_,marker='o',color='#3778bf')
    d.loc[base].plot(ax=ax_,marker='o',color='#f0833a')
    ax.set_xticklabels(['6M','1Y','3Y','5Y','7Y','10Y'],rotation=0)
    ax.set_title(name+'收益率变动')
    ax_.legend([base, end],loc='lower right',\
        ncol=1,fontsize=10,frameon=False,)
    ax_.set_ylabel('(%)',fontsize=10)
    ax.set_ylabel('期间变动(BP)',fontsize=10)
    return d

def local_gz_5y():
    df = do.get_data('rates')
    df.index = df.date
    df = df['2013':]
    df['地方债-国债'] = (df['地方5年']-df['国债5年'])*100
    df = df[['地方5年','国债5年','地方债-国债','date']]

    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date,0,df['地方债-国债'],\
        label='地方债-国债(左:BP)',color='lightgrey',alpha=1)
    ax_=ax.twinx()
    df[['地方5年','国债5年']].plot(ax=ax_)
    ax_.set_yticks(np.arange(1,6))
    ax.set_yticks(range(0,100,20))
    ax.legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['地方债:5年:AAA','国债:5年'],\
        loc=1,frameon=False,fontsize=10)
    # ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.1,-0.25),borderaxespad = 0.,fontsize=12,frameon=False)
    # ax_.legend(['地方债:5年:AAA','国债:5年'],\
    #     ncol=1,loc=3, bbox_to_anchor=(0.55,-0.3),borderaxespad = 0.,fontsize=12,frameon=False)
    ax.set_title('地方债-国债(5Y)')
    plt.show()
    return df

def gk_gz_10y():
    df = do.get_data('rates')
    df.index = df.date
    df = df['2009':]
    df['国开债-国债'] = (df['国开10年']-df['国债10年'])*100
    df = df[['国开10年','国债10年','国开债-国债','date']]
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date,0,df['国开债-国债'],\
        label='国开债-国债(左:BP)',color='lightgrey',alpha=1)
    ax_= ax.twinx()
    df[['国开10年','国债10年']].plot(ax=ax_)
    ax.set_title('国开债-国债(10Y)')
    ax.legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['国开债:10年','国债:10年'],\
        loc=1,frameon=False,fontsize=10)
    ax.set_ylim([0,160])
    ax_.set_ylim([2,6.5])
    # ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.10,-0.25),borderaxespad = 0.,fontsize=12,frameon=False)
    # ax_.legend(['国开债:10年','国债:10年'],\
    #     ncol=1,loc=3, bbox_to_anchor=(0.55,-0.3),borderaxespad = 0.,fontsize=12,frameon=False)
    plt.show()
    return df

def cd3m_r007():
    cash = do.get_data('cash_cost');cash.index = cash.date
    df = do.get_data('rates')
    df.index = df.date
    df = df['2015':]
    df['存单-DR007'] = (df['cd_3m_aaa+']-cash['DR007'])*100
    df['DR007'] = cash['DR007']
    df = df[['cd_3m_aaa+','DR007','存单-DR007','date']]
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    ax.fill_between(df.date,0,df['存单-DR007'],\
        label='存单-DR007(左:BP)',color='lightgrey',alpha=1)
    ax_= ax.twinx()
    df[['cd_3m_aaa+','DR007']].plot(ax=ax_,color=['#f0833a','#3778bf'])
    ax.set_title('存单与DR007')
    ax.legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['同业存单:3个月:AAA+','DR007'],\
        loc=1,ncol=2,frameon=False,fontsize=10)
    ax.set_ylim([-100,250])
    ax_.set_ylim([1.0,5.5])
    # ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.05,-0.25),borderaxespad = 0.,fontsize=12,frameon=False)
    # ax_.legend(['存单:3个月:AAA+','DR007'],\
    #     ncol=1,loc=3, bbox_to_anchor=(0.45,-0.3),borderaxespad = 0.,fontsize=12,frameon=False)
    plt.show()
    return df 

def msP():
    df = do.get_data('rates')
    df.index = df.date
    df = df['2010':]
    df = df[['中票_AAA_1y','中票_AAA_5y','中票_AA+_1y','中票_AA+_5y','date']]
    plt.style.use({'font.size' : 10}) 
    fig,ax = plt.subplots(figsize=(6,4), dpi=300)
    df[['中票_AAA_1y','中票_AAA_5y','中票_AA+_1y','中票_AA+_5y']].plot(ax=ax,\
        color = ["#3778bf","brown","lightgrey","#f0833a"])
    ax.axhline(y=np.median(df['中票_AAA_5y']),ls='--',color='grey',label='5Y:AAA:中位数')
    ax.axhline(y=np.median(df['中票_AA+_5y']),ls='--',color='black',label='5Y:AA+:中位数')
    ax.set_xlabel('')
    ax.set_title('中票收益率')
    ax.legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax.set_ylim([1,8])
    # ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.1,-0.42),borderaxespad = 0.,fontsize=12,frameon=False)
    plt.show()

    return df 


# figs = [yieldCurve('gz'),yieldCurve('gk'),gz(1),gz(10),gk(1),gk(10),\
#     CurveChange('gz'),CurveChange('gk'),local_gz(),gk_gz(),cd_r007(),msP()]

# for i in range(len(figs)):
#     f = figs[i]
#     f.savefig('./tmp/收益率水平/{}.jpg'.format(i),dpi=300,bbox_inches='tight')
