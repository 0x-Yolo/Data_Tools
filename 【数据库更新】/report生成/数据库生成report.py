
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
        print("成功打印"+"1"+"张图片,保存为\n" , os.getcwd() + self.title + '.pdf')

    def pic_SRDI(self,window=14):
        start=self.start.strftime("%Y%m%d")
        end=self.end.strftime("%Y%m%d")

        ## 读取数据
        df = pd.read_sql("select * from fig_SRDI  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        print('SRDI的数据更新至' , df.iloc[-1,-1])
        
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
        df = pd.read_sql("select * from fig_rates  \
        where date >= '{}' and date <= '{}';".format(start , end), conn)
        print('期限利差的数据更新至' , df.iloc[-1,-1])
        
        
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

    def fig_industrial_production(self):
        # * 工业生产

        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = pd.read_sql("select * from fig_industrial_production  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date
        # 绘图
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
        # plt.suptitle("工业生产"+end)
        self.pic_list.append(fig)

        return data

    def fig_cpi_ppi_related(self):
        # * 物价（CPI/PPI相关）
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = pd.read_sql("select * from fig_cpi_ppi_related  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图 
        ## P1 
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

        data[['平均价:猪肉:全国']].dropna(axis=0).plot(ax=ax[1][0])

        data[['中国大宗商品价格指数:总指数']].dropna(axis=0).plot(ax=ax[1][1])

        plt.tight_layout()
        self.pic_list.append(fig1)


        ## P2
        fig2, ax = plt.subplots(nrows=1,ncols=2,figsize = (12,4), dpi=100)
        data[['南华综合指数']].dropna(axis=0).plot(ax=ax[0])
        data[['CRB现货指数:综合']].dropna(axis=0).plot(ax=ax[1])
 
        plt.tight_layout()
        self.pic_list.append(fig2)

        return data

    def fig_upstream(self):
        # * 上游
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = pd.read_sql("select * from fig_upstream  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图
        ## P1
        fig1, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        data[['综合平均价格指数:环渤海动力煤']].dropna(axis=0).plot(ax=ax[0][0])
        data[['炼焦煤库存:六港口合计']].dropna(axis=0).plot(ax=ax[0][1])
        data[['现货价:原油:英国布伦特Dtd','现货价:原油:美国西德克萨斯中级轻质原油(WTI)']].\
            dropna(axis=0).plot(ax=ax[1][0])
        data[['Mylpic矿价指数:综合']].dropna(axis=0).plot(ax=ax[1][1])   
        # plt.suptitle('')
        plt.tight_layout()
        self.pic_list.append(fig1)


        ## P2
        fig2, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        data[['国内铁矿石港口库存量']].dropna(axis=0).plot(ax=ax[0][0])
        
        data[['伦敦现货白银:以美元计价']].dropna(axis=0).plot(ax=ax[0][1])
        ax01_=ax[0][1].twinx()
        data[['伦敦现货黄金:以美元计价']].dropna(axis=0).plot(ax=ax01_,color = 'red')
        
        data[['期货收盘价(活跃合约):阴极铜']].dropna(axis=0).plot(ax=ax[1][0])
        ax10_ = ax[1][0].twinx()
        data[['期货收盘价(活跃合约):铝']].dropna(axis=0).plot(ax=ax10_,color='red')
        ax10_.legend(loc = 'lower right')

        data[['库存期货:阴极铜']].dropna(axis=0).plot(ax=ax[1][1])
        ax11_ = ax[1][1].twinx()
        data[['库存期货:铝']].dropna(axis=0).plot(ax=ax11_,color = 'red')

        plt.tight_layout()
        self.pic_list.append(fig2)

        return data

    def fig_midstream(self):
        # * 中游
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = pd.read_sql("select * from fig_midstream  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图
        ## P1
        fig1, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        data[['Mylpic综合钢价指数']].dropna(axis=0).plot(ax=ax[0][0])
        data[['库存:主要钢材品种:合计','库存:螺纹钢(含上海全部仓库)']].\
            dropna(axis=0).plot(ax=ax[0][1])

        data[['水泥价格指数:全国']].dropna(axis=0).plot(ax=ax[1][0])
        ax10_ = ax[1][0].twinx()
        data[['中国玻璃价格指数']].dropna(axis=0).plot(ax=ax10_,color='red')
        ax10_.legend(loc = 'lower right')

        data[['中国盛泽化纤价格指数']].dropna(axis=0).plot(ax=ax[1][1])

        plt.tight_layout()
        self.pic_list.append(fig1)

        ## P2
        fig2, ax = plt.subplots(nrows=1,ncols=1,figsize = (6,4), dpi=100)
        data[['期货收盘价(活跃合约):PVC','期货收盘价(活跃合约):天然橡胶']].\
            dropna(axis=0).plot(ax = ax)
        ax.legend(loc = 'upper left')
        self.pic_list.append(fig2)

        return data

    def fig_downstream(self):
        # * 下游
        # 近一年
        end=self.end.strftime("%Y%m%d")
        start=self.start.strftime("%Y%m%d")

        # 提取数据
        data = pd.read_sql("select * from fig_downstream  \
        where date >= '{}' and date <= '{}';".format(start , end),conn)
        data.index = data.date

        # 画图
        ## P1
        fig1, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        data[['30大中城市:商品房成交套数']].dropna(axis=0).plot(ax=ax[0][0])
        ax00_ = ax[0][0].twinx()
        data[['30大中城市:商品房成交面积']].dropna(axis=0).plot(ax=ax00_,color='red')

        data[['100大中城市:成交土地溢价率:当周值']].dropna(axis=0).plot(ax=ax[0][1])
        data[['当周日均销量:乘用车:厂家零售']].dropna(axis=0).plot(ax=ax[1][0])
        data[['柯桥纺织:价格指数:总类']].dropna(axis=0).plot(ax=ax[1][1])

        plt.tight_layout()
        self.pic_list.append(fig1)

        ## P2
        fig2, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        data[['义乌中国小商品指数:总价格指数']].dropna(axis=0).plot(ax=ax[0][0])
        data[['中关村电子价格产品指数']].dropna(axis=0).plot(ax=ax[0][1])
        data[['中国公路物流运价指数']].dropna(axis=0).plot(ax=ax[1][0])
        
        data[['电影票房收入']].dropna(axis=0).plot(ax=ax[1][1])
        ax11_ = ax[1][1].twinx()
        data[['电影观影人次']].dropna(axis=0).plot(ax=ax11_,color='red')

        plt.tight_layout()
        self.pic_list.append(fig2)

        ## P3
        fig3, ax = plt.subplots(nrows=1,ncols=3,figsize = (18,4), dpi=100)
        data[['CCFI:综合指数']].dropna(axis=0).plot(ax=ax[0])
        data[['CICFI:综合指数']].dropna(axis=0).plot(ax=ax[1])
        data[['波罗的海干散货指数(BDI)']].dropna(axis=0).plot(ax=ax[2])

        plt.tight_layout()
        self.pic_list.append(fig3)

        return data
    
    def fig_bond_premium(self):
        # * 1/3/5/10Y 国债到期收益率
        # 近一年
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

        ## P1 1/3/5/10Y 国债到期收益率
        fig1, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,8), dpi=100)
        dff[['1年国债',"国债_10年-1年"]].plot(ax=ax[0][0])
        dff[['3年国债',"国债_10年-3年"]].plot(ax=ax[0][1])
        dff[['5年国债',"国债_10年-5年"]].plot(ax=ax[1][0])
        dff[['10年国债']].plot(ax=ax[1][1])

        plt.tight_layout()
        self.pic_list.append(fig1)

def get_db_conn(io):
    with open(io, 'r') as f1:
        config = f1.readlines()
    for i in range(0, len(config)):
        config[i] = config[i].rstrip('\n')

    host = config[0]  
    username = config[1]  # 用户名 
    password = config[2]  # 密码
    schema = config[3]
    port = int(config[4])
    engine_txt = config[5]

    conn = pymysql.connect(	
        host = host,	
        user = username,	
        passwd = password,	
        db = schema,	
        port=port,	
        charset = 'utf8'	
    )	
    engine = create_engine(engine_txt)
    return conn, engine

if __name__=='__main__':

    """
    years = 10
    end = dt.datetime.today()
    start=dt.datetime.now() - dt.timedelta(days=years*365)
    start=start.strftime("%Y-%m-%d")
    end=end.strftime("%Y-%m-%d")
    """

    # 数据库私钥
    db_path = "/Users/wdt/Desktop/tpy/db.txt"
    conn , engine = get_db_conn(db_path)

    '''    
    report= Report()
    report.fig_liquidity_premium()
    report.pic_SRDI()
    report.fig_bond_leverage()
    report.fig_rates()
    report.fig_credit_premium()
    '''
    
    # 宏观
    report = Report(years=1)
    report.fig_industrial_production()
    report.fig_cpi_ppi_related()
    report.fig_upstream()
    report.fig_midstream()
    report.fig_downstream()
    
    report.print_all_fig()