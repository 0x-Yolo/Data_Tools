
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages

from WindPy import w

## test
'''
w.start()
years = 10
end = dt.datetime.today()
start=dt.datetime.now() - dt.timedelta(days=years*365)
start=start.strftime("%Y-%m-%d")
end=end.strftime("%Y-%m-%d")
err, data=w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',start,end,
                  "Fill=Previous",usedf=True) 
data
'''

#基础的图像设置：
plt.style.use({'figure.figsize':(6, 4)})
set_style_A={'grid.linestyle': '--',
     'axes.spines.left': True,
     'axes.spines.bottom': True,
     'axes.spines.right': False,
     'axes.spines.top': False}
sns.set_style("whitegrid")
plt.rcParams['font.family']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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
    
    
## 报告框架    
class Report():
    
    def __init__(self, years=10):
        self.end = dt.datetime.today()
        self.start=dt.datetime.now()-dt.timedelta(days=years*365)
        self.show_start=dt.datetime.now()-dt.timedelta(days=1*365)
        self.pic_list=[]
        self.title="周报"+self.end.strftime("%Y-%m-%d")
        self.pdf = PdfPages(self.title+'.pdf') 
    
    def print_all_fig(self):
        n=len(self.pic_list)
        pdf=self.pdf
        for pic in self.pic_list:
            pdf.savefig(pic)
            plt.close
        pdf.close()
        print("成功打印"+"1"+"张图片,保存为")
            
    def pic_SRDI(self,window=14):
        start=self.start.strftime("%Y%m%d")
        end=self.end.strftime("%Y%m%d")
        
        ## 读取数据
        err, df= w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',start,end,"Fill=Previous",usedf=True) 
        df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014','成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', '成交量:R4M', '成交量:R6M', '成交量:R9M']
        #df=data.pivot_table(index="time",columns="index_name")
        #df.columns=df.columns.droplevel(0).tolist()
        ## 处理数据
        df.fillna(0 , inplace = True)
        df['成交总量'] = df.apply(lambda x: x.sum(), axis=1)
        df["R014+_成交总量"]=df[['成交量:R014', '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
                            '成交量:R4M', '成交量:R6M', '成交量:R9M']].apply(lambda x: x.sum(), axis=1)
        dff=df[['成交量:R001', '成交量:R007', "R014+_成交总量"]].div(df["成交总量"],axis=0)
        dff.columns=['成交量占比:R001', '成交量占比:R007', "R014+_成交总量占比"]
        ## 处理短期回购扩散指数
        dff["负债短期化_因子"]=(dff["成交量占比:R001"].diff(1)-dff["成交量占比:R007"].diff(1)-dff["R014+_成交总量占比"].diff(1))
        dff["加权利率_R001"]=df["加权利率:R001"]
        ## 去掉极值
        dff["负债短期化_因子_去极值"]=winsorize_series(dff["负债短期化_因子"])
        dff["负债短期化_因子_去极值Zscore"]=std_series(dff["负债短期化_因子_去极值"])
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
        err,data=w.edb('M0017139,M0041653,M0220163,M0017142,M0048486,M1010889,M1010892,M0329545', 
                    start,end,"Fill=Previous",usedf=True)
        data.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天","shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年"]
        data.index=pd.to_datetime(data.index)
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
        err, df=w.edb('M0041739,M5639029',start,end,"Fill=Previous",usedf = True)
        #df=data.data.pivot_table(index="time",columns="index_name").fillna(method="ffill").dropna()
        #df.columns=df.columns.droplevel(0).tolist()
        df.columns = ['成交量:银行间质押式回购', '债券市场托管余额']
        # df.index=pd.to_datetime(df.index)

        ## 制作图片 
        df["杠杆率"]=winsorize_series(df["成交量:银行间质押式回购"]/(df["债券市场托管余额"]*100))
        fig, ax = plt.subplots(nrows=2,ncols=1,figsize = (10,6), dpi=100)
        df["杠杆率"].rolling(30).mean().plot(ax=ax[0],title="债市整体杠杆率"+end)
        ax[0].set_xlabel("")
        std_series(df["杠杆率"].rolling(6).mean()).plot(ax=ax[1],ylim=(-3,3))
        ax[1].set_xlabel("")
        ax[1].set_ylabel("杠杆拥挤度因子")
        self.pic_list.append(fig)
        return df
    
    def fig_rates(self):
        start=self.start.strftime("%Y%m%d")
        end=self.end.strftime("%Y%m%d")
        err,df=w.edb('S0059749,S0059747,M1004267,M1004271,S0059744,S0059746,M1004263,M1004265',start,end,"Fill=Previous",usedf=True)
        #df.value=df.value.astype(float)
        '''
        df=df.pivot_table(index=["time"],columns=["id"]).fillna(method="ffill")
        df.index=pd.to_datetime(df.index)
        df=df.reset_index().set_index(["time"])
        df.columns=df.columns.droplevel(0)
        '''
        df.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]
        df.index=pd.to_datetime(df.index)
        
        
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
    
    # 信用利差的数据
    def fig_credit_premium(self):
        end=self.end
        start=self.start
        #经济数据库(EDB)-利率走势数据-中债商业银行二级资本债到期收益率（AAA-）:3年;中债中短期票据到期收益率(AAA):3年;中债国开债到期收益率:3年-iFinD数据接口
        err,data=w.edb("M0048434,M0048424,M1004265,S0059746,M1010706,M1015080,S0059738",start.strftime("%Y%m%d"),end.strftime("%Y%m%d"),"Fill=Previous",usedf=True)
        data.columns=["中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AA+):3年","中债国开债到期收益率:3年","中债国债到期收益率:3年",
                    "中债商业银行二级资本债到期收益率(AAA-):3年","中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
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
        plt.suptitle("信用溢价"+str(end))
        self.pic_list.append(fig)
            
        return data_bond_perpetual

w.start()
report= Report()
report.fig_liquidity_premium()
report.pic_SRDI()
report.fig_bond_leverage()
report.fig_rates()
report.fig_credit_premium()
report.print_all_fig()