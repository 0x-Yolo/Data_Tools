import data_organize as do
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False


def indices():
    # 指数涨跌幅热力图

    df = do.get_data('bond_indices')
    df.index = df.date

    months=['2021-01','2021-02',\
        '2021-03','2021-04','2021-05','2021-06','2021-07'] 
    # years = range(2017,2022)

    stat = pd.DataFrame([],index = months,columns = df.columns[:-1])
    for m in months:
        df_tmp = df[m:m]
        stat.loc[m] = (df_tmp.iloc[-1,:-1]-df_tmp.iloc[0,:-1]) / df_tmp.iloc[0,:-1]
    # for y in years:
    #     df_tmp = df[str(y):str(y)].fillna(method='ffill')
    #     stat.loc[y] = (df_tmp.iloc[-1,:-1]-df_tmp.iloc[0,:-1]) / df_tmp.iloc[0,:-1]

    stat = stat.astype(float)*100
    plt.style.use({'font.size' : 12})     
    fig, ax = plt.subplots(nrows=1,ncols=1,\
        figsize=(10,6), dpi=300)
    sns.heatmap(stat,cmap="bwr",linewidths=1,ax=ax,\
                cbar=True, annot=True)
    plt.xticks(rotation=30)
    plt.yticks(rotation=0)
    
def rate_dif():
    def cal_p(num,l):
        l=np.sort(l).tolist()
        idx = l.index(num)
        return (idx+1)/(len(l))


    rates = do.get_data('rates')
    rates.index = rates.date

    # =======
    # 利率水平
    # =======
    base = '2021-06-30'; end = '2021-07-30'
    start = '2007-01-01'
    m = ['1年', '3年', '5年', \
        '7年', '10年', '20年', '30年']
    # import rateLevel
    # df = rateLevel.yieldCurve()

    name = '国债' ; l = [name+x for x in m]
    stat = pd.DataFrame(columns = m)
    stat.loc['当前水平gz'] = rates.loc[end,l].tolist()
    stat.loc['较上月变化gz'] = ((rates.loc[end,l]-rates.loc[base,l])*100).tolist()
    stat.loc['当前分位数gz'] = [100*cal_p(rates.loc[end,col], rates.loc[start:,col]) for col in l]
    stat.loc['上月末分位数gz'] = [100*cal_p(rates.loc[base,col], rates.loc[start:,col]) for col in l]
    
    name = '国开' ; l = [name+x for x in m] ; start = '2007-01-01'
    stat.loc['当前水平gk'] = rates.loc[end,l].tolist()
    stat.loc['较上月变化gk'] = ((rates.loc[end,l]-rates.loc[base,l])*100).tolist()
    stat.loc['当前分位数gk'] = [100*cal_p(rates.loc[end,col], rates.loc[start:,col]) for col in l]
    stat.loc['上月末分位数gk'] = [100*cal_p(rates.loc[base,col], rates.loc[start:,col]) for col in l]
    stat


    # =======
    # 利差水平
    # =======
    l = ['3-1','5-3','10-5','10-1','30-10']
    stat2 = pd.DataFrame(columns = l)
    # gz
    div = pd.DataFrame(columns = l); start = '2007-01-01'
    div['3-1'] = rates['国债3年'] - rates['国债1年']
    div['5-3'] = rates['国债5年'] - rates['国债3年']
    div['10-5'] = rates['国债10年'] - rates['国债5年']
    div['10-1'] = rates['国债10年'] - rates['国债1年']
    div['30-10'] = rates['国债30年'] - rates['国债10年']
    # stat2.loc['中位数gz'] = [np.quantile(div.loc[start:,col],0.5) for col in l]
    stat2.loc['当前水平gz'] = div.loc[end].tolist()
    stat2.loc['较上月变化gz'] = ((div.loc[end,l]-div.loc[base,l])*100).tolist()
    stat2.loc['当前分位数gz'] =[100*cal_p(div.loc[end,col], div.loc[start:,col]) for col in l]
    stat2.loc['上月末分位数gz']=[100*cal_p(div.loc[base,col], div.loc[start:,col]) for col in l]
    # gk
    div = pd.DataFrame(columns = l); start = '2007-01-01'
    div['3-1'] = rates['国开3年'] - rates['国开1年']
    div['5-3'] = rates['国开5年'] - rates['国开3年']
    div['10-5'] = rates['国开10年'] - rates['国开5年']
    div['10-1'] = rates['国开10年'] - rates['国开1年']
    div['30-10'] = rates['国开30年'] - rates['国开10年']
    # stat2.loc['中位数gk'] = [np.quantile(div.loc[start:,col],0.5) for col in l]
    stat2.loc['当前水平gk'] = div.loc[end].tolist()
    stat2.loc['较上月变化gk'] = ((div.loc[end,l]-div.loc[base,l])*100).tolist()
    stat2.loc['当前分位数gk'] =[100*cal_p(div.loc[end,col], div.loc[start:,col]) for col in l]
    stat2.loc['上月末分位数gk']=[100*cal_p(div.loc[base,col], div.loc[start:,col]) for col in l]

    stat.to_excel('利率水平.xlsx')
    stat2.to_excel('利差水平.xlsx')

def fundamt():
    df = do.get_data('fundAmt')
    df.index = df.date
    df = df[['货币基金份额', '股票基金份额', \
        '混合型基金份额','债券基金份额']]['2020':]

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(figsize=(6,4),dpi=300)
    ax.plot(df)
    plt.xticks(rotation=30)
    ax.legend(['货币基金份额', '股票基金份额', '混合型基金份额','债券基金份额'],\
        ncol=2,loc=3, bbox_to_anchor=(0.15,-0.35),borderaxespad = 0.0,frameon=False)
    
    return fig

    # fig.savefig('xw.jpg',dpi=300,bbox_inches='tight')