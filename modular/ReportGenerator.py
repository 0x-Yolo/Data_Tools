import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import sys
import plotly.express as px
import plotly.graph_objects as go

import data_organize as do
from primary_market_plot import GK,GZ

#基础的图像设置：
plt.style.use({'figure.figsize':(6, 4)})
set_style_A={'grid.linestyle': '--',
     'axes.spines.left': True,
     'axes.spines.bottom': True,
     'axes.spines.right': False,
     'axes.spines.top': False}
# sns.set_style("whitegrid")

# plt.rcParams['font.family']=['Kaiti SC']
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False

# 存一个数据库信息的文本
# path = input('输入存放数据库信息的地址')
for p in sys.path:
    if 'modular' in p :
        path = os.path.abspath(p +'/db.txt')
conn , engine = do.get_db_conn(path)
print('成功连接数据库finance')


# 时间设置
#去极值
def winsorize_series(series,min = 0.05,max = 0.95): #百分位法
    series = series.sort_values()
    q = series.quantile([min,max])
    return np.clip(series,q.iloc[0],q.iloc[1])
#归一化
def MaxMinNormal(data):
    """[0,1] normaliaztion"""
    x = (data - data.min()) / (data.max() - data.min())
    return x
#z-score
def std_series(se):
    se_std = se.std()
    se_mean = se.mean()
    return (se - se_mean)/se_std
#wind数据处理
def w_transform_data(data,select="id"):
    df=data.data
    df.value=df.value.astype(float)
    df=df.pivot_table(index=["time"],columns=[select]).fillna(method="ffill")
    df.index=pd.to_datetime(df.index)
    df=df.reset_index().set_index(["time"])
    return df
def volatility_series(series,window=14):
    return series.rolling(window).std()

def day(list):
    """寻找上周五"""
    for i in range(len(list)-1):
        d = list[i]
        d_yesterday = d - dt.timedelta(days = 1)
        if d_yesterday != list[i+1]:
            return i+1
            break
def spread(spread):
    if(spread!=0):
        if(spread > 0):
            a ='上行'+ str(spread)+'bp'
            return a
        if(spread < 0 ):
            spread = abs(spread)
            a ='下行'+ str(spread)+'bp'
            return a
    else:
        a ='保持不变'
        return a
#标注
def net_investment(net_investment):
    if(net_investment!=0):
        if(net_investment > 0):
            a ='净投放'+ str(net_investment)+'亿元'
            return a
        if(net_investment< 0 ):
            net_investment = abs(net_investment)
            a ='净回笼'+ str(net_investment)+'亿元'
            return a
    else:
        a ='净投放为0亿元'
        return a

class weeklyReport:
    def __init__(self, isMonth = False):

        self.pic_list=[]
        self.title_list=[]

        self.title="周报"

        self.isMonth = isMonth

    def print_all_jpg(self):
        if self.isMonth:
            download_path = './月报图片输出地址/'
        if not self.isMonth:
            download_path = './周报图片输出地址/'

        n = len(self.pic_list)
        for i in range(n):
            self.pic_list[i].savefig(download_path+'{}.jpg'.\
                format(self.title_list[i]),\
                bbox_inches='tight',dpi=300)
            print(self.title_list[i]+'.jpg'+'-打印成功')
        print("成功打印"+str(n)+"张图片")
        
    def print_all_fig(self):
        if self.isMonth:
            download_path = './月报图片输出地址/'
        if not self.isMonth:
            download_path = './周报图片输出地址/'

        n = len(self.pic_list)
        pdf = PdfPages(download_path+self.title+'.pdf')
        for pic in self.pic_list:
            pdf.savefig(pic,bbox_inches='tight')
            plt.close
        pdf.close()
        print("成功打印"+str(n)+"张图片,保存至\n" , download_path)

    def cash_cost(self,base_day ,endday ):
        startday = '2020-01-01'
        # 资金利率

        cash_cost = do.get_data('cash_cost',startday,endday)
        policy_rate = do.get_data('policy_rate',startday,endday)
        cash_cost.index = cash_cost['date']
        policy_rate.index = policy_rate['date']

        #计算本周与上周差值
        cash_cost_list = cash_cost.date.tolist()[::-1]
        policy_rate_list = policy_rate.date.tolist()[::-1]

        DR001_spread = (cash_cost['DR001'][-1]-cash_cost['DR001'][base_day])*100
        DR001_spread = round(DR001_spread, 2)  
        DR007_spread = (cash_cost['DR007'][-1]-cash_cost['DR007'][base_day])*100
        DR007_spread = round(DR007_spread, 2)  
        #绘制市场曲线

        #资金利率
        fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        plt.plot(cash_cost['DR001'],'#3778bf',label="DR001")
        plt.plot(cash_cost['DR007'],'#f0833a',label='DR007')
        plt.plot(policy_rate['逆回购利率：7天'].fillna(method='ffill'),'gray',label='逆回购利率：7天',ls = '--')
        
        if self.isMonth=='no':
            pass
        elif self.isMonth:
            plt.annotate('本月DR001' + spread(DR001_spread)+'\n'+'本月DR007' + spread(DR007_spread),xy=(cash_cost.index[-1],cash_cost['DR001'][-1]),xytext=(cash_cost['date'][-105],cash_cost['DR001'][-1]-1.4),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9,),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=7)
        else:
            plt.annotate('本周DR001' + spread(DR001_spread)+'\n'+'本周DR007' + spread(DR007_spread),\
            xy=(cash_cost.index[-1],cash_cost['DR001'][-1]),\
            xytext=(cash_cost['date'][-105],cash_cost['DR001'][-1]-1.4),\
            color="k",weight="bold",alpha=0.9,\
            arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9,),\
            bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},\
            fontsize=7)
        
        plt.title('资金利率', fontsize=12)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.05,-0.8),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.xticks(fontsize=10,rotation=45)
        plt.yticks(fontsize=10,rotation=0)

        self.pic_list.append(fig)
        self.title_list.append('资金利率')

        return fig

    def monetary_policy_tools(self,base_day,end ):
        # * 公开市场投放
        start='2020-10-01'
        # 读取数据
        df = do.get_data('monetary_policy_tools',start,end)
        df.index = df['date']
        
        # 数据处理，周频统计
        dql = ['MLF_到期','逆回购_到期','国库现金：到期量']
        tfl = ['MLF_数量_3m', 'MLF_数量_6m', '逆回购_数量_7d',\
            '逆回购_数量_14d', '逆回购_数量_28d', '逆回购_数量_63d',\
            'MLF_数量_1y', '国库现金：中标量']
        df_weekly = df.loc[:,['OMO：净投放', 'OMO：投放', 'OMO：回笼']].dropna()
        tmp_workday_list = []
        for idx in df.index:
            if np.isnan(df.loc[idx, 'OMO：投放'] ):
                tmp_workday_list.append(idx)
            else:
                tmp_workday_list.append(idx)
                df_weekly.loc[idx , 'MLF-逆回购-国库现金_回笼量'] =\
                    df.loc[tmp_workday_list, dql].sum().sum()
                df_weekly.loc[idx , 'MLF-逆回购-国库现金_投放量']= \
                    df.loc[tmp_workday_list, tfl].sum().sum()
                tmp_workday_list = []
        df_weekly['MLF-逆回购-国库现金_净投放量'] = \
            df_weekly['MLF-逆回购-国库现金_投放量']-df_weekly['MLF-逆回购-国库现金_回笼量']

        plt.style.use({'font.size' : 12}) 
        fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        ax.bar(df_weekly.index, df_weekly['MLF-逆回购-国库现金_投放量'],\
        width=3,label = '投放',edgecolor='black',color="#3778bf")
        ax.bar(df_weekly.index, -df_weekly['MLF-逆回购-国库现金_回笼量'],\
        width=3,color='grey',label = '回笼',edgecolor='black')
        ax.axhline(y=0,ls='-',color='k',lw=1)
        ax.plot(df_weekly.index, df_weekly['MLF-逆回购-国库现金_净投放量'],\
        color="#f0833a",lw=0.6,marker = 'o',label='净投放',markersize=2)
        
        if self.isMonth=='no':
            pass
        elif self.isMonth:
            plt.annotate('本月' + net_investment(df_weekly.loc[df_weekly.index>base_day,'MLF-逆回购-国库现金_净投放量'].sum()),\
                xy=(df_weekly.index[-1],df_weekly['MLF-逆回购-国库现金_净投放量'][-1]),xytext=(df_weekly.index[-12],df_weekly['MLF-逆回购-国库现金_净投放量'][-1]-7000),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=7)
        else:
            plt.annotate('本周' + net_investment(df_weekly['MLF-逆回购-国库现金_净投放量'][-1]),xy=(df_weekly.index[-1],df_weekly['MLF-逆回购-国库现金_净投放量'][-1]),xytext=(df_weekly.index[-12],df_weekly['MLF-逆回购-国库现金_净投放量'][-1]-7000),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=7)
        
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0,-0.8),borderaxespad = 0.,frameon=False,fontsize=10)
        plt.xticks(fontsize=10,rotation=45)
        plt.yticks(fontsize=10,rotation=0)
        ax.set_title('公开市场操作',fontsize=12)

        self.pic_list.append(fig)
        self.title_list.append('公开市场操作')

        return fig

    def interbank_deposit(self,base_day , endday):
        # * 存单价格与净融资量
        startday = '2020-01-01'

        # interbank_dps_vol = do.get_data('interbank_dps_vol',startday,endday)
        interbank_dps_vol = do.get_data('interbank_dps_vol_weekly')
        
        interbank_deposit = do.get_data('interbank_deposit',startday,endday)
        

        interbank_deposit.index = interbank_deposit['date']

        interbank_deposit_list = interbank_deposit.date.tolist()[::-1]
        cd_spread = (interbank_deposit['存单_股份行_1y'][-1]-interbank_deposit['存单_股份行_1y'][base_day])*100
        cd_spread = round(cd_spread, 2)  

        #绘制同业存单与MLF
        plt.style.use({'font.size' : 12})     
        fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        ax.bar(interbank_dps_vol['date'], interbank_dps_vol['净融资额(亿元)'],\
             width=4, color='Lightblue',label='1年股份行存单净融资量')
        ax.set_ylabel('（亿元）',fontsize=10)
        # ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0,-0.18),borderaxespad = 0.)  
        ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.72,-0.8),borderaxespad = 0.,frameon=False,fontsize=8)
        plt.xticks(fontsize=10,rotation=45)
        plt.yticks(range(-3000,6000,2000),fontsize=10)

        ax_=ax.twinx()
        ax_.grid(ls='--', axis='y')
        ax_.set_axisbelow(True)
        ax_.plot(interbank_deposit[['存单_股份行_1y']],'#3778bf',label="1年股份行存单利率")
        ax_.scatter(interbank_deposit.index,interbank_deposit['MLF：1y'],\
            label='MLF利率：1年', marker='o',color = '#f0833a',s=10)
        plt.yticks([1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75],fontsize=10)
        ax_.set_yticks([1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75])
        # ax.legend(ncol=2,loc=3, bbox_to_anchor=(0.5,-0.18),borderaxespad = 0.)  
        ax_.legend(ncol=2,loc=3, bbox_to_anchor=(-0.15,-0.8),borderaxespad = 0.,frameon=False,fontsize=8)
                
        if self.isMonth=='no':
            pass
        elif self.isMonth:
            ax_.annotate('本月' + spread(cd_spread),xy=(interbank_deposit.index[-1],interbank_deposit['存单_股份行_1y'][-1]),\
                xytext=(interbank_deposit['date'][-130],interbank_deposit['存单_股份行_1y'][-1]-1.3),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':4},fontsize=7)
        else:
            ax_.annotate('本周' + spread(cd_spread),xy=(interbank_deposit.index[-1],interbank_deposit['存单_股份行_1y'][-1]),\
                xytext=(interbank_deposit['date'][-130],interbank_deposit['存单_股份行_1y'][-1]-1.3),\
                color="k",weight="bold",alpha=0.9,arrowprops=\
                dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),\
                bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':4},fontsize=7)
        ax.set_title('MLF与同业存单')

        fig.tight_layout()
        self.pic_list.append(fig)
        self.title_list.append('MLF与同业存单')

        return fig

    def prmy_mkt_weekly_issue(self,startday,endday):
        # 一级市场发行 
        # 时间为近一周
        

        primary_market = do.get_data('primary_rate_sec', startday, endday)

        primary_market.index = primary_market['date']
        primary_market = primary_market.dropna(axis=0, how='any', thresh=None, subset=['全场倍数'], inplace=False)
        
        # 类型备注
        primary_market = primary_market[['债券简称', 'date', '发行期限(年)', '发行人全称','全场倍数']]
        primary_market.loc[primary_market['发行人全称'] == '中华人民共和国财政部' , '类型'] = '国债'
        primary_market.loc[(primary_market['发行人全称'] == '国家开发银行'), '类型'] = '国开债'
        primary_market.loc[((primary_market['发行人全称'] == '中国进出口银行')|(primary_market['发行人全称'] == '中国农业发展银行')), '类型'] = '非国开债'
        primary_market = primary_market.dropna(axis=0, how='any', thresh=None, subset=['类型'], inplace=False)
        
        # 国债
        primary_market_gz= primary_market[(primary_market['类型'] == '国债')]
        # 国开债
        primary_market_gkz= primary_market[(primary_market['类型'] == '国开债')]
        # 非国开债
        primary_market_fgkz= primary_market[(primary_market['类型'] == '非国开债')]

        # 绘图-本周利率债发行招标倍数
        fig,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        ax.grid(ls='--')
        ax.set_axisbelow(True)

        ax.scatter(primary_market_gz['发行期限(年)'],primary_market_gz['全场倍数'],label='国债', marker='o',color = 'darkorange',s=20)
        ax.scatter(primary_market_gkz['发行期限(年)'],primary_market_gkz['全场倍数'],label='国开债', marker='*',color = 'royalblue',s=20)
        ax.scatter(primary_market_fgkz['发行期限(年)'],primary_market_fgkz['全场倍数'],label='非国开债', marker='^',color = 'navy',s=20)
        
        if self.isMonth=='no':
            title = '上半年利率债招标倍数'
        elif self.isMonth:
            title = '本月利率债招标倍数'
        else:
            title = '本周利率债招标倍数'
        
        plt.title(title,fontsize=12)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.xticks(fontsize=10,rotation=0)
        plt.yticks(fontsize=10,rotation=0)

        self.pic_list.append(fig)
        self.title_list.append('利率债招标倍数')

        return fig

    def prmy_mkt_sentiment(self):
        # 调包画图 
        # 时间跨度为2020至今
        fig1 = GK()
        fig2 = GZ()

        self.pic_list.append(fig1)
        self.title_list.append('国开全场倍数与综收')

        self.pic_list.append(fig2)
        self.title_list.append('国债全场倍数与综收')
        
        return [fig1, fig2]

    def rates_change(self,start,end):
        # 利率债城投债中票bp变动情况 
        # end = dt.datetime.today()
        # start=dt.datetime.now() - dt.timedelta(days=7)
        df = do.get_data('rates',start,end)
        
        #### P1    
        d = pd.DataFrame(index=['国债','国开债','地方债'],\
            columns=['1Y','3Y','5Y','7Y','10Y'])
        d.loc['国债'] = ((df.iloc[-1,:5] - df.iloc[0,:5])*100).tolist()
        d.loc['国开债'] = ((df.iloc[-1,10:15] - df.iloc[0,10:15])*100).tolist()
        d.loc['地方债'] = ((df.iloc[-1,5:10] - df.iloc[0,5:10])*100).tolist()
        # plt.style.use({'font.size' : 12}) 
        fig1,ax = plt.subplots(figsize=(4.15,1.42 ),dpi = 300)

        d.plot(kind = 'bar',\
                    color = ["#3778bf","lightsteelblue","lightgray","peachpuff","#f0833a"],\
        edgecolor='black',ax=ax)
        plt.grid(ls='--', axis='y')
        plt.rc('axes', axisbelow=True)
        if self.isMonth=='no':
            title = '利率债半年度变动'
        elif self.isMonth:
            title = '利率债月度变动'
        else:
            title = '利率债周度变动'
        plt.title(title, fontsize=12)
        plt.legend(ncol=5,loc=1, bbox_to_anchor=(1.1,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.axhline(y = 0, color = "dimgray", ls = '-',linewidth = 1)
        plt.xticks(fontsize=10,rotation=0)
        plt.yticks(fontsize=10,rotation=0)
        plt.ylabel("(BP)",fontsize=10)
        self.pic_list.append(fig1)
        self.title_list.append('利率债bp变动')
        
        #### P2
        fig2,ax = plt.subplots(figsize=(4.15,1.42 ),dpi = 300)
        d = pd.DataFrame(index=['AAA','AA+','AA'],\
        columns=['城投1Y','城投3Y','城投5Y','城投7Y'])
        d.loc['AAA']=((df.iloc[-1,15:19] - df.iloc[0,15:19])*100).tolist()
        d.loc['AA+']=((df.iloc[-1,19:23] - df.iloc[0,19:23])*100).tolist()
        d.loc['AA']=((df.iloc[-1,23:27] - df.iloc[0,23:27])*100).tolist()

        d.plot(kind = 'bar',\
                    color = ["#3778bf","lightsteelblue","lightgray","#f0833a"],\
        edgecolor='black',ax=ax)
        plt.grid(ls='--', axis='y')
        plt.rc('axes', axisbelow=True)
        
        if self.isMonth=='no':
            title = '城投债收益率半年度变动'
        elif self.isMonth:
            title = '城投债收益率月度变动'
        else:
            title = '城投债收益率周度变动'

        plt.title(title, fontsize=12)
        plt.legend(ncol=5,loc=1, bbox_to_anchor=(1.15,-0.2),borderaxespad = 0.,frameon=False,fontsize=10)
        plt.axhline(y = 0, color = "dimgray", ls = '-',linewidth = 1)
        plt.xticks(fontsize=10,rotation=0)
        plt.yticks(fontsize=10,rotation=0)
        plt.ylabel("(BP)")
        self.pic_list.append(fig2)
        self.title_list.append('城投债bp变动')

        #### P3
        d = pd.DataFrame(index=['AAA','AA+','AA','AA-'],\
        columns=['中票短融1Y','中票短融3Y','中票短融5Y'])
        d.loc['AAA']=((df.iloc[-1,27:30] - df.iloc[0,27:30])*100).tolist()
        d.loc['AA+']=((df.iloc[-1,30:33] - df.iloc[0,30:33])*100).tolist()
        d.loc['AA']=((df.iloc[-1,33:36] - df.iloc[0,33:36])*100).tolist()
        d.loc['AA-']=((df.iloc[-1,36:39] - df.iloc[0,36:39])*100).tolist()

        # plt.style.use({'font.size' : 12}) 
        fig3,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        d.plot(kind = 'bar',\
                    color = ["#3778bf","lightsteelblue","#f0833a"],\
        edgecolor='black',ax=ax)
        plt.grid(ls='--', axis='y')
        plt.rc('axes', axisbelow=True)
        
        if self.isMonth=='no':
            title = '中票短融收益率半年度变动'
        elif self.isMonth:
            title = '中票短融收益率月度变动'
        else:
            title = '中票短融收益率周度变动'

        plt.title(title,fontsize=12)
        plt.legend(ncol=5,loc=1, bbox_to_anchor=(1.1,-0.2),borderaxespad = 0.,frameon=False,fontsize=10)
        plt.axhline(y = 0, color = "dimgray", ls = '-',linewidth = 1)
        plt.xticks(fontsize=10,rotation=0)
        plt.yticks(fontsize=10,rotation=0)
        plt.ylabel("(BP)")
        self.pic_list.append(fig3)
        self.title_list.append('中票短融bp变动')

        return [fig1,fig2,fig3]

    def fig_net_data(self,start,end, heat=False):
        df_net_week = do.get_data('Net_buy_bond',start , end)

        df_net_week.loc[df_net_week['期限'] == '1年及1年以下' , '期限备注'] = '短债'
        df_net_week.loc[(df_net_week['期限'] == '1-3年') , '期限备注'] = '中债'
        df_net_week.loc[(df_net_week['期限'] == '5-7年')|(df_net_week['期限'] == '7-10年')|(df_net_week['期限'] == '10-15年')|(df_net_week['期限'] == '15-20年')
           |(df_net_week['期限'] == '20-30年')|(df_net_week['期限'] == '30年以上') , '期限备注'] = '长债'
        df_net_week.loc[(df_net_week['期限'] == '3-5年') , '期限备注'] = '中长债'
        
        co_list = df_net_week['机构名称'].unique()

        stat = pd.DataFrame([],columns = co_list,index = ['短债', '中债','中长债','长债'])
        for co in co_list:
            df_co = df_net_week[df_net_week['机构名称'] == co]
            stat[co] = df_co.groupby(['期限备注'])['合计'].sum()
        stat2 = pd.DataFrame([],columns = co_list,index = ['7-10年\n国债新债', '7-10年\n政金债新债'])
        for co in co_list:
            df_co = df_net_week[(df_net_week['机构名称'] == co)&(df_net_week['期限'] == '7-10年')]
            stat2.loc['7-10年\n国债新债',co] = df_co.groupby('date')['国债-新债'].sum().sum()
            stat2.loc['7-10年\n政金债新债',co] = df_co.groupby('date')['政策性金融债-新债'].sum().sum()

        # 画图
        plt.style.use({'font.size' : 10})     
        fig1, ax = plt.subplots(nrows=1,ncols=1,\
        figsize=(4.15,1.42), dpi=300)

        if heat:
            stat = np.sign(stat)
            sns.heatmap(stat,cmap="OrRd",linewidths=1,ax=ax,\
                cbar=False, )

        else:
            tick_label = ["农村金融机构","基金公司及产品","保险公司",'外资银行']
            stat = stat[tick_label]
            x = np.arange(4)
            y1 = stat.iloc[0,:]
            y2 = stat.iloc[1,:]
            y3 = stat.iloc[2,:]
            y4 = stat.iloc[3,:]
            bar_width = 0.2

            ax.grid(ls='--', axis='y')
            ax.set_axisbelow(True)

            ax.bar(x, y1, bar_width, align="center",color=sns.xkcd_rgb['bluish'], edgecolor='black', label="短债")
            ax.bar(x+bar_width, y2, bar_width, color=sns.xkcd_rgb['dull yellow'], edgecolor='black', align="center", label="中债")
            ax.bar(x+2*bar_width, y3, bar_width,color=sns.xkcd_rgb['dull red'], edgecolor='black', align="center", label="中长债")
            ax.bar(x+3*bar_width, y4, bar_width,color=sns.xkcd_rgb['grey'], edgecolor='black', align="center", label="长债")
            ax.set_ylabel("（亿元）",fontsize = 10)
            ax.set_xticks(x+bar_width*1.5)
            ax.set_xticklabels(tick_label,fontsize=8)
            
            ax.axhline(y = 0, color = "dimgray", ls = '-',linewidth = 1)
            # ax.legend(fontsize=15)
            # ax.legend(ncol=3,loc=3, bbox_to_anchor=(0.22,-0.32),borderaxespad = 0.,frameon=False)
            ax.legend(ncol=4,loc=1, bbox_to_anchor=(1,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)
            
        ax.set_title('各机构久期分布',fontsize=12)
        self.pic_list.append(fig1)
        self.title_list.append('各机构久期分布')

        #P2
        plt.style.use({'font.size' : 10})     
        fig2, ax = plt.subplots(nrows=1,ncols=1,\
        figsize=(4.15,1.42), dpi=300)

        if heat:
            stat2 = np.sign(stat2)
            sns.heatmap(stat2.astype(int),cmap="OrRd",linewidths=1,ax=ax,\
                cbar=False,square=False)
        else:
            tick_label = ["农村金融机构","基金公司及产品","保险公司",'外资银行']
            stat2 = stat2[tick_label]
            x = np.arange(4)
            y1 = stat2.iloc[0,:]
            y2 = stat2.iloc[1,:]
            bar_width = 0.25
            ax.grid(ls='--', axis='y')
            ax.set_axisbelow(True)
            ax.bar(x, y1, bar_width, align="center",color=sns.xkcd_rgb['bluish'], edgecolor='black', label="7-10年国债-新债")
            ax.bar(x+bar_width, y2, bar_width, color=sns.xkcd_rgb['dull red'], edgecolor='black', align="center", label="7-10年政策性金融债-新债")
            ax.set_ylabel("（亿元）",fontsize=10)
            ax.set_xticks(x+bar_width/2)
            ax.set_xticklabels(tick_label,fontsize=8)
            ax.axhline(y = 0, color = "dimgray", ls = '-',linewidth = 1)
            # ax.legend(fontsize=15)
            ax.legend(ncol=5,loc=1, bbox_to_anchor=(1.1,-0.3),borderaxespad = 0.,fontsize=10,frameon=False)

        if self.isMonth=='no':
            title = '各机构7-10年政金新债、国债新债半年度净买入情况'
        elif self.isMonth:
            title = '各机构7-10年政金新债、国债新债月度净买入情况'
        else:
            title = '各机构7-10年政金新债、国债新债周度净买入情况'
        ax.set_title(title,fontsize=12)

        self.pic_list.append(fig2)
        self.title_list.append('各机构7-10年政金新债、国债新债净买入情况')

        return [fig1,fig2]

    def net_buy_amt(self):
        # pdf
        df_net = do.get_data('Net_buy_bond')
        gz10y = do.get_data('rates')[['国债10年','date']]
        gz10y.rename(columns={'国债10年':'十年期国债收益率'}, inplace = True)
        gz10y.index = gz10y.date

        co_list = df_net['机构名称'].unique().tolist()
        # pic_list = []
        for windows in [10,20]:
            
            for co in co_list[:8]:
                df_co = df_net.loc[(df_net['机构名称'] == co) ]

                # 一个属于机构co的dataframe ;暂时先用含双休日的日期索引
                stat_table = pd.DataFrame(index = df_co.date.unique())
                stat_table1 = pd.DataFrame(index = df_co.date.unique())
                stat_table2 = pd.DataFrame(index = df_co.date.unique())

                for name , grp in df_co.groupby(['期限']):
                    # name分期限

                    stat_table.loc[:, name+'国债-新债'] = grp.groupby(['date'])['国债-新债'].sum().tolist()
                    stat_table1.loc[:, name+'政策性金融债-新债'] = grp.groupby(['date'])['政策性金融债-新债'].sum().tolist()
                    stat_table2.loc[:, name+'地方政府债'] = grp.groupby(['date'])['地方政府债'].sum().tolist()

                # 以不含双休日的日期索引为准
                stat_table = pd.merge(stat_table,gz10y.loc[:,'十年期国债收益率'],how='inner',
                                    left_index=True,right_index=True)


                plt.style.use({'font.size' : 12}) 
                fig, ax = plt.subplots(nrows=2,ncols=2,figsize = (20,8), dpi=100)

                pd.Series.rolling(stat_table['7-10年国债-新债'],window=windows).mean().plot(\
                    ax = ax[0][0],label='7-10年国债-新债'+'(MA{})'.format(str(windows)))
                ax[0][0].axhline(y=0, c="y", ls="--", lw=1.5)
                ax_right = ax[0][0].twinx()
                stat_table[['十年期国债收益率']].plot(ax = ax_right ,color = 'red')
                ax[0][0].set_title('7-10年国债-新债')
                ax[0,0].legend(ncol=1,loc=3, bbox_to_anchor=(0,-0.3),borderaxespad = 0.)
                ax_right.legend(ncol=1,loc=3, bbox_to_anchor=(0.78,-0.3),borderaxespad = 0.)

                pd.Series.rolling(stat_table1['7-10年政策性金融债-新债'],window=windows).mean().plot(\
                    ax = ax[0][1],label='7-10年政策性金融债-新债'+'(MA{})'.format(str(windows)))
                ax[0][1].axhline(y=0, c="y", ls="--", lw=1.5)
                ax_right = ax[0][1].twinx()
                stat_table[['十年期国债收益率']].plot(ax = ax_right ,color = 'red')
                ax[0][1].set_title('7-10年政策性金融债-新债')
                ax[0,1].legend(ncol=1,loc=3, bbox_to_anchor=(0,-0.3),borderaxespad = 0.)
                ax_right.legend(ncol=1,loc=3, bbox_to_anchor=(0.78,-0.3),borderaxespad = 0.)

                pd.Series.rolling(stat_table2['7-10年地方政府债'],window=windows).mean().plot(\
                    ax = ax[1][0],label='7-10年地方政府债'+'(MA{})'.format(str(windows)))
                ax[1][0].axhline(y=0, c="y", ls="--", lw=1.5)
                ax_right = ax[1][0].twinx()
                stat_table[['十年期国债收益率']].plot(ax = ax_right ,color = 'red')
                ax[1][0].set_title('7-10年地方政府债')
                ax[1,0].legend(ncol=1,loc=3, bbox_to_anchor=(0,-0.3),borderaxespad = 0.)
                ax_right.legend(ncol=1,loc=3, bbox_to_anchor=(0.78,-0.3),borderaxespad = 0.)

                fig.delaxes(ax[1,1])
                plt.suptitle(co)
                plt.tight_layout()  

                self.pic_list.append(fig)
                self.title_list.append('利率债净买入_{}_MA:{}'.format(co,windows))
        return 

    def secondary_credit(self,start,end):
        CreditBondTrading_stat = do.get_data('secondary_credit_sec_stat',start,end)
        #按时间排序，取最近的10天
        CreditBondTrading_stat= CreditBondTrading_stat.sort_values(by='date')
        # CreditBondTrading_stat = CreditBondTrading_stat[-days:]
        CreditBondTrading_stat.index = CreditBondTrading_stat['date']
        date = CreditBondTrading_stat.index
        date = date.strftime('%m-%d')

        # P1
        fig1,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)

        plt.bar(date,CreditBondTrading_stat['笔数'], width=0.7, color='#f0833a',label="笔数")
        
        if not self.isMonth:
            for a,b in zip(date,CreditBondTrading_stat['笔数']):
                plt.text(a,200, '%.f' % b, ha='center', va= 'top',fontsize=8)
        
        # plt.yticks([500,1000,1500])
        plt.xticks(fontsize=10,rotation=45)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.25,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)

        plt.twinx()
        plt.plot(date,CreditBondTrading_stat['均价'],'#3778bf',label="均价")
        
        if not self.isMonth:
            for a,b in zip(date,CreditBondTrading_stat['均价']):
                plt.text(a, b+0.001, '%.2f' % b, ha='center', va= 'center',fontsize=8)

        # plt.yticks([3.20,3.25,3.30,3.35,3.40,3.45,3.50])
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.6,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.title('信用债 均价&笔数',fontsize=12)
        self.pic_list.append(fig1)
        self.title_list.append('信用债 均价&笔数')

        # P2
        fig2,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)

        plt.bar(date,CreditBondTrading_stat['情绪指数'], width=0.7, color='#f0833a',label="情绪指数")
        if not self.isMonth:
            for a,b in zip(date,CreditBondTrading_stat['情绪指数']):
                plt.text(a,0.5, '%.2f' % b, ha='center', va= 'top',fontsize=8)
        # plt.yticks([0,1,2,3,4])
        plt.xticks(fontsize=10,rotation=45)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.15,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)

        plt.twinx()
        plt.plot(date,CreditBondTrading_stat['风险偏好指数'],'#3778bf',label="风险偏好指数")
        if not self.isMonth:
            for a,b in zip(date,CreditBondTrading_stat['风险偏好指数']):
                plt.text(a, b+0.001, '%.2f' % b, ha='center', va= 'center',fontsize=8)

        # plt.yticks([2.65,2.85,3.05,3.25,3.45,3.65,3.85])
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.5,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.title('信用债 风险偏好&情绪指数',fontsize=12)
        self.pic_list.append(fig2)
        self.title_list.append('信用债 风险偏好&情绪指数')

        # P3
        fig3,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)

        plt.plot(date,CreditBondTrading_stat['信用扩张指数'],'#f0833a',label="信用分歧指数（左轴）")
        if not self.isMonth:
            for a,b in zip(date,CreditBondTrading_stat['信用扩张指数']):
                plt.text(a,b+0.001, '%.2f' % b, ha='center', va= 'top',fontsize=8)
        # plt.yticks([1.2,1.3,1.4,1.5,1.6])
        plt.xticks(fontsize=10,rotation=45)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)

        plt.twinx()
        plt.plot(date,CreditBondTrading_stat['平均期限'],'#3778bf',label="平均期限（右轴）")
        if not self.isMonth:
            for a,b in zip(date,CreditBondTrading_stat['平均期限']):
                plt.text(a, b+0.001, '%.2f' % b, ha='center', va= 'center',fontsize=8)

        # plt.yticks([1.6,1.7,1.8,1.9,2.0])
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.6,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.title('信用债 平均期限&扩张指数',fontsize=12)
        self.pic_list.append(fig3)
        self.title_list.append('信用债 平均期限&扩张指数')

        return [fig1,fig2,fig3]

    def secondary_rate(self,start,end):
        # * 二级利率债，需要选定券种
        # df_raw = pd.read_excel('/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/交易数据/利率债.xlsx')
        df = do.get_data('secondary_rate_sec',start,end)

        #筛选200215
        df_200215 = df.loc[df['代码'] == '200215.IB']
        a = df_200215.groupby(['date'])['价格'].count()
        b = df_200215.groupby(['date'])['价格'].agg([np.mean,np.max,np.min])
        c = df_200215.groupby(['date'])['昨日平均'].mean()
        d = df_200215.groupby(['date'])['债券余额(亿)'].mean()
        df_200215 = pd.concat([a,b,c,d],axis=1)
        #筛选210205
        df_210205 = df.loc[df['代码'] == '210205.IB']
        a = df_210205.groupby(['date'])['价格'].count()
        b = df_210205.groupby(['date'])['价格'].agg([np.mean,np.max,np.min])
        c = df_210205.groupby(['date'])['昨日平均'].mean()
        d = df_210205.groupby(['date'])['债券余额(亿)'].mean()
        df_210205 = pd.concat([a,b,c,d],axis=1)
        # 合并
        df_merge = pd.concat([df_200215['价格'],df_210205['价格']],axis=1)
        df_merge.columns = ['200215','210205']
        date = df_merge.index
        date = date.strftime('%m-%d')
        df_merge.index = date

        # 200215&210205
        fig1,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        df_merge.plot(kind = 'bar',color = ["#3778bf","#f0833a"],alpha = 0.3,ax=ax)
        plt.xlabel('')
        # plt.grid(ls='--', axis='y')
        # plt.rc('axes', axisbelow=True) 

        plt.xticks(fontsize=10,rotation=45)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.2,-0.7),borderaxespad = 0.,fontsize=10,frameon=False)

        plt.twinx()
        plt.plot(date,df_200215['mean'],'#3778bf',label="200215均价")
        plt.plot(date,df_210205['mean'],'#f0833a',label="210205均价")
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.5,-0.7),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.title('200215&210205',fontsize=12)
        self.pic_list.append(fig1)
        self.title_list.append('200215&210205')

        
        #筛选200016
        df_200016 = df.loc[df['代码'] == '200016.IB']
        a = df_200016.groupby(['date'])['价格'].count()
        b = df_200016.groupby(['date'])['价格'].agg([np.mean,np.max,np.min])
        c = df_200016.groupby(['date'])['昨日平均'].mean()
        d = df_200016.groupby(['date'])['债券余额(亿)'].mean()
        df_200016 = pd.concat([a,b,c,d],axis=1)
        #把日期转为str
        date = df_200016.index
        date = date.strftime('%m-%d')
        #画图
        fig2,ax = plt.subplots(figsize=(4.15,1.42),dpi = 300)
        plt.bar(date, df_200016['价格'], width=0.7, color='#f0833a',alpha = 0.2,label="交易笔数")
        plt.xticks(fontsize=10,rotation=45)
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(-0.05,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)

        plt.twinx()
        plt.plot(date,df_200016['mean'],'#3778bf',label="Mean")
        plt.plot(date,df_200016['amax'],"lightsteelblue",label="Max",ls='--')
        plt.plot(date,df_200016['amin'],"lightgray",label="Min",ls='--')
        plt.legend(ncol=3,loc=3, bbox_to_anchor=(0.3,-0.65),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.title('200016',fontsize=12)
        self.pic_list.append(fig2)
        self.title_list.append('200016')

        return [fig1, fig2]

    def r_dr(self,start = '2019-07-01'):
        """
        R007-DR007利差
        超储率
        """
        df = do.get_data('cash_cost')
        df.index = df.date

        df = df.loc[df.date>start]
        df['R007-DR007'] = df['R007']-df['DR007']
        df = df.loc[df['R007-DR007']<=2] # 去除异常值

        plt.style.use({'font.size' : 10})  
        fig, ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
        ax.fill_between(df.date, 0, df['R007-DR007'].rolling(10).mean()*100, \
             label = 'R007-DR007:MA10',color='lightgrey',alpha=1)
        plt.xticks(rotation=45)

        ax_=ax.twinx()
        ax_.plot(df.date,df['R007'],lw=1,label='R007',color='black'); 
        ax_.plot(df.date,df['DR007'],lw=1,label='DR007',color='#f0833a')
        # df[['R007','DR007']].plot(ax=ax_)
        ax_.set_title('R007-DR007',fontsize=12)
        ax.legend(ncol=1,loc=3, bbox_to_anchor=(-0.05,-0.8),borderaxespad = 0.,frameon=False,fontsize=10)
        ax_.legend(ncol=2,loc=3, bbox_to_anchor=(0.47,-0.8),borderaxespad = 0.,frameon=False,fontsize=10)

        self.pic_list.append(fig); self.title_list.append('D-DR利差')
        return fig 
    def gk_gz(self,start='2015-01-01'):
        # 
        df = do.get_data('rates')
        df.index = df.date
        df = df.loc[df.date > start]

        df['国开债-国债'] = df['国开10年']-df['国债10年']

        fig, ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
        ax.fill_between(df.date, 0, df['国开债-国债'].rolling(1).mean()*100, \
             label = '国开债-国债',color='lightgrey',alpha=0.9)
        # plt.xticks(rotation=0,fontsize=10)
        ax_=ax.twinx()
        ax_.plot(df[['国开10年']],lw=1,label='国开10年',color='black'); 
        ax_.plot(df[['国债10年']],lw=1,label='国债10年',color='#f0833a')
        # df[['国开10年','国债10年']].plot(ax=ax,lw=1)
        ax_.set_xlabel('');

        ax.set_title('国开债-国债',fontsize=12)
        ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.68,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
        ax_.legend(ncol=2,loc=3, bbox_to_anchor=(-0.05,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
        self.pic_list.append(fig); self.title_list.append('国开债-国债')
        return fig
    def term_spread(self):
        # 期限利差
        plt.style.use({'font.size' : 10}) 
        df = do.get_data('rates')
        df = df.loc[df.date>'2015-01-01']
        df['国开债_10y-1y'] = df['国开10年']-df['国开1年']
        df.index = df.date
        # 国开10-1
        fig1, ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
        (df[['国开债_10y-1y']]*1).plot(ax=ax)
        ax.set_title('国开债_10y-1y',fontsize=12)
        ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.27,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
        ax.set_xlabel('')
        ax.set_yticks(np.arange(5)/2)
        # 国开10-R007
        cash_cost = do.get_data('cash_cost');cash_cost.index=cash_cost.date
        cash_cost = cash_cost.loc[cash_cost.date>'2016-01-01']
        df['10年国开-R007(MA30)'] = (df['国开10年']-cash_cost['R007'])*100
        fig2, ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
        df[['10年国开-R007(MA30)']].dropna().\
            rolling(30).mean().plot(ax=ax)
        ax.set_xlabel('')
        ax.set_yticks(np.arange(50,250,30))
        ax.legend(ncol=1,loc=3, bbox_to_anchor=(0.2,-0.6),borderaxespad = 0.,fontsize=10,frameon=False)
        ax.set_title('10年国开-R007(MA30)',fontsize=12)
        # self.pic_list.append(fig); self.title_list.append('国开债_10y-1y')
        
        return [fig1, fig2]
    def most_net_buy_amt(self,start , end):
        # 
        df = do.get_data('Net_buy_bond', start, end)
        co_list = df['机构名称'].unique().tolist()
        
        rate, ax = plt.subplots(nrows=1,ncols=2,figsize=(6,4), dpi=300, \
            sharey = True)
        # 期限:7-10 券种:利率债
        rate_secs=['国债-新债', '国债-老债', '政策性金融债-新债', '政策性金融债-老债',\
            '地方政府债']
        df.loc[df['期限']=='7-10年'].groupby(['机构名称']).sum(['date'])\
            [rate_secs].sum(axis=1).plot(kind='barh', ax=ax[0])
        ax[0].set_ylabel('')
        ax[0].set_title('利率债(7-10年)净买入',fontsize=12)
        # 期限:长 券种:利率债
        # rate2, ax = plt.subplots(figsize=(4,6), dpi=300)
        #  '10-15年', '15-20年','20-30年', '30年以上'
        df.loc[(df['期限']=='1-3年')|(df['期限']=='3-5年')|(df['期限']=='5-7年') ].\
            groupby(['机构名称']).sum(['date'])\
            [rate_secs].sum(axis=1).plot(kind='barh', ax=ax[1])
        ax[1].set_ylabel('')
        ax[1].set_title('利率债(1-7年)净买入',fontsize=12)
        rate.tight_layout()

        # 券种:信用债
        credit, ax = plt.subplots(nrows=1,ncols=2,figsize=(6,4), dpi=300,\
            sharey=True)
        credit_secs = [ '中期票据','短期/超短期融资券', '企业债', '地方政府债', '资产支持证券']
        df.loc[df['期限']!='1年及1年以下'].groupby(['机构名称']).sum(['date'])\
            [credit_secs].sum(axis=1).plot(kind='barh', ax=ax[0])
        ax[0].set_ylabel('')
        ax[0].set_title('信用债(1年以上)净买入', fontsize=12)
        
        # credit2, ax = plt.subplots(figsize=(4,6), dpi=300)
        credit_secs = [ '中期票据','短期/超短期融资券', '企业债', '地方政府债', '资产支持证券']
        df.loc[df['期限']=='1年及1年以下'].groupby(['机构名称']).sum(['date'])\
            [credit_secs].sum(axis=1).plot(kind='barh', ax=ax[1])
        ax[1].set_ylabel('')
        ax[1].set_title('信用债(1年及以下)净买入', fontsize=12)
        credit.tight_layout()
        return rate, credit
    def fig_net_heat():
        df_net_week = do.get_data('Net_buy_bond','2021-06-01','2021-06-22')

        df_net_week.loc[df_net_week['期限'] == '1年及1年以下' , '期限备注'] = '短债'
        df_net_week.loc[(df_net_week['期限'] == '1-3年') , '期限备注'] = '中债'
        df_net_week.loc[(df_net_week['期限'] == '5-7年')|(df_net_week['期限'] == '7-10年')|(df_net_week['期限'] == '10-15年')|(df_net_week['期限'] == '15-20年')
           |(df_net_week['期限'] == '20-30年')|(df_net_week['期限'] == '30年以上') , '期限备注'] = '长债'
        df_net_week.loc[(df_net_week['期限'] == '3-5年') , '期限备注'] = '中长债'
        
        co_list = df_net_week['机构名称'].unique()
        co_list = ['农村金融机构', '证券公司','保险公司', '基金公司及产品','外资银行']

        stat = pd.DataFrame([],columns = co_list,index = ['短债', '中债','中长债','长债','7-10年\n国债新债', '7-10年\n政金债新债'])
        stat = pd.DataFrame([],columns = co_list,index = ['短债', '中债','中长债','长债'])#,'7-10年\n国债新债', '7-10年\n政金债新债'])
        
        for co in co_list:
            df_co = df_net_week[df_net_week['机构名称'] == co]
            stat[co] = df_co.groupby(['期限备注'])['合计'].sum()

            df_co = df_net_week[(df_net_week['机构名称'] == co)&(df_net_week['期限'] == '7-10年')]
            # stat.loc['7-10年\n国债新债',co] = df_co.groupby('date')['国债-新债'].sum().sum()
            # stat.loc['7-10年\n政金债新债',co] = df_co.groupby('date')['政策性金融债-新债'].sum().sum()
        
        plt.style.use({'font.size' : 10})     
        fig, ax = plt.subplots(nrows=1,ncols=1,\
        figsize=(4.15,1.42), dpi=300)

        sns.heatmap(np.sign(stat.astype(int)).T,cmap="OrRd",linewidths=1,ax=ax,\
            cbar=False,square=False)
        plt.xticks(rotation = 0)
        # ax.legend(['1','2',],loc=3,)
    
    def fig_net_data_2(self,start,end):
        df_net_week = do.get_data('Net_buy_bond',start,end)

        df_net_week.loc[df_net_week['期限'] == '1年及1年以下' , '期限备注'] = '短债'
        df_net_week.loc[(df_net_week['期限'] == '1-3年') , '期限备注'] = '中债'
        df_net_week.loc[(df_net_week['期限'] == '5-7年')|(df_net_week['期限'] == '7-10年')|(df_net_week['期限'] == '10-15年')|(df_net_week['期限'] == '15-20年')
           |(df_net_week['期限'] == '20-30年')|(df_net_week['期限'] == '30年以上') , '期限备注'] = '长债'
        df_net_week.loc[(df_net_week['期限'] == '3-5年') , '期限备注'] = '中长债'
        
        co_list = ['农村金融机构', '证券公司','保险公司', '基金公司及产品','外资银行']
        stat = pd.DataFrame([],columns = co_list,index = ['短债', '中债','中长债','长债'])#,'7-10年\n国债新债', '7-10年\n政金债新债'])
        for co in co_list:
            df_co = df_net_week[df_net_week['机构名称'] == co]
            stat[co] = df_co.groupby(['期限备注'])['合计'].sum()

            df_co = df_net_week[(df_net_week['机构名称'] == co)&(df_net_week['期限'] == '7-10年')]
            stat.loc['7-10年\n国债新债',co] = df_co.groupby('date')['国债-新债'].sum().sum()
            stat.loc['7-10年\n政金债新债',co] = df_co.groupby('date')['政策性金融债-新债'].sum().sum()
        
        tmp = np.sign(stat.astype(int))

        # fig1
        plt.style.use({'font.size' : 10})     
        fig1, ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
        for idx in tmp.index[:4]:
            for co in co_list:
                if tmp.loc[idx,co] == 1:
                    ax.scatter (co,idx, marker='+',s=50,c='red',)
                else:
                    ax.scatter (co,idx, marker='_',s=50,c='green',)
        ax.legend(['净买入','净卖出'],\
            ncol=2,loc=3, bbox_to_anchor=(0.15,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
        ax.set_xticklabels(['农村金融机构', '证券公司','保险公司', '基金公司','外资银行'])
        ax.set_title('分机构久期分布',fontsize=12)
        plt.ylim(-1,4)
        self.pic_list.append(fig1)
        self.title_list.append('分机构久期分布(不标注金额)')
        
        
        tmp.columns = ['农村金融机构', '证券公司','保险公司', '基金公司','外资银行']

        # fig2
        plt.style.use({'font.size' : 10})     
        fig2, ax = plt.subplots(figsize=(4.15,1.42), dpi=300)
        # ax.set_xticklabels(['农村金融机构', '证券公司','保险公司', '基金公司','外资银行'])

        x1,x2,y1,y2 = [],[],[],[]
        for idx in tmp.index[-2:]:
            for co in ['农村金融机构', '证券公司','保险公司', '基金公司','外资银行']:
                if tmp.loc[idx,co] == 1:
                    x1.append(co)
                    y1.append(idx)
                    # ax.scatter (co,idx, marker='+',s=50,c='red',label='净买入')
                else:
                    x2.append(co)
                    y2.append(idx)
                    # ax.scatter (co,idx, marker='_',s=50,c='green',)
        ax.scatter (x1,y1, marker='+',s=50,c='red',label='净买入')
        ax.scatter (x2,y2, marker='_',s=50,c='green',label='净卖出')

        ax.legend(
            ncol=2,loc=3, bbox_to_anchor=(0.15,-0.5),borderaxespad = 0.,fontsize=10,frameon=False)
        plt.ylim(-1,2)
        # ax.set_xticklabels(['农村金融机构', '证券公司','保险公司', '基金公司','外资银行'])
        ax.set_title('分机构7-10年政金新债、国债新债净买入情况',fontsize=12)
        self.pic_list.append(fig2)
        self.title_list.append('分机构7-10年政金新债、国债新债周度净买入情况(不标注金额)')
        
        return [fig1,fig2]


class MacroReport:

    def __init__(self, years = 1):
        self.end = dt.datetime.today()
        self.start=dt.datetime.now()-dt.timedelta(days=years*365)
        self.pic_list=[]
        self.title="经济数据高频跟踪周报"+self.end.strftime("%Y-%m-%d")

    def print_all_fig(self):
        n = len(self.pic_list)
        pdf = PdfPages(self.title+'.pdf')
        for pic in self.pic_list:
            pdf.savefig(pic,bbox_inches='tight')
            plt.close
        pdf.close()
        print("成功打印"+str(n)+"张图片,保存为\n" , os.getcwd() +'/'+self.title + '.pdf')

    def fig_all(self):
        '''画出所有图'''
        self.fig_industrial_production()
        self.fig_cpi_ppi_related()
        self.fig_upstream()
        self.fig_midstream()
        self.fig_downstream()

    def fig_industrial_production(self):
        # * 工业生产

        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")
        # 提取数据
        data = do.get_data('fig_industrial_production',start , end)
        # data = pd.read_sql("select * from fig_industrial_production  \
        # where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date
        
        # 绘图 _V2
        ## PTA产业负荷率/玻璃产能利用率/全国高炉开工率
        fig, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        ## p1 PTA产业负荷率
        data[['PTA产业链负荷率:PTA工厂']].dropna(axis = 0).plot(ax = ax[0,0])
        ax[0,0].set_title('PTA产业负荷率')
        ## p2 玻璃产能利用率
        data[['浮法玻璃:产能利用率']].dropna(axis = 0).plot(ax = ax[0,1])
        ax[0,1].set_title('玻璃产能利用率')
        ## p3 全国高炉开工率
        data[['高炉开工率(163家):全国']].dropna(axis = 0).plot(ax = ax[1,0])
        ax[1,0].set_title('全国高炉开工率')
        #ax[1,0].legend(loc = 'best')
        ## 删除第四张
        fig.delaxes(ax[1,1])

        '''        
        # 绘图 _V1
        fig, ax = plt.subplots(nrows=1,ncols=3,figsize = (18,4), dpi=100)
        ## p1
        data[['日均产量：粗钢：国内']].dropna(axis = 0).plot(ax = ax[0])
        ax[0].legend(loc='upper left')
        ax_right = ax[0].twinx()
        data[['日均产量：焦炭：重点企业(旬)']].dropna(axis = 0).plot(ax = ax_right, color = 'red')
        ax[1].legend(loc='upper right')
        ## p2
        data[['高炉开工率(163家):全国']].dropna(axis = 0).plot(ax = ax[1])
        ax[1].legend(loc = 'best')
        ## p3
        data[['产能利用率:电炉:全国']].dropna(axis = 0).plot(ax = ax[2])
        ax[2].legend(loc = 'best')
        '''
        for i in range(ax.shape[0]):
            for j in range(ax.shape[1]):
                ax[i,j].set_xlabel('')
        plt.suptitle("工业生产",fontsize=30)
        plt.tight_layout()
        self.pic_list.append(fig)
        return data

    def fig_cpi_ppi_related(self):
        # * 物价（CPI/PPI相关）

        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = do.get_data('fig_cpi_ppi_related', start , end)
        # data = pd.read_sql("select * from fig_cpi_ppi_related  \
        # where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图 -v2
        ##  农产品批发价格指数/ /iCPI
        fig, ax = plt.subplots(nrows=3,ncols=2,figsize = (12,12), dpi=100)

        ## p1
        ax[0,0].plot(data[["农产品批发价格200指数"]],color='C0')
        # ax[0,0].set_xticklabels(labels=data.date,rotation=30)
        data[["农产品批发价格200指数"]].dropna(axis = 0).plot(ax = ax[0,0],fontsize=10)
        # ax[0,0].plot(data[['农产品批发价格200指数']].dropna(axis = 0))
        ax[0,0].set_title('农产品批发价格指数')
        # ax[0,0].set_xticklabels(data.index,rotation=30)
        ## p2
        data[['平均批发价:28种重点监测蔬菜']].dropna(axis=0).plot(ax=ax[0][1])
        ax01_ = ax[0][1].twinx()
        data[['平均批发价:7种重点监测水果']].dropna(axis=0).plot(ax=ax01_,color='red')
        ax01_.legend(loc='upper right')
        ax[0][1].set_title('重点监测蔬菜和水果平均批发价')
        ## p3
        data[['iCPI:总指数:日环比']].dropna(axis = 0).plot(ax = ax[1,0])
        ax[1,0].set_title('iCPI')
        ## p4
        fig.delaxes(ax[1,1])
        ## p5
        data[['南华综合指数']].dropna(axis=0).plot(ax=ax[2,0])
        ax[2,0].set_title('南华综合指数')
        ## p6
        data[['CRB现货指数:综合']].dropna(axis=0).plot(ax=ax[2,1])
        ax[2,1].set_title('CRB现货指数')

        for i in range(ax.shape[0]):
            for j in range(ax.shape[1]):
                ax[i,j].set_xlabel('')
        plt.suptitle('物价（CPI/PPI相关）',fontsize=30)
        plt.tight_layout()
        """
        # 画图 -v1
        ## fig1 
        fig1, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        data[['食用农产品价格指数:蛋类:周环比','食用农产品价格指数:蔬菜类:周环比', 
        '食用农产品价格指数:禽类:周环比']].dropna(axis=0).plot(ax=ax[0][0])
        ax00_ = ax[0][0].twinx()
        data[['食用农产品价格指数']].dropna(axis=0).plot(ax=ax00_)
        ax00_.legend(loc='best')
        #ax[0][0].set_title('食用农产品价格指数')

        data[['平均批发价:28种重点监测蔬菜']].dropna(axis=0).plot(ax=ax[0][1])
        ax01_ = ax[0][1].twinx()
        data[['平均批发价:7种重点监测水果']].dropna(axis=0).plot(ax=ax01_,color='red')
        ax01_.legend(loc='upper right')
        ax[0][1].set_title('重点监测蔬菜和水果平均批发价')

        data[['平均价:猪肉:全国']].dropna(axis=0).plot(ax=ax[1][0])

        data[['中国大宗商品价格指数:总指数']].dropna(axis=0).plot(ax=ax[1][1])

        plt.tight_layout()
        self.pic_list.append(fig1)
        ## fig2
        fig2, ax = plt.subplots(nrows=1,ncols=2,figsize = (12,4), dpi=100)
        data[['南华综合指数']].dropna(axis=0).plot(ax=ax[0])
        ax[0].set_title('南华综合指数')
        data[['CRB现货指数:综合']].dropna(axis=0).plot(ax=ax[1])
        ax[1].set_title('CRB现货指数')

        """
        
        self.pic_list.append(fig)
        return data

    def fig_upstream(self):
        # * 上游
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = do.get_data('fig_upstream')
        # data = pd.read_sql("select * from fig_upstream  \
        # where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图 -v2
        fig, ax = plt.subplots(nrows=5,ncols=2,figsize = (12,20), dpi=100)
        ## p1
        data[['南华焦炭指数']].dropna(axis=0).plot(ax=ax[0,0])
        ax[0,0].set_title('南华焦炭指数')
        ## p2
        data[['炼焦煤库存:六港口合计']].dropna(axis=0).plot(ax=ax[0,1])
        ax[0,1].set_title('炼焦煤库存')
        ## p3
        data[['Mylpic矿价指数:综合']].dropna(axis=0).plot(ax=ax[1,0])   
        ax[1,0].set_title('铁矿石价格')
        ## p4
        data[['国内铁矿石港口库存量']].dropna(axis=0).plot(ax=ax[1,1])
        ax[1,1].set_title('铁矿石库存')
        ## p5
        data[['现货价:原油:英国布伦特Dtd','现货价:原油:美国西德克萨斯中级轻质原油(WTI)']].\
            dropna(axis=0).plot(ax=ax[2,0])
        ax[2,0].set_title('石油价格')
        ## p6
        data[['伦敦现货白银:以美元计价']].dropna(axis=0).plot(ax=ax[2,1])
        ax21_=ax[2,1].twinx()
        data[['伦敦现货黄金:以美元计价']].dropna(axis=0).plot(ax=ax21_,color = 'red')
        ax[2,1].set_title('黄金和白银现货价格')
        ## p7
        data[['期货收盘价(活跃合约):阴极铜']].dropna(axis=0).plot(ax=ax[3,0])
        ax30_ = ax[3,0].twinx()
        data[['期货收盘价(活跃合约):铝']].dropna(axis=0).plot(ax=ax30_,color='red')
        ax30_.legend(loc = 'lower right')
        ax[3,0].set_title('有色金属期货收盘价')
        ## p8
        data[['库存期货:阴极铜','库存期货:铝']].dropna(axis=0).plot(ax=ax[3,1])
        ax[3,1].set_title('铜与铝库存')
        ## p9
        data[['综合平均价格指数:环渤海动力煤']].dropna(axis=0).plot(ax=ax[4,0])
        ax[4,0].set_title('铜保税区库存')
        ## p10
        fig.delaxes(ax[4,1])
        for i in range(ax.shape[0]):
            for j in range(ax.shape[1]):
                ax[i,j].set_xlabel('')
        plt.suptitle('上游',fontsize=30)
        plt.tight_layout()
        self.pic_list.append(fig)
        return data

    def fig_midstream(self):
        # * 中游
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = do.get_data('fig_midstream')
        # data = pd.read_sql("select * from fig_midstream  \
        # where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图
        fig, ax = plt.subplots(nrows=3,ncols=2,figsize = (12,12), dpi=100)
        ## P1
        data[['Mylpic综合钢价指数']].dropna(axis=0).plot(ax=ax[0][0])
        ax[0,0].set_title('钢铁价格')
        ## P2
        data[['库存:主要钢材品种:合计','库存:螺纹钢(含上海全部仓库)']].\
            dropna(axis=0).plot(ax=ax[0,1])
        ax[0,1].set_title('钢铁库存')
        ## P3
        data[['水泥价格指数:全国']].dropna(axis=0).plot(ax=ax[1][0])
        ax10_ = ax[1][0].twinx()
        data[['中国玻璃价格指数']].dropna(axis=0).plot(ax=ax10_,color='red')
        ax10_.legend(loc = 'lower right')
        ax[1,0].set_title('水泥和玻璃价格指数')
        ## P4
        fig.delaxes(ax[1,1])
        ## P5
        data[['中国盛泽化纤价格指数']].dropna(axis=0).plot(ax=ax[2,0])
        ax[2,0].set_title('化纤价格')
        ## P6
        data[['期货收盘价(活跃合约):黄大豆1号']].dropna(axis = 0).plot(ax=ax[2,1])
        ax21_ = ax[2,1].twinx()
        data[['期货收盘价(活跃合约):黄玉米']].dropna(axis = 0).plot(ax=ax21_,color='red')
        ax[2,1].set_title('农产品价格')
        ax[2,1].legend(loc = 'lower right')

        # data[['期货收盘价(活跃合约):PVC','期货收盘价(活跃合约):天然橡胶']].\
        #     dropna(axis=0).plot(ax = ax)

        for i in range(ax.shape[0]):
            for j in range(ax.shape[1]):
                ax[i,j].set_xlabel('')
        plt.suptitle('中游',fontsize=30)
        plt.tight_layout()
        self.pic_list.append(fig)
        return data

    def fig_downstream(self):
        # * 下游
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = do.get_data('fig_downstream', start , end )
        # data = pd.read_sql("select * from fig_downstream  \
        # where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date
        # data = data[data.columns[:2]]
        # data.columns = ['30大中城市:商品房成交套数', '大中城市:商品房成交面积']
        # 画图
        fig, ax = plt.subplots(nrows=6,ncols=2,figsize = (12,24), dpi=100)
        ## P1
        # data[['30大中城市:商品房成交面积','date']].dropna(axis=0).plot(ax=ax[0][0])
        ax[0,0].plot(data[['30大中城市:商品房成交面积']],color ='C0')
        ax[0,0].set_title('商品房成交面积')
        ## P2[['100大中城市:成交土地溢价率:当周值']]
        # data[['30大中城市:商品房成交面积']].dropna(axis=0).plot(ax=ax[0][1])
        ax[0,1].plot(data[['100大中城市:成交土地溢价率:当周值']].dropna(),color ='C0')
        ax[0,1].set_title('房地产成交土地溢价率')
        ## P3
        #['当周日均销量:乘用车:厂家零售']]
        data[['当周日均销量:乘用车:厂家零售']].dropna(axis=0).plot(ax=ax[1][0])
        ax[1,0].set_title('汽车销售')
        ## P4
        fig.delaxes(ax[1,1])
        ## P5
        data[['柯桥纺织:价格指数:总类']].dropna(axis=0).plot(ax=ax[2,0])
        ax[2,0].set_title('纺织服装价格')
        ## P6
        data[['义乌中国小商品指数:总价格指数']].dropna(axis=0).plot(ax=ax[2,1])
        ax[2,1].set_title('商贸批发零售')
        ## P7
        data[['电影票房收入']].dropna(axis=0).plot(ax=ax[3,0])
        # ax30_ = ax[3,0].twinx()
        # data[['电影观影人次']].dropna(axis=0).plot(ax=ax30_,color='red')
        # ax30_.set_yticks(range(0,14000,2000))
        ax[3,0].set_title('电影票房收入和观影人次')
        ## P8
        fig.delaxes(ax[3,1])
        ## P9
        data[['中国公路物流运价指数']].dropna(axis=0).plot(ax=ax[4,0])
        ax[4,0].set_title('中国公路物流运价指数')
        ## P10
        data[['波罗的海干散货指数(BDI)']].dropna(axis=0).plot(ax=ax[4,1])
        ax[4,1].set_title('波罗的海干散货指数')
        ## P10
        data[['CCFI:综合指数']].dropna(axis=0).plot(ax=ax[5,0])
        ax[5,0].set_title('中国出口集装箱运价指数')
        ## P10
        data[['CICFI:综合指数']].dropna(axis=0).plot(ax=ax[5,1])
        ax[5,1].set_title('中国进口集装箱运价指数')

        for i in range(ax.shape[0]):
            for j in range(ax.shape[1]):
                ax[i,j].set_xlabel('')
        plt.suptitle('下游',fontsize=30)
        plt.tight_layout()
        self.pic_list.append(fig)

        return data
## 报告框架    
class Report:
    
    def __init__(self, years=10):
        self.end = dt.datetime.today()
        self.start=dt.datetime.now()-dt.timedelta(days=years*365)
        self.show_start=dt.datetime.now()-dt.timedelta(days=1*365)
        self.pic_list=[]
        self.title="周报"+self.end.strftime("%Y-%m-%d")
    
    def print_all_fig(self):
        n=len(self.pic_list)
        pdf=PdfPages(self.title+'.pdf') 
        for pic in self.pic_list:
            pdf.savefig(pic,bbox_inches='tight')
            plt.close
        pdf.close()
        print("成功打印"+str(n)+"张图片,保存为\n" , os.getcwd() +'/'+self.title + '.pdf')

    def pic_SRDI(self,window=14):
        # TODO
        start=self.start.strftime("%Y%m%d")
        end=self.end.strftime("%Y%m%d")
        
        ## 读取数据
        df = pd.read_sql("select * from fig_SRDI  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        print('SRDI的数据更新至' , df.iloc[-1,-1])
        df.index = df.date

        ## 处理数据
        df['成交总量'] = df.iloc[:,:-1].apply(lambda x: x.sum(), axis=1) #跳过date列
        df["R014+_成交总量"]=df[['成交量:R014', '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
                            '成交量:R4M', '成交量:R6M', '成交量:R9M']].apply(lambda x: x.sum(), axis=1)
        dff=df[['成交量:R001', '成交量:R007', "R014+_成交总量"]].div(df["成交总量"],axis=0)
        dff.columns=['成交量占比:R001', '成交量占比:R007', "R014+_成交总量占比"]
        ## 处理短期回购扩散指数
        dff["负债短期化_因子"]=(dff["成交量占比:R001"].diff(1)-dff["成交量占比:R007"].diff(1)-dff["R014+_成交总量占比"].diff(1))
        dff["加权利率_R001"]=df["加权利率:R001"]
        ## 去掉极值
        dff["负债短期化_因子_去极值"]=winsorize_series(dff["负债短期化_因子"]).tolist()
        dff["负债短期化_因子_去极值Zscore"]=std_series(dff["负债短期化_因子_去极值"]).tolist()
        dff["SRDI"]=dff["负债短期化_因子_去极值Zscore"]
        factor_df=dff
        ## 绘制因子图像
        fig, ax = plt.subplots(nrows=2,ncols=1,figsize = (10,6), dpi=100)
        factor_df[['成交量占比:R001', '成交量占比:R007', "R014+_成交总量占比"]].plot(ax=ax[0],xlabel=" ",ylim=(0,1),ylabel="融资占比")
        factor_df[["SRDI"]].rolling(window).mean().plot(ax=ax[1])
        plt.ylabel("SRDI因子")
        plt.xlabel(" ")
        plt.suptitle("SRDI扩散因子"+end)
        ## 添加图片
        self.pic_list.append(fig)
        print("添加图片成功")

    def fig_liquidity_premium(self):
        start=self.start.strftime("%Y-%m-%d")
        end=self.end.strftime("%Y-%m-%d")

        ## 读取源数据
        data = pd.read_sql("select * from fig_liquidity_premium  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        print('流动性溢价的数据更新至' , data.iloc[-1,-1])
        
        data.index = data.date
        ## 基本数据图
        fig, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        data[["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天","IRS：FR007：1y"]]["2020":].plot(ax=ax[0],title="短期流动性"+end)
        # 非银流动性溢价
        data["非银流动性溢价"]=winsorize_series(data["质押回购利率_7天"]-data["存款类质押回购利率_7天"])
        data["非银流动性溢价"].rolling(30).mean().plot(ax=ax[1])
        ax[1].set_ylabel("非银流动性溢价")
        std_series(data["非银流动性溢价"]).rolling(14).mean().plot(ax=ax[2],ylim=(-3,3))
        ax[2].set_ylabel("非银流动性溢价因子")
        plt.tight_layout()
        self.pic_list.append(fig)
        print("添加图片成功")
        ## 中期流动性溢价
        fig2, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        data[["存单_AAA_3m","shibor_3m","存单_AAA_1y","MLF：1年"]]["2020":].plot(ax=ax[0],
        title="中期流动性"+end)
        data["中期流动性溢价"]=100*(data["存单_AAA_1y"]-data["MLF：1年"])
        data["中期流动性溢价"].rolling(30).mean().plot(ax=ax[1])
        ax[1].set_ylabel("中期流动溢价_银行负债")
        std_series(data["中期流动性溢价"]).rolling(14).mean().plot(ax=ax[2],ylim=(-2,2))
        ax[2].set_ylabel("中期流动溢价因子")
        plt.tight_layout()
        self.pic_list.append(fig2)
        print("添加图片成功")
        
        
        ## 流动性波动率
        fig3, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        data[["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天"]].rolling(30).mean().plot(ax=ax[0])
        ax[0].set_title("短期流动性")
        # 
        data_repo_volatility=data[["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天"]].rolling(30).std()
        data_repo_volatility.columns=["Shibor_7d","R007","DR007"]
        dataa_repo_volatility=data_repo_volatility.apply(winsorize_series)
        dataa_repo_volatility.plot(ax=ax[1])
        ax[1].set_ylabel("回购波动率")
        data_repo_volatility_std=dataa_repo_volatility.apply(std_series)
        data_repo_volatility_std.plot(ax=ax[2],ylim=(-3,3))
        ax[2].set_ylabel("回购波动率率因子")
        plt.axhline(y=0, c="r", ls="--", lw=1.5)
        plt.tight_layout()
        self.pic_list.append(fig3)
        print("添加图片成功")
        return data_repo_volatility
      
    def fig_bond_leverage(self):
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y-%m-%d")
        # 获取数据
        df = pd.read_sql("select * from fig_bond_leverage  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        print('杠杆率的数据更新至' , df.iloc[-1,-1])
        df.index = df.date
        df = df.fillna(method = 'ffill')
        ## 制作图片 
        df["杠杆率"]=winsorize_series(df["成交量:银行间质押式回购"]/(df["债券市场托管余额"])*100)
        fig, ax = plt.subplots(nrows=2,ncols=1,figsize = (10,6), dpi=100)
        # p1
        df["杠杆率"].rolling(30).mean().plot(ax=ax[0],title="债市整体杠杆率"+end)
        ax[0].grid(ls='--', axis='y')
        # plt.rc('axes', axisbelow=True)
        ax[0].set_xlabel("")
        # P2
        std_series(df["杠杆率"].rolling(6).mean()).plot(ax=ax[1],ylim=(-3,3))
        ax[1].axhline(y=0, c="r", ls="--", lw=1.5)
        ax[1].set_xlabel("")
        ax[1].set_ylabel("杠杆拥挤度因子")
        plt.tight_layout()
        self.pic_list.append(fig)
        return df
    
    def fig_rates(self):
        start=self.start.strftime("%Y%m%d")
        end=self.end.strftime("%Y%m%d")
        df = pd.read_sql("select * from fig_rates  \
        where date >= '{}' and date <= '{}';".format(start , end), conn)
        print('期限利差的数据更新至' , df.iloc[-1,-1])
        df.index = df.date
        
        
        fig, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        ## 期限利差
        dff=pd.DataFrame()
        dff["国债_10年-5年"]=df["10年国债"]-df["5年国债"]
        dff["国债_10年-1年"]=df["10年国债"]-df["1年国债"]
        dff["国债_3年-1年"]=df["5年国债"]-df["1年国债"]
        dff=dff.apply(winsorize_series)*100
        dff.plot(ax=ax[0],xlabel=" ")
        dff.apply(std_series).plot(ax=ax[1],ylim=(-2,2))
        ax[1].axhline(y=0.0, c="r", ls="--", lw=1.5)
        ax[1].set_ylabel("期限利差Z-Score")
        ax[1].set_xlabel(" ")
        (dff.apply(MaxMinNormal)*100).plot(ax=ax[2])
        ax[2].set_ylabel("期限利差分位数")
        ax[2].set_xlabel(" ")
        plt.suptitle("国债_期限利差"+str(end))
        plt.tight_layout()
        self.pic_list.append(fig)
        ## 国开期限利差
        fig_gk, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        ## 期限利差
        dff=pd.DataFrame()
        dff["国开_10年-5年"]=df["10年国开"]-df["5年国开"]
        dff["国开_10年-1年"]=df["10年国开"]-df["1年国开"]
        dff["国开_3年-1年"]=df["5年国开"]-df["1年国开"]
        dff=dff.apply(winsorize_series)*100
        dff.plot(ax=ax[0],xlabel=" ")
        dff.apply(std_series).plot(ax=ax[1],ylim=(-2,2))
        ax[1].axhline(y=0.0, c="r", ls="--", lw=1.5)
        ax[1].set_ylabel("期限利差Z-Score")
        ax[1].set_xlabel(" ")
        (dff.apply(MaxMinNormal)*100).plot(ax=ax[2])
        ax[2].set_ylabel("期限利差分位数")
        ax[2].set_xlabel(" ")
        plt.suptitle("国开_期限利差"+str(end))
        plt.tight_layout()
        self.pic_list.append(fig_gk)
        
        fig2, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        ## 税收利差
        dff=pd.DataFrame()
        dff["税收溢价_10y"]=df["10年国开"]-df["10年国债"]
        dff["税收溢价_5y"]=df["5年国开"]-df["5年国债"]
        dff["税收溢价_1年"]=df["1年国开"]-df["1年国债"]
        dff=dff.apply(winsorize_series)*100
        dff.plot(ax=ax[0])
        dff.apply(std_series).plot(ax=ax[1],ylim=(-3,3))
        ax[1].axhline(y=0, c="r", ls="--", lw=1.5)
        ax[1].set_ylabel("税收利差Z-Score")
        ax[1].set_xlabel(" ")
        (dff.apply(MaxMinNormal)*100).plot(ax=ax[2])
        ax[2].set_ylabel("税收利差分位数")
        ax[2].set_xlabel(" ")
        plt.suptitle("税收利差跟踪"+str(end))
        plt.tight_layout()
        self.pic_list.append(fig2)
    
        fig3, ax = plt.subplots(nrows=2,ncols=2,figsize = (10,6), dpi=100)
        ## 波动率
        df[["1年国债","3年国债","5年国债","10年国债"]].plot(ax=ax[0,0],ylabel="yield",xlabel=" ")
        df[["1年国债","3年国债","5年国债","10年国债"]].apply(volatility_series).plot(ax=ax[1,0],ylabel="volatility",xlabel=" ")
        df[["1年国开","3年国开","5年国开","10年国开"]].plot(ax=ax[0,1],xlabel=" ")
        df[["1年国开","3年国开","5年国开","10年国开"]].apply(volatility_series).plot(ax=ax[1,1],xlabel=" ")
        plt.suptitle("利率波动率跟踪"+str(end))
        plt.tight_layout()
        self.pic_list.append(fig3)
        
        return df
    
    def fig_credit_premium(self):
        # 信用利差的数据
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")
        #经济数据库(EDB)-利率走势数据-中债商业银行二级资本债到期收益率（AAA-）:3年;中债中短期票据到期收益率(AAA):3年;中债国开债到期收益率:3年-iFinD数据接口
        # 提取数据
        data = pd.read_sql("select * from fig_credit_premium  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        print('信用利差的数据更新至' , data.iloc[-1,-1])
        data.index = data.date

        # 绘图
        fig, ax = plt.subplots(nrows=3,ncols=1,figsize = (10,9), dpi=100)
        data_bond_perpetual=pd.DataFrame()
        data_bond_perpetual["AAA永续债信用利差_3y"]=data["中债可续期产业债到期收益率(AAA):3年"]-data["中债国开债到期收益率:3年"]
        data_bond_perpetual["AAA银行二级资本债信用利差_3y"]=data["中债商业银行二级资本债到期收益率(AAA-):3年"]-data["中债国开债到期收益率:3年"]
        data_bond_perpetual=data_bond_perpetual*100
        data_bond_perpetual.dropna().plot(ax=ax[0])
        ## 城投
        bond_chengtou_premium=pd.DataFrame()
        bond_chengtou_premium["AAA城投信用利差_3y"]=data["中债城投债到期收益率(AAA):3年"]-data["中债国开债到期收益率:3年"]
        bond_chengtou_premium["AA+城投信用利差_3y"]=data["中债城投债到期收益率(AA+):3年"]-data["中债国开债到期收益率:3年"]
        bond_chengtou_premium=bond_chengtou_premium*100
        bond_chengtou_premium.plot(ax=ax[1],ylabel="信用溢价分位数")
        bond_chengtou_premium.apply(std_series).plot(ax=ax[2],ylim=(-3,3),ylabel="信用溢价Z-score")
        ax[2].axhline(y=0, c="r", ls="--", lw=1.5)
        plt.suptitle("信用溢价"+end)
        self.pic_list.append(fig)
            
        return data_bond_perpetual
  
    def fig_bond_premium(self):
        # * 1/3/5/10Y 国债到期收益率走势与利差
        # 近十年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        df = pd.read_sql("select * from fig_rates  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        df.index = df.date

        dff=df[['10年国债','5年国债','3年国债','1年国债']].dropna(axis=0)
        dff["国债_10年-5年"]=df["10年国债"]-df["5年国债"]
        dff["国债_10年-1年"]=df["10年国债"]-df["1年国债"]
        dff["国债_10年-3年"]=df["10年国债"]-df["3年国债"]
        # 去极值
        # dff = dff.apply(winsorize_series)
        ## P1 1/3/5/10Y 国债到期收益率ZS
        fig, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        dff[['1年国债',"国债_10年-1年"]].apply(std_series).plot(ax=ax[0][0])
        dff[['3年国债',"国债_10年-3年"]].apply(std_series).plot(ax=ax[0][1])
        dff[['5年国债',"国债_10年-5年"]].apply(std_series).plot(ax=ax[1][0])
        dff[['10年国债']].apply(std_series).plot(ax=ax[1][1])

        plt.suptitle('Z-Score')
        plt.tight_layout()
        self.pic_list.append(fig)
    
        return dff

    def fig_industries_premium(self):
        # TODO 行业情绪指数
        # 地产钢铁煤炭有色汽车
        # 近十年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        df = do.get_data('fig_industries_premium')
        df.index = df.date

        # 绘图 
        fig, ax = plt.subplots(nrows=3,ncols=2,figsize = (20,9), dpi=100)
        ## 地产
        df[['信用利差_地产']].apply(winsorize_series).apply(std_series).plot(ax=ax[0,0])
        ax[0,0].grid(ls='--', axis='y')
        ax[0,0].set_axisbelow(True)
        ax[0,0].set_title('地产情绪指数')
        ## 钢铁
        df[['信用利差_钢铁']].apply(winsorize_series).apply(std_series).plot(ax=ax[0,1])
        ax[0,1].grid(ls='--', axis='y')
        ax[0,1].set_axisbelow(True)
        ax[0,1].set_title('钢铁情绪指数')        
        ## 煤炭
        df[['信用利差_煤炭']].apply(winsorize_series).apply(std_series).plot(ax=ax[1,0])
        ax[1,0].grid(ls='--', axis='y')
        ax[1,0].set_axisbelow(True)
        ax[1,0].set_title('煤炭情绪指数')
        ## 有色
        df[['信用利差_有色']].apply(winsorize_series).apply(std_series).plot(ax=ax[1,1])
        ax[1,1].grid(ls='--', axis='y')
        ax[1,1].set_axisbelow(True)
        ax[1,1].set_title('有色情绪指数')
        ## 汽车
        df[['信用利差_汽车']].apply(winsorize_series).apply(std_series).plot(ax=ax[2,0])
        ax[2,0].grid(ls='--', axis='y')
        ax[2,0].set_axisbelow(True)
        ax[2,0].set_title('汽车情绪指数')

        fig.delaxes(ax[2,1])
        fig.suptitle('行业利差')
        fig.tight_layout()
        self.pic_list.append(fig)
        return 

    def fig_credit_premium_v2(self):
        # * 城投等
        # 近十年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        df = pd.read_sql("select * from fig_credit_premium  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        df_rate = pd.read_sql("select * from fig_rates  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)

        df.index = df.date; df_rate.index = df_rate.date
        df = pd.merge(df,df_rate,how='inner',left_index=True,right_index=True)


        dff = pd.DataFrame(index = df.index)
        dff['二级资本债_AAA-_1Y利差'] = df['中债商业银行二级资本债到期收益率(AAA-):1年']-df['1年国开']
        dff['二级资本债_AAA-_3Y利差'] = df['中债商业银行二级资本债到期收益率(AAA-):3年']-df['3年国开']
        dff['二级资本债_AAA-_5Y利差'] = df['中债商业银行二级资本债到期收益率(AAA-):5年']-df['5年国开']
        
        dff['城投_AAA_1Y利差'] = df['中债城投债到期收益率(AAA):1年']-df['1年国开']
        dff['城投_AAA_3Y利差'] = df['中债城投债到期收益率(AAA):3年']-df['3年国开']
        dff['城投_AAA_5Y利差'] = df['中债城投债到期收益率(AAA):5年']-df['5年国开']
        dff['城投_AA+_1Y利差'] = df['中债城投债到期收益率(AA+):1年']-df['1年国开']
        dff['城投_AA+_3Y利差'] = df['中债城投债到期收益率(AA+):3年']-df['3年国开']
        dff['城投_AA+_5Y利差'] = df['中债城投债到期收益率(AA+):5年']-df['5年国开']
        dff['城投_AA_1Y利差'] = df['中债城投债到期收益率(AA):1年']-df['1年国开']
        dff['城投_AA_3Y利差'] = df['中债城投债到期收益率(AA):3年']-df['3年国开']
        dff['城投_AA_5Y利差'] = df['中债城投债到期收益率(AA):5年']-df['5年国开']

        # 绘图 
        fig, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        ## AAA二级资本债
        dff[['二级资本债_AAA-_1Y利差', '二级资本债_AAA-_3Y利差', '二级资本债_AAA-_5Y利差']] \
            .apply(std_series).plot(ax=ax[0,0])
        ## AAA城投
        dff[['城投_AAA_1Y利差','城投_AAA_3Y利差', '城投_AAA_5Y利差']].\
        apply(std_series).plot(ax=ax[0,1])
        ## AA+城投
        dff[['城投_AA+_1Y利差', '城投_AA+_3Y利差', '城投_AA+_5Y利差']] \
        .apply(std_series).plot(ax=ax[1,0])
        ## AA城投
        dff[['城投_AA_1Y利差', '城投_AA_3Y利差', '城投_AA_5Y利差']] \
        .apply(std_series).plot(ax=ax[1,1]) 

        plt.suptitle('利差Z-Score')
        plt.tight_layout()
        self.pic_list.append(fig)

        return dff

    def fig_liquid_v2(self):
        # * 流动性v2
        # 近十年

        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        df_liquidity = pd.read_sql("select * from fig_liquidity_premium  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        df_leverage= pd.read_sql("select * from fig_bond_leverage  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        df_rate = pd.read_sql("select * from fig_rates  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)


        df_liquidity.index = df_liquidity.date
        df_leverage.index = df_leverage.date
        df_rate.index = df_rate.date

        df = pd.merge(df_liquidity,df_leverage,how='inner',left_index=True,right_index=True)
        df = pd.merge(df,df_rate,how='inner',left_index=True,right_index=True)

        # dff = pd.DataFrame(index = df.index)
        df['shibor_3m-10y'] = df['shibor_3m']-df['10年国开']
        df['贴票利率波动率'] = std_series(df['国股银票转贴现收益率_3m'].dropna(axis=0))
        df['同业存单-1年短债利差'] = df['存单_AAA_1y'] - df['MLF：1年']
        df['1Y存单/短债比价'] = df['存单_AAA_1y'] / df['MLF：1年']
        df['回购余额/债券托管余额'] = df['成交量:银行间质押式回购'] / df['债券市场托管余额']

        fig, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        df[['shibor_3m-10y']].apply(std_series).plot(ax=ax[0,0])
        df[['国股银票转贴现收益率_3m','贴票利率波动率']].dropna().plot(ax=ax[0,1])
        df[['同业存单-1年短债利差','1Y存单/短债比价']].plot(ax=ax[1,0])
        df[['回购余额/债券托管余额']].dropna().plot(ax=ax[1,1])

        plt.tight_layout()
        self.pic_list.append(fig)

        return df
        
    def radar_chart(self,date):
        # 制定日期的利差雷达图
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")
        # 城投等
        df1 = pd.read_sql("select * from fig_credit_premium  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        # 行业
        df2 = pd.read_sql("select * from fig_industries_premium  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        df_rate = pd.read_sql("select * from fig_rates  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)

        df1.index = df1.date; df_rate.index = df_rate.date
        df2.index = df2.date

        df11 = pd.merge(df1,df_rate,how='inner',left_index=True,right_index=True)
        df22 = pd.merge(df2,df_rate,how='inner',left_index=True,right_index=True)

        dff = pd.DataFrame(index = df_rate.index)
        dff['二级资本债_AAA-_1Y利差'] = df11['中债商业银行二级资本债到期收益率(AAA-):1年']-df11['1年国开']
        dff['二级资本债_AAA-_3Y利差'] = df11['中债商业银行二级资本债到期收益率(AAA-):3年']-df11['3年国开']
        dff['二级资本债_AAA-_5Y利差'] = df11['中债商业银行二级资本债到期收益率(AAA-):5年']-df11['5年国开']
        
        dff['城投_AAA_1Y利差'] = df11['中债城投债到期收益率(AAA):1年']-df11['1年国开']
        dff['城投_AAA_3Y利差'] = df11['中债城投债到期收益率(AAA):3年']-df11['3年国开']
        dff['城投_AAA_5Y利差'] = df11['中债城投债到期收益率(AAA):5年']-df11['5年国开']
        dff['城投_AA+_1Y利差'] = df11['中债城投债到期收益率(AA+):1年']-df11['1年国开']
        dff['城投_AA+_3Y利差'] = df11['中债城投债到期收益率(AA+):3年']-df11['3年国开']
        dff['城投_AA+_5Y利差'] = df11['中债城投债到期收益率(AA+):5年']-df11['5年国开']
        dff['城投_AA_1Y利差'] = df11['中债城投债到期收益率(AA):1年']-df11['1年国开']
        dff['城投_AA_3Y利差'] = df11['中债城投债到期收益率(AA):3年']-df11['3年国开']
        dff['城投_AA_5Y利差'] = df11['中债城投债到期收益率(AA):5年']-df11['5年国开']

        dff['钢铁利差'] = df22['信用利差_钢铁']
        dff['煤炭利差'] = df22['信用利差_煤炭']        
        dff['有色利差'] = df22['信用利差_有色']
        dff['汽车利差'] = df22['信用利差_汽车']
        dff['地产利差'] = df22['信用利差_地产']
        
        # 去极值以及计算当前标准差
        dff_std = dff.apply(winsorize_series).apply(std_series)

        # 画图
        def Line(line_style, line_color, line_width):
            """
            This function generate a plotly line object
            """
            Line = go.scatterpolar.Line(dash=line_style, color=line_color, width=line_width)
            return Line

        def func_radar(df_std , date):
            import plotly.graph_objects as go
            categories = list(df_std.columns)
            categories.append(df_std.columns[0])

            arr = df_std.loc[date].values
            arr = np.append(arr,arr[0])  

            layout = go.Layout(
                polar={
                    "bgcolor": "rgba(0,0,0,0)",        # set background color
                    "gridshape": "linear",             # set the grid style of the radar 
                    "radialaxis": {
                        "showticklabels": True, 
                        "gridcolor": "black" ,#grid color
                        "dtick": 1,
                    }   
                    ,
                    "angularaxis": {
                        "linecolor": "black",
                        # "linewidth": 2,
                        "gridcolor": "black",
                    },
                },
                plot_bgcolor="rgba(0,0,0,0)",
            )
            fig = go.Figure(layout=layout)

            fig.add_trace(go.Scatterpolar(
                r=arr,
                line = Line('solid','orange',2),
                theta=categories,
                fill='toself',
                name=date+'利差'
            ))

            fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[-2, 2],
                tickangle = 0,
                tickfont_size = 12
                )),
            showlegend=True
            )
            fig.show()
            return fig
        fig = func_radar(dff_std , date)

        self.pic_list.append(fig)
        return dff




