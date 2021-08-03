import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
import matplotlib.ticker as ticker
plt.rcParams['axes.unicode_minus'] = False

    
def cash_fig():
    cash_amt_prc = do.get_data('cash_amt_prc'); cash_amt_prc.index=cash_amt_prc.date
    
    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=6,figsize=(6*2,4*6), dpi=300)
    # * P0.0
    cash_amt_prc[['R001','R007']].dropna()['2019':].plot(ax=ax[0,0],\
        color=['#3778bf','#f0833a'])
    cash_amt_prc[['R021']].dropna()['2019':].plot(ax=ax[0,0],\
        color=['grey'],lw=1) 
    ax[0,0].set_xlabel('')
    ax[0,0].set_title('质押式回购资金利率')
    ax[0,0].legend(loc=9,ncol=3,frameon=False)
    l = do.set_axes_rotation(ax[0,0])
    ax[0,0].set_ylabel('(%)',fontsize=10)

    # * P0.1
    cash_amt_prc[['DR001','GC001']]['2019':].dropna().\
        plot(ax=ax[0,1],ylim=(0,7),color=['#3778bf','#f0833a','grey'])
    # ax_ = ax[0,1].twinx()
    # cash_amt_prc[['DR001']]['2019':].plot(ax=ax_,color='grey',lw=1,ylim=(0,4))
    # ax_.legend(loc=1,ncol=1,frameon=False)
    ax[0,1].set_xlabel('')
    ax[0,1].set_title('隔夜资金利率')
    ax[0,1].legend(loc=9,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[0,1])
    ax[0,1].set_ylabel('(%)',fontsize=10)
    # ax_.set_ylabel('(%)',fontsize=10)

    # * P1.0
    cash_amt_prc[['DR007','GC007']]['2019':].dropna().plot(ax=ax[1,0])
    # ax_ = ax[1,0].twinx()
    # cash_amt_prc[['DR007']]['2019':].plot(ax=ax_,color='grey',lw=1,ylim=(0,4))
    # ax_.legend(loc=1,ncol=1,frameon=False)
    ax[1,0].set_title('7天资金利率')
    ax[1,0].set_xlabel('')
    ax[1,0].legend(loc=9,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[1,0])
    ax[1,0].set_ylabel('(%)',fontsize=10)
    # ax_.set_ylabel('(%)',fontsize=10)

    # * P1.1
    ax[1,1].fill_between(cash_amt_prc.date['2019':], 0, cash_amt_prc['成交量:银行间质押式回购']['2019':]/10000, \
        label = '成交量(左:万亿)',color='lightgrey',alpha=1)
    ax[1,1].set_ylim([0,6])
    ax_=ax[1,1].twinx()
    (cash_amt_prc[['R001']]['2019':]).plot(ax=ax_,ylim=(0.6,8))
    ax[1,1].set_title('隔夜回购利率与成交量')
    ax[1,1].legend(loc=2, frameon=False)
    ax_.legend(loc=1, frameon=False)
    l = do.set_axes_rotation(ax[1,1])
    ax[1,1].set_ylabel('万亿',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P2.0
    cash_amt_prc['R007-DR007'] = (cash_amt_prc['R007']-cash_amt_prc['DR007'])*100
    ax[2,0].fill_between(cash_amt_prc.date['2016':], 0, cash_amt_prc['R007-DR007']['2016':], \
        label = 'R007-DR007(左,BP)',color='lightgrey',alpha=1)
    ax[2,0].set_ylim([-50,200])
    ax_=ax[2,0].twinx()
    cash_amt_prc[['R007','DR007']]['2016':].plot(ax=ax_,ylim=(1,8))
    ax[2,0].set_title('R007-DR007')
    ax[2,0].legend(loc=2,frameon=False)
    ax_.legend(loc=1,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[2,0],rotation=0)
    ax[2,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P2.1
    ax[2,1].plot(cash_amt_prc['date']['2016':],cash_amt_prc[['R007','GC007']]['2016':],alpha=0.8)
    ax[2,1].set_xlabel('')
    ax[2,1].set_title('银行间与交易所资金利率')
    ax[2,1].legend(['R007','GC007'],loc=9,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[2,1],rotation=0)
    ax[2,1].set_ylabel('(%)',fontsize=10)

    # * P3.0
    repo_vol = do.get_data('repo_volume'); repo_vol.index=repo_vol.date
    repo_vol[['隔夜回购占比','七天回购占比']]=\
        repo_vol[['成交量:R001','成交量:R007']].div(\
            repo_vol[['成交量:银行间质押式回购']].sum(axis=1),axis=0)
    ax[3,0].fill_between(repo_vol.date['2015':], 0, repo_vol['隔夜回购占比']['2015':], \
        label = '隔夜回购占比(R001)',color='lightgrey',alpha=1)
    ax[3,0].fill_between(repo_vol.date['2015':], 0, repo_vol['七天回购占比']['2015':], \
        label = '七天回购占比(R007)',color='orange',alpha=1)
    ax[3,0].legend(ncol=2,loc=0,frameon=False)
    ax[3,0].set_title('隔夜与七天')
    # ax[2,1].set_ylabel('(占比)',fontsize=10)

    # * P3.1
    irs = do.get_data('spreads');irs.index=irs.date
    irs[['IRS_1y_FR007', 'IRS_5y_FR007','IRS_5y_shibor3m']].dropna().plot(ax=ax[3,1],\
        ylim=(0,7),color=['#3778bf','#f0833a','grey'])
    ax[3,1].set_xlabel('')
    ax[3,1].set_title('IRS')
    ax[3,1].legend(['IRS:1年(FR007)','IRS:5年(FR007)','IRS:5年(3M SHIBOR)'],\
        ncol=2,loc=9,frameon=False)
    l = do.set_axes_rotation(ax[3,1],rotation=0)
    ax[3,1].set_ylabel('(%)',fontsize=10)

    # * P4.0
    irs['cd:6M-R007'] = (irs['cd_AAA_6m']-cash_amt_prc['R007'])*100
    irs['R007'] = cash_amt_prc['R007']
    ax[4,0].fill_between(irs.date['2015':],0,irs['cd:6M-R007']['2015':],\
        label='同业存单:6个月:AAA-R007',color='lightgrey',alpha=1)
    ax_=ax[4,0].twinx()
    irs[['R007','cd_AAA_6m']]['2015':].plot(ax=ax_)
    ax[4,0].set_title('6M存单-R007')
    # ax[4,0].set_xticklabels(ax[4,0].get_xticklabels(), rotation=30)
    ax[4,0].legend(loc=2,frameon=False)
    ax_.legend(['R007','同业存单:6个月:AAA'],loc=1,ncol=1,frameon=False)
    ax[4,0].set_ylim([-300,300])
    ax_.set_ylim([0,8])
    ax[4,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P4.1
    irs['1年'] = irs['中短票_AA+_1y']-cash_amt_prc['R007']
    irs['3年'] = irs['中短票_AA+_3y']-cash_amt_prc['R007']
    irs['5年'] = irs['中短票_AA+_5y']-cash_amt_prc['R007']
    irs[['1年', '3年','5年']]['2016':].plot(ax=ax[4,1],\
        color=['#3778bf','#f0833a','grey'],ylim=(-3,4))
    ax[4,1].set_xlabel('')
    ax[4,1].set_title('中短票:AA+-R007')
    ax[4,1].legend(ncol=3,loc=9,frameon=False)
    ax[4,1].axhline(y=0,lw=1,color='black',ls='--')
    l = do.set_axes_rotation(ax[4,1],rotation=0)
    ax[4,1].set_ylabel('(%)',fontsize=10)

    # * P5.0
    irs['国开债:10年-R007'] = (irs['国开10年']-cash_amt_prc['R007'])
    irs['地方债:3年:AAA-R007'] = (irs['地方债_AAA_3y']-cash_amt_prc['R007'])
    irs = irs[['国开债:10年-R007','地方债:3年:AAA-R007']]
    irs[['国开债:10年-R007','地方债:3年:AAA-R007']]['2016':].plot(ax=ax[5,0],\
        ylim=(-3,3),color=['#3778bf','#f0833a'])
    ax[5,0].set_xlabel('')
    ax[5,0].set_title('国开10年与地方债3年-R007')
    ax[5,0].legend(ncol=2,loc=9 ,frameon=False)
    ax[5,0].axhline(y=0,lw=1,color='black',ls='--')
    l = do.set_axes_rotation(ax[5,0],rotation=0)
    ax[5,0].set_ylabel('(%)',fontsize=10)

    # * P5.1
    interbank_deposit = do.get_data('interbank_deposit','2020-01-01')
    interbank_deposit.index = interbank_deposit.date
    ax[5,1].plot(interbank_deposit[['存单_股份行_1y']],'#3778bf',label="1年股份行存单利率")
    # ax[5,1].scatter(interbank_deposit.index,interbank_deposit['MLF：1y'],\
    #     label='MLF利率：1年', marker='o',color = '#f0833a',s=10)
    interbank_deposit['MLF：1y'].fillna(method='ffill').\
        plot(ax = ax[5,1],ls='--',color = '#f0833a', lw=1.5)
    ax[5,1].set_ylim([1.5,3.75])
    ax[5,1].legend(ncol=2,loc=9,frameon=False,)
    ax[5,1].set_title('MLF与同业存单')
    ax[5,1].set_ylabel('(%)',fontsize=10)
    ax[5,1].set_xlabel('')

    plt.suptitle('流动性指标',fontsize=24,y=1.01)
    plt.tight_layout()

    return fig

def rate_level_fig():
    df = do.get_data('rates');df.index = df.date

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=6,figsize=(6*2,4*6), dpi=300)
    
    # * P0.0 & P0.1
    ## 选取对比日期
    today = df.index[-1];base = df['2020':'2020'].index[-1]
    # 国债
    name = '国债'
    m = ['3月', '6月', '1年', '3年', '5年', \
        '7年', '10年', '20年', '30年']
    l = [name+x for x in m]
    d = pd.DataFrame(columns=[0,1,2,3,6,9,12,24,36])
    d.loc[today.date()] = df.loc[today,l].tolist()
    d.loc[base.date()] = df.loc[base,l].tolist()
    d.loc['25分位数'] = [np.quantile(df[x]['2007':],0.25) for x in l]
    d.loc['75分位数'] = [np.quantile(df[x]['2007':],0.75) for x in l]
    d.loc['中位数'] = [np.quantile(df[x]['2007':],0.5) for x in l]
    #plot 
    d.loc[today.date()].plot(ax=ax[0,0],label='现值('+today.date().strftime('%Y%m%d')+')',\
        marker='o',color='#3778bf')
    d.loc[base.date()].plot(ax=ax[0,0],color='#f0833a',label='2020年底',marker='s')
    d.loc['25分位数'].plot(ax=ax[0,0],ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=ax[0,0],ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=ax[0,0],color='orange',alpha=0.3)
    ax[0,0].set_ylim([1.5,4.5])
    ax[0,0].set_xticks([0,3,6,9,12,24,36])
    ax[0,0].set_xticklabels(['3M','3Y','5Y','7Y','10Y','20Y','30Y'])
    ax[0,0].legend(ncol=2,loc='best',frameon=False,fontsize=10)
    ax[0,0].set_title(name+'到期收益率曲线')
    ax[0,0].set_ylabel('(%)',fontsize=10)
    # 国开
    name = '国开'
    m = ['3月', '6月', '1年', '3年', '5年', \
        '7年', '10年', '20年', '30年']
    l = [name+x for x in m]
    d = pd.DataFrame(columns=[0,1,2,3,6,9,12,24,36])
    d.loc[today.date()] = df.loc[today,l].tolist()
    d.loc[base.date()] = df.loc[base,l].tolist()
    d.loc['25分位数'] = [np.quantile(df[x]['2007':],0.25) for x in l]
    d.loc['75分位数'] = [np.quantile(df[x]['2007':],0.75) for x in l]
    d.loc['中位数'] = [np.quantile(df[x]['2007':],0.5) for x in l]
    #plot
    d.loc[today.date()].plot(ax=ax[0,1],label='现值('+today.date().strftime('%Y%m%d')+')',\
        marker='o',color='#3778bf')
    d.loc[base.date()].plot(ax=ax[0,1],color='#f0833a',label='2020年底',marker='s')
    d.loc['25分位数'].plot(ax=ax[0,1],ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=ax[0,1],ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=ax[0,1],color='orange',alpha=0.3)
    ax[0,1].set_ylim([1.5,5.5])
    ax[0,1].set_xticks([0,3,6,9,12,24,36])
    ax[0,1].set_xticklabels(['3M','3Y','5Y','7Y','10Y','20Y','30Y'])
    ax[0,1].legend(ncol=2,loc='best',frameon=False,fontsize=10)
    ax[0,1].set_title(name+'到期收益率曲线')
    ax[0,1].set_ylabel('(%)',fontsize=10)

    # * P1.0 & P1.1 国债10&1y
    #10y
    year=10
    a = df[['国债'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[:,0].plot(ax=ax[1,0],label='国债'+str(year)+'年')
    ax[1,0].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    ax[1,0].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[1,0].set_xlabel('')
    ax[1,0].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    ax[1,0].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[1,0].set_ylim([2,5])
    ax[1,0].set_title('国债'+str(year)+'年')
    ax[1,0].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[1,0],0)
    # 1y
    year=1
    a = df[['国债'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[:,0].plot(ax=ax[1,1],label='国债'+str(year)+'年')
    ax[1,1].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    ax[1,1].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[1,1].set_xlabel('')
    ax[1,1].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    ax[1,1].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[1,1].set_ylim([0,5])
    ax[1,1].set_title('国债'+str(year)+'年')
    ax[1,1].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[1,1],0)

    # * P2.0 & P2.1 国开10&1y
    #10y
    year=10
    a = df[['国开'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[:,0].plot(ax=ax[2,0],label='国开'+str(year)+'年')
    ax[2,0].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    ax[2,0].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[2,0].set_xlabel('')
    ax[2,0].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    ax[2,0].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[2,0].set_ylim([2.5,6.5])
    ax[2,0].set_title('国开'+str(year)+'年')
    ax[2,0].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[2,0],0)
    # 1y
    year=1
    a = df[['国开'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[:,0].plot(ax=ax[2,1],label='国开'+str(year)+'年')
    ax[2,1].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    ax[2,1].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[2,1].set_xlabel('')
    ax[2,1].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    ax[2,1].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[2,1].set_ylim([0,6.5])
    ax[2,1].set_title('国开'+str(year)+'年')
    ax[2,1].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[2,1],0)


    # * P3.0 P3.1 国债/国开bp变动
    base = df['2021'].index[0]
    end = df['2021'].index[-1]
    ## gz
    name = '国债'  
    m = [ '6月', '1年', '3年', '5年','7年', '10年']
    l = [name+x for x in m]
    d = pd.DataFrame([],columns=range(6))
    d.loc[base] = df.loc[base,l].tolist()
    d.loc[end] = df.loc[end,l].tolist()
    d.loc['期间变动(BP)'] =( d.loc[end]-d.loc[base] )*100
    ## plott
    d.loc['期间变动(BP)'].plot(ax=ax[3,0],kind='bar',color='lightgrey')
    ax_=ax[3,0].twinx()
    d.loc[end].plot(ax=ax_,marker='o',color='#3778bf')
    d.loc[base].plot(ax=ax_,marker='o',color='#f0833a')
    ax[3,0].set_xticklabels(['6M','1Y','3Y','5Y','7Y','10Y'],rotation=0)
    ax[3,0].set_title(name+'收益率变动')
    ax_.legend([base.date(),end.date()],loc='lower right',\
        ncol=1,fontsize=10,frameon=False,)
    ax_.set_ylabel('(%)',fontsize=10)
    ax[3,0].set_ylabel('期间变动(BP)',fontsize=10)
    ## gk
    name = '国开'  
    m = [ '6月', '1年', '3年', '5年','7年', '10年']
    l = [name+x for x in m]
    d = pd.DataFrame([],columns=range(6))
    d.loc[base] = df.loc[base,l].tolist()
    d.loc[end] = df.loc[end,l].tolist()
    d.loc['期间变动(BP)'] =( d.loc[end]-d.loc[base] )*100
    ## plott
    d.loc['期间变动(BP)'].plot(ax=ax[3,1],kind='bar',color='lightgrey')
    ax_=ax[3,1].twinx()
    d.loc[end].plot(ax=ax_,marker='o',color='#3778bf')
    d.loc[base].plot(ax=ax_,marker='o',color='#f0833a')
    ax[3,1].set_xticklabels(['6M','1Y','3Y','5Y','7Y','10Y'],rotation=0)
    ax[3,1].set_title(name+'收益率变动')
    ax_.legend([base.date(),end.date()],loc='lower right',\
        ncol=1,fontsize=10,frameon=False,)
    ax[3,1].set_ylabel('期间变动(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)
    

    # * P4.0地方债-国债
    df['地方债-国债'] = (df['地方5年']-df['国债5年'])*100
    ax[4,0].fill_between(df.date['2013':],0,df['地方债-国债']['2013':],\
        label='地方债-国债(左:BP)',color='lightgrey',alpha=1)
    ax_=ax[4,0].twinx()
    df[['地方5年','国债5年']]['2013':].plot(ax=ax_,color=['#3778bf','#f0833a'])
    ax_.set_yticks(np.arange(1,6))
    ax[4,0].set_yticks(range(0,100,20))
    ax[4,0].legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['地方债:5年:AAA','国债:5年'],\
        loc=1,frameon=False,fontsize=10)
    ax[4,0].set_title('地方债-国债(5Y)')
    ax[4,0].set_ylim([0,90])
    ax_.set_ylim([1.5,5.5])
    ax[4,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P4.1国开债-国债
    df['国开债-国债'] = (df['国开10年']-df['国债10年'])*100
    ax[4,1].fill_between(df.date['2009':],0,df['国开债-国债']['2009':],\
        label='国开债-国债(左:BP)',color='lightgrey',alpha=1)
    ax_= ax[4,1].twinx()
    df[['国开10年','国债10年']]['2009':].plot(ax=ax_,\
        color=[ '#3778bf','#f0833a'])
    ax[4,1].set_title('国开债-国债(10Y)')
    ax[4,1].legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['国开债:10年','国债:10年'],\
        loc=1,frameon=False,fontsize=10)
    ax[4,1].set_ylim([0,160])
    ax_.set_ylim([2,6.5])
    ax[4,1].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P5.0存单-Dr007
    cash = do.get_data('cash_cost');cash.index = cash.date
    df['存单-DR007'] = (df['cd_3m_aaa+']-cash['DR007'])*100
    df['DR007'] = cash['DR007']
    ax[5,0].fill_between(df.date['2015':],0,df['存单-DR007']['2015':],\
        label='存单-DR007(左:BP)',color='lightgrey',alpha=1)
    ax_= ax[5,0].twinx()
    df[['cd_3m_aaa+','DR007']]['2015':].plot(ax=ax_,color=['#f0833a','#3778bf'])
    ax[5,0].set_title('存单与DR007')
    ax[5,0].legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['同业存单:3个月:AAA+','DR007'],\
        loc=1,ncol=2,frameon=False,fontsize=10)
    ax[5,0].set_ylim([-100,250])
    ax_.set_ylim([1.0,5.5])
    ax[5,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P5.1中票
    df[['中票_AAA_1y','中票_AAA_5y','中票_AA+_1y','中票_AA+_5y']]['2010':].\
        plot(ax=ax[5,1],color = ["#3778bf","brown","lightgrey","#f0833a"])
    ax[5,1].axhline(y=np.median(df['中票_AAA_5y']['2010':]),ls='--',color='grey',label='5Y:AAA:中位数')
    ax[5,1].axhline(y=np.median(df['中票_AA+_5y']['2010':]),ls='--',color='black',label='5Y:AA+:中位数')
    ax[5,1].set_xlabel('')
    ax[5,1].set_title('中票收益率')
    ax[5,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax[5,1].set_ylim([1,8])
    ax[5,1].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[5,1],0)

    fig.suptitle('市场利率水平',fontsize=24,y=1.01)
    fig.tight_layout()

    return fig

def rate_diff_fig():
    secondary_rate_sec = do.get_data('secondary_rate_sec')
    rates = do.get_data('rates'); rates.index = rates.date

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=11,figsize=(6*2,4*11), dpi=300)

    # * P0.0 期限利差1
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin1 = rates0['国债10年']-rates0['国债7年']
    margin2 = rates0['国开10年']-rates0['国开7年']
    df = pd.DataFrame([margin1,margin2])
    df.index = ['国债10Y-7Y','国开10Y-7Y']
    df  = df.T
    ax[0,0].plot(rates0['date'],margin1*100,'#3778bf',label="国债10Y-7Y")
    ax[0,0].plot(rates0['date'],margin2*100,'#f0833a',label='国开10Y-7Y')
    ax[0,0].set_title('期限利差1')
    ax[0,0].set_ylim([-30,30])
    ax[0,0].set_ylabel('(BP)',fontsize=10)
    ax[0,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[0,0])

    # * P0.1 期限利差2
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin3 = rates0['国债30年']-rates0['国债10年']
    margin4 = rates0['国债10年']-rates0['国债1年']
    margin5 = rates0['国债3年']-rates0['国债1年']
    df = pd.DataFrame([margin3,margin4,margin5])
    df.index = ['国债30Y-10Y','国开10Y-1Y','国开3Y-1Y']
    df  = df.T
    ax[0,1].plot(rates0['date'],margin3*100,'#3778bf',label="国债30Y-10Y")
    ax[0,1].plot(rates0['date'],margin4*100,'#f0833a',label='国开10Y-1Y')
    ax[0,1].plot(rates0['date'],margin5*100,'gray',label='国开3Y-1Y')
    ax[0,1].set_title('期限利差2')
    ax[0,1].set_ylabel('(BP)',fontsize=10)
    ax[0,1].set_ylim([-50,200])
    ax[0,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[0,1])

    # * P1.0 隐含税率
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    tax_rate = 1 - rates0['国债10年']/rates0['国开10年']
    ax[1,0].plot(rates0['date'],tax_rate,'#3778bf',label="隐含税率(%)")
    ax[1,0].set_title('国开与国债的隐含税率', )
    ax[1,0].set_ylim([0.05,0.20])
    ax[1,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[1,0])

    # * P1.1 国开与非国开的利差
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin6 = rates0['农发10年']-rates0['国开10年']
    margin7 = rates0['口行10年']-rates0['国开10年']
    df = pd.DataFrame([margin6,margin7])
    df.index = ['农发10Y-国开10Y','进出口10Y-国开10Y']
    df  = df.T    
    ax[1,1].plot(rates0['date'],margin6,'#3778bf',label="农发10Y-国开10Y")
    ax[1,1].plot(rates0['date'],margin7,'#f0833a',label='进出口10Y-国开10Y')
    ax[1,1].set_title('国开与非国开的利差')
    ax[1,1].set_ylabel('(BP)',fontsize=10)
    ax[1,1].set_ylim([-0.1,0.5])
    ax[1,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[1,1])

    # * P2.0 国债期限利差
    rates1 = rates.loc[rates['date'] >= '2007-01-01']
    #计算利差
    margin1 = rates1['国债10年']-rates1['国债1年']
    margin2 = rates1['国债10年']-rates1['国债5年']
    margin3 = rates1['国债3年']-rates1['国债1年']
    df = pd.DataFrame([margin1,margin2,margin3])
    df.index = ['10Y-1Y','10Y-5Y','3Y-1Y']
    df  = df.T    
    
    ax[2,0].plot(rates1['date'],margin1,'#3778bf',label="10Y-1Y")
    ax[2,0].plot(rates1['date'],margin2,'#f0833a',label='10Y-5Y')
    ax[2,0].plot(rates1['date'],margin3,'gray',label='3Y-1Y')
    ax[2,0].set_title('国债期限利差', )
    ax[2,0].set_ylabel('(%)',fontsize=10)
    ax[2,0].set_ylim([-1,3])
    ax[2,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)

    # * P2.1 国债、国开债10年-1年
    rates2 = rates.loc[rates['date'] >= '2008-01-01']
    margin4 = rates2['国债10年']-rates2['国债1年']
    margin5 = rates2['国开10年']-rates2['国开1年']
    df = pd.DataFrame([margin4,margin5])
    df.index = ['国债10Y-1Y','国开10Y-1Y']
    df  = df.T  
    ax[2,1].plot(rates2['date'],margin4,'#3778bf',label="国债10Y-1Y")
    ax[2,1].plot(rates2['date'],margin5,'#f0833a',label='国开10Y-1Y')
    ax[2,1].set_title('国债、国开债10年-1年', )
    ax[2,1].set_ylabel('(%)',fontsize=10)
    ax[2,1].set_ylim([-1,3])
    ax[2,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)

    # * P3.0 国债1年收益率与10年-1年利差
    rates3 = rates.loc[rates['date'] >= '2009-01-01']
    margin6 = rates3['国债10年']-rates3['国债1年']
    ax[3,0].grid(ls='--')
    ax[3,0].set_axisbelow(True)
    ax[3,0].scatter(rates3['国债1年'][:-1],margin6[:-1], marker='o',color = '', edgecolors='#3778bf')
    ax[3,0].scatter(rates3['国债1年'][:1],margin6[:1], marker='o',color = '', edgecolors='#f0833a')
    ax[3,0].set_title('国债1年收益率与10年-1年利差', )
    ax[3,0].annotate('当前值',xy=(rates3['国债1年'][:1],margin6[:1]),xytext=(rates3['国债1年'][:1],margin6[:1]-1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax[3,0].set_ylabel('(%)')

    # * P3.1 国债1年收益率与10年-1年利差
    rates3 = rates.loc[rates['date'] >= '2009-01-01']
    margin7 = rates3['国债30年']-rates3['国债10年']
    ax[3,1].grid(ls='--')
    ax[3,1].set_axisbelow(True)
    ax[3,1].scatter(rates3['国债10年'][:-1],margin7[:-1], marker='o',color = '', edgecolors='#3778bf')
    ax[3,1].scatter(rates3['国债10年'][:1],margin7[:1], marker='o',color = '', edgecolors='#f0833a')
    ax[3,1].set_title('国债10年收益率与30年-10年利差', )
    ax[3,1].annotate('当前值',xy=(rates3['国债10年'][:1],margin7[:1]),xytext=(rates3['国债10年'][:1],margin7[:1]-0.1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax[3,1].set_ylabel('(%)',fontsize=10)

    # * P4.0 国债2*5Y-(1Y+10Y)
    rates4 = rates.loc[rates['date'] >= '2015-10-08']
    gz = rates4['国债5年']*2 - ( rates4['国债1年'] + rates4['国债10年'])
    ax[4,0].plot(rates4['date'],gz,'#3778bf',label="2*5Y-(1Y+10Y)")
    ax[4,0].set_title('国债2*5Y-(1Y+10Y)')
    ax[4,0].set_ylim([-0.5,1])
    ax[4,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax[4,0].set_ylabel('(%)',fontsize=10)

    # * P4.1 国开债2*5Y-(1Y+10Y)
    rates4 = rates.loc[rates['date'] >= '2015-10-08']
    gkz = rates4['国开5年']*2 - ( rates4['国开1年'] + rates4['国开10年'])
    ax[4,1].plot(rates4['date'],gkz,'#3778bf',label="2*5Y-(1Y+10Y)")
    ax[4,1].set_title('国开债2*5Y-(1Y+10Y)', )
    ax[4,1].set_ylim([-0.5,1.5])
    ax[4,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax[4,1].set_ylabel('（%）',fontsize=10)

    # * P5.0 10年期国债与国开债-国债利差
    rates1 = rates.loc[rates['date'] >= '2009-01-05']
    margin1 = rates1['国开10年']-rates1['国债10年']
    ax[5,0].grid(ls='--')
    ax[5,0].set_axisbelow(True)
    ax[5,0].scatter(rates1['国债10年'][:-1],margin1[:-1], marker='o',color = '', edgecolors='#3778bf')
    ax[5,0].scatter(rates1['国债10年'][:1],margin1[:1], marker='o',color = '', edgecolors='#f0833a')
    ax[5,0].set_title('10年期国债与国开债-国债利差', )
    ax[5,0].annotate('当前值',xy=(rates1['国债10年'][:1],margin1[:1]),xytext=(rates1['国债10年'][:1],margin1[:1]+0.5),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax[5,0].set_ylabel('(%)',fontsize=10)

    # * P5.1 国开债-国债关键期限利差
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
    
    ax[5,1].plot(keymargin.index,keymargin['国债'],'#3778bf',label="国债")
    ax[5,1].plot(keymargin.index,keymargin['国开债'],'#f0833a',label='国开债')
    ax[5,1].set_ylim([1.5,4])
    ax[5,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[5,1].set_ylabel('(%)',fontsize=10)
    ax_=ax[5,1].twinx()
    ax_.bar(keymargin.index,keymargin['国开债-国债'], width=0.7, color='gray',alpha = 0.2,label='国开债-国债')
    ax_.set_ylim([0,50])
    ax_.legend(ncol=3,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('(BP)',fontsize=10)
    ax_.set_title('国开债-国债关键期限利差', )

    # * 6.0 农发、口行-国开利差:10年
    rates2 = rates.loc[rates['date'] >= '2016-01-04']
    rates2.index = rates2['date']
    rates2 = rates2[['国开10年', '农发10年', '口行10年']]
    rates2['农发-国开'] = (rates2['农发10年'] - rates2['国开10年'])*100

    rates2['口行-国开'] = (rates2['口行10年'] - rates2['国开10年'])*100

    ax[6,0].plot(rates2.index,rates2['国开10年'],'#3778bf',label="国开10年",linewidth=1)
    ax[6,0].plot(rates2.index,rates2['农发10年'],'#f0833a',label='农发10年',linewidth=1)
    ax[6,0].plot(rates2.index,rates2['口行10年'],'gray',label='口行10年',linewidth=1)
    ax[6,0].set_ylim([2.5,6])
    ax[6,0].legend(ncol=1,loc=2,fontsize=10,frameon=False)
    ax[6,0].set_ylabel('(%)',fontsize=10)
    ax_=ax[6,0].twinx()
    ax_.bar(rates2.index,rates2['农发-国开'], width=1, color='#f0833a',alpha = 0.2,label='农发-国开')
    ax_.bar(rates2.index,rates2['口行-国开'], width=1, color='gray',alpha = 0.2,label='口行-国开')
    ax_.set_ylim([0,40])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('(BP)',fontsize=10)
    ax_.set_title('农发、口行-国开利差:10年', )

    # * 6.1 国开债新老券利差
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
    
    ax[6,1].plot(df.index,df['200205'],'#3778bf',label="200205")
    ax[6,1].plot(df.index,df['200210'],'#f0833a',label='200210')
    ax[6,1].set_ylim([3,4])
    ax[6,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[6,1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax[6,1].set_ylabel('(%)',fontsize=10)
    ax_=ax[6,1].twinx()
    ax_.bar(df.index,df['200205-200210'], width=1, color='gray',alpha = 0.2,label='200205-200210')
    ax_.set_ylim([-1.5,1])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('(BP)',fontsize=10)
    ax_.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax_.set_title('国开债新老券利差', )
    l = do.set_axes_rotation(ax[6,1],45)

    # * 7.0 信用利差水平
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y','中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y', '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05']
    credit1  = rates1[-1:]
    credit2 = rates1.describe()[4:7]
    credit3 = rates1.loc[rates1.index == '2020-12-31']
    credit = pd.concat([credit1,credit2,credit3],axis=0)
    credit.index = [['现值','25分位数','中位数','75分位数','2020年底']]
    #转置
    credit= pd.DataFrame(credit.values.T, index=credit.columns, columns=credit.index)
    
    ax[7,0].plot(credit[['现值']],'#3778bf',label="现值")
    ax[7,0].plot(credit[['25分位数']],'#f0833a',label='25分位数')
    ax[7,0].plot(credit[['中位数']],'gray',label='中位数')
    ax[7,0].plot(credit[['75分位数']],'tomato',label='75分位数')
    ax[7,0].plot(credit[['2020年底']],'yellow',label='2020年底')
    ax[7,0].set_ylabel('(%)',fontsize=10)
    ax[7,0].set_title('信用利差水平', )
    ax[7,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[7,0],rotation = 45)

    # * 7.1 分评级信用利差
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y','中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y', '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05']
    
    ax[7,1].plot(rates1.index,rates1['中票_AAA_1y'],'#3778bf',label="AAA1年")
    ax[7,1].plot(rates1.index,rates1['中票_AAA_5y'],'#f0833a',label='AAA5年')
    ax[7,1].plot(rates1.index,rates1['中票_AA+_1y'],'gray',label='AA+1年')
    ax[7,1].plot(rates1.index,rates1['中票_AA+_5y'],'tomato',label='AA+5年')
    ax[7,1].set_title('分评级信用利差', )
    ax[7,1].set_ylim([1.5,6.5])
    ax[7,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)

    # * 8.0 中美利差:10年
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    #计算利差
    margin1 = (rates1['国债10年']-rates_us1['美债10年']) * 100
    df = pd.DataFrame([rates1['国债10年'],rates_us1['美债10年'],margin1])
    df.index = ['国债10年','美债10年','中美利差10年']
    df  = df.T

    ax[8,0].plot(rates_us1['date'],rates_us1['美债10年'],'#f0833a',label='美债10年')
    ax[8,0].plot(rates1['date'],rates1['国债10年'],'#3778bf',label="国债10年")
    ax[8,0].set_ylabel('（%）',fontsize=10)
    ax[8,0].set_ylim([0,6])
    ax[8,0].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[8,0].twinx()
    ax_.bar(margin1.index,margin1, width=1, color='gray',alpha = 0.2,label='中美利差10年')
    ax_.set_ylim([0,300])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:10年', )

    # * 8.1 中美利差:2年
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    #计算利差
    margin2 = (rates1['国债2年']-rates_us1['美债2年']) * 100
    df = pd.DataFrame([rates1['国债2年'],rates_us1['美债2年'],margin2])
    df.index = ['国债2年','美债2年','中美利差2年']
    df  = df.T

    ax[8,1].plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label='美债2年')
    ax[8,1].plot(rates1['date'],rates1['国债2年'],'#3778bf',label="国债2年")
    ax[8,1].set_ylabel('（%）',fontsize=10)
    ax[8,1].set_ylim([0,5])
    ax[8,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[8,1].twinx()
    ax_.bar(margin2.index,margin2, width=1, color='gray',alpha = 0.2,label='中美利差2年')
    ax_.set_ylim([-50,500])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:2年', )

    # * 9.0 中美利差:1年
    rates1 = rates.loc[rates['date'] >= '2010-06-21']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    #计算利差
    margin3 = (rates1['国债1年']-rates_us1['美债1年']) * 100
    df = pd.DataFrame([rates1['国债1年'],rates_us1['美债1年'],margin3])
    df.index = ['国债1年','美债1年','中美利差1年']
    df  = df.T

    ax[9,0].plot(rates_us1['date'],rates_us1['美债1年'],'#f0833a',label='美债1年')
    ax[9,0].plot(rates1['date'],rates1['国债1年'],'#3778bf',label="国债1年")
    ax[9,0].set_ylabel('（%）',fontsize=10)
    ax[9,0].set_ylim([-0.5,5])
    ax[9,0].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[9,0].twinx()
    ax_.bar(margin3.index,margin3, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    ax_.set_ylim([-50,500])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:1年', )

    # * 9.1 中美利差与人民币汇率
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates2 = rates.loc[rates['date'] >= '2011-01-04']
    rates2.index = rates2['date']
    rates_us2 = rates_us.loc[rates_us['date'] >= '2011-01-04']
    rates_us2.index = rates_us2['date']
    rates_us2 = rates_us2.dropna()
    #计算利差
    margin4 = ((rates2['国债10年']-rates_us2['美债10年']) * 100).dropna()
    df = pd.DataFrame([rates_us2['美元兑人民币'],margin4])
    df.index = ["美元兑人民币","中美利差10年"]
    df = df.T

    ax[9,1].plot(rates_us2['date'],rates_us2['美元兑人民币'],'#3778bf',label="美元兑人民币")
    ax[9,1].set_ylim([5,8])
    ax[9,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[9,1].twinx()
    ax_.plot(margin4.index,margin4,'#f0833a',label="中美利差10年")
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差与人民币汇率', )
    ax_.set_ylim([0,300])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)

    # * 10.0 中美市场利差
    cash_cost = do.get_data('cash_cost');cash_cost.index = cash_cost.date
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

    ax[10,0].plot(rates_us1['date'],rates_us1['libor_3m'],'#3778bf',label="美元libor3个月")
    ax[10,0].plot(cash_cost1['date'],cash_cost1['shibor_3m'],'#f0833a',label='人民币shibor3个月')
    ax[10,0].set_ylim([0,8])
    ax[10,0].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[10,0].set_ylabel('（%）',fontsize=10)
    ax_=ax[10,0].twinx()
    ax_.bar(margin5.index,margin5, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_ylim([0,700])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_title('中美市场利差', )

    # * 10.1 美债期限利差
    rates_us1 = rates_us.loc[rates_us['date'] >= '2007-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    margin6 = (rates_us1['美债10年']-rates_us1['美债2年']) * 100    
    df = pd.DataFrame([rates_us1['美债10年'],rates_us1['美债2年'],margin6])
    df.index = ["美债10年",'美债2年','美债10-2年']
    df  = df.T

    ax[10,1].plot(rates_us1['date'],rates_us1['美债10年'],'#3778bf',label="美债10年")
    ax[10,1].plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label="美债2年")
    ax[10,1].set_ylim([0,4.5])
    ax[10,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[10,1].set_ylabel('（%）',fontsize=10)
    ax_=ax[10,1].twinx()
    ax_.bar(margin6.index,margin6, width=1, color='gray',alpha = 0.2,label='美债10-2年')
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_ylim([0,400])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_title('美债期限利差', )

    plt.suptitle('利差情况',fontsize=24,y=1.01)
    fig.tight_layout()

    return fig


# cash = cash_fig()
# cash.savefig('流动性指标.pdf',dpi=100,bbox_inches='tight')

# ratelevel= rate_level_fig()
# ratelevel.savefig('市场利率水平.pdf',dpi=100,bbox_inches='tight')

# ratediff = rate_diff_fig()
# ratediff.savefig('利差水平.pdf',dpi=100,bbox_inches='tight')



