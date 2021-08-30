from numpy.lib import financial
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer,DECIMAL,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re

import data_organize as do

from WindPy import w
w.start()
years = 20
end = dt.datetime.today()
start=dt.datetime.now() - dt.timedelta(days=years*365)
start=start.strftime("%Y-%m-%d")
end=end.strftime("%Y-%m-%d")
end = '2021-07-07'




def daily_fig_liquidity_premium():
    err,df=w.edb('M0017139,M0041653,M0220163,\
    M0017142,M0048486,M1006642,M1006645,M0329545,\
    M1011048', start,end ,usedf=True)
    df.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年",
                "国股银票转贴现收益率_3m"]
    df['date'] = df.index
    # df = df.dropna(axis = 0)

    name = 'fig_liquidity_premium'
    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_bond_leverage():
    err, df=w.edb('M0041754,M0041746',start,'2021-06-30',usedf = True)
    df.columns = ['银行间质押式回购余额', '中债托管余额']
    # df = df.dropna(axis = 0)
    df['date'] = df.index

    name = 'fig_bond_leverage'
    columns_type=[
                  Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def get_sq_data():
    err,df = w.edb("M0096412,M0341750,M0096433,M0329565,M0329612,M0096484,\
            M0096505,M0096547,M0096526,M0096307,M0329591,M0340603,\
            M0340624,M0340645,M0340666,M0340687,M0340708", \
            "2010-01-01", "2021-08-12",usedf=True)
    df['date'] = df.index
    name='sq_dps_amt'
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
                Float(),Float(),Float(),Float(), Float(),Float(), 
                Float(),Float(),Float(),Float(), Float(),        
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def net_financing_amt():
    err,df = \
        w.wset("bondissuanceandmaturity",\
            "startdate=2015-01-01;enddate=2021-08-01;frequency=day;maingrade=all;zxgrade=all;datetype=startdate;type=default;bondtype=default;bondid=1000008489000000,a101020100000000,a101020200000000,a101020300000000,1000011872000000,a101020400000000,a101020700000000,a101020800000000,a101020b00000000,a101020500000000,1000013981000000,1000002993000000,1000004571000000,1000040753000000,a101020a00000000,a101020600000000,1000016455000000,a101020900000000;field=startdate,netfinancingamount",\
            usedf=True)
    name = 'net_financing_amt'
    columns_type=[DateTime(),Float()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_rates():
    err,df=w.edb('S0059744,S0059746,S0059747,S0059749,M1004263,M1004265,M1004267,M1004271',start,end,"Fill=Previous",usedf=True)
    df.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]
    df = df.dropna(axis = 0)
    df['date'] = df.index

    name = 'fig_rates'
    columns_type=[Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_credit_premium():
    # 城投AAA135、AA+135，国开3、国债3，二级资本债AAA-135
    err,df=w.edb("M0048432,M0048434,M0048435, \
                  M0048422,M0048424,M0048425, \
                  M0048412,M0048414,M0048415, \
                  M1004265,S0059746,          \
                  M1010704,M1010706,M1010708, \
                  M1015080,S0059738",start,end,usedf=True)

    df.columns=["中债城投债到期收益率(AAA):1年","中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AAA):5年",
                "中债城投债到期收益率(AA+):1年","中债城投债到期收益率(AA+):3年","中债城投债到期收益率(AA+):5年",
                "中债城投债到期收益率(AA):1年","中债城投债到期收益率(AA):3年","中债城投债到期收益率(AA):5年",
                "中债国开债到期收益率:3年","中债国债到期收益率:3年",
                "中债商业银行二级资本债到期收益率(AAA-):1年","中债商业银行二级资本债到期收益率(AAA-):3年","中债商业银行二级资本债到期收益率(AAA-):5年",
                "中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
    df['date'] = df.index
    #df = df.dropna(axis = 0)

    name = 'fig_credit_premium'
    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def fig_industrial_production():
    # 工业生产
    err,df = w.edb("S5704502,S5715680,S5708175,S5715660,S5417017,S5914175",
                    start, end,usedf = True)

    # ,"Fill=Previous"
    df.columns = ["日均产量：粗钢：国内", "日均产量：焦炭：重点企业(旬)",
                  "高炉开工率(163家):全国", "产能利用率:电炉:全国",
                  "PTA产业链负荷率:PTA工厂","浮法玻璃:产能利用率"]
    #df = df.dropna(axis = 0)
    # df = df.fillna(0)
    df['date'] = df.index

    name = 'fig_industrial_production'
    columns_type = [Float(),
                  Float(),
                  Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def fig_cpi_ppi_related():
    # 物价（CPI、PPI相关）
    err,df = w.edb("S0000241,S0000242,S0000240,S0000236,    \
           S5065111,S5065112,S0143884,S5042881,S0105896,S0031505,\
           S0248945,M6424471",
          start, end,usedf = True)
    df.columns = ["食用农产品价格指数:蛋类:周环比", "食用农产品价格指数:蔬菜类:周环比",
                  "食用农产品价格指数:禽类:周环比", "食用农产品价格指数",
                  '平均批发价:28种重点监测蔬菜', '平均批发价:7种重点监测水果','平均价:猪肉:全国',
                  '中国大宗商品价格指数:总指数','南华综合指数','CRB现货指数:综合',
                  '农产品批发价格200指数','iCPI:总指数:日环比']

    df['date'] = df.index

    name = 'fig_cpi_ppi_related'
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def fig_upstream():
    # 上游
    err,df = w.edb("S5104570,S5125686,S5111905,S5111903,\
            S5705040,S5705131,S0031648,S0031645,\
            M0066355,M0066356,S0049493,S0049494,S0200868",
            start, end, usedf = True)
    df.columns = ['综合平均价格指数:环渤海动力煤','炼焦煤库存:六港口合计',
                  '现货价:原油:英国布伦特Dtd','现货价:原油:美国西德克萨斯中级轻质原油(WTI)',
                  'Mylpic矿价指数:综合','国内铁矿石港口库存量','伦敦现货白银:以美元计价',
                  '伦敦现货黄金:以美元计价','期货收盘价(活跃合约):阴极铜','期货收盘价(活跃合约):铝',
                  '库存期货:阴极铜','库存期货:铝','南华焦炭指数']
    df['date'] = df.index
    name = 'fig_upstream'
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def fig_midstream():
    # 中游
    err,df = w.edb("S5705039,S0247603,S0181750,S5914515,S5907373,S5416650,M0067419,M0066359,\
                M0066348,M0066350", \
                   start, end, usedf = True)
    df.columns = ['Mylpic综合钢价指数','库存:主要钢材品种:合计','库存:螺纹钢(含上海全部仓库)',
                  '水泥价格指数:全国','中国玻璃价格指数','中国盛泽化纤价格指数',
                  '期货收盘价(活跃合约):PVC','期货收盘价(活跃合约):天然橡胶',
                  '期货收盘价(活跃合约):黄大豆1号','期货收盘价(活跃合约):黄玉米']
    df['date'] = df.index
    name = 'fig_midstream'
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def fig_downstream():
    err,df=w.edb("S2707379,S2707380,S2726996,S6126413, \
                  S0049599,S0000293,S6500614,S6424740, \
                  S6604459,S6604460,S0000066,S0237842,S0031550",
                start, end,usedf = True)
    df.columns = ['30大中城市:商品房成交套数','30大中城市:商品房成交面积','100大中城市:成交土地溢价率:当周值',
                  '当周日均销量:乘用车:厂家零售','柯桥纺织:价格指数:总类','义乌中国小商品指数:总价格指数',
                  '中关村电子价格产品指数','中国公路物流运价指数','电影票房收入','电影观影人次',
                  'CCFI:综合指数','CICFI:综合指数','波罗的海干散货指数(BDI)']
    df['date'] = df.index
    name = 'fig_downstream'
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist


def industries_premium():
    # 地产/钢铁/煤炭/有色/汽车
    err,df = w.edb("M1008950,M1008953,M1008973,M1008971,M1008964", 
                   start, end, usedf = True) 
    df.columns = ["信用利差_地产","信用利差_钢铁","信用利差_煤炭",\
                  "信用利差_有色","信用利差_汽车"]
    df['date'] = df.index
    name = 'fig_industries_premium'

    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df,name,dtypelist

def ccl():
    # 超储率
    ## 2015年前无政府存款记录
    err,df = w.edb("M0001528,M0062047,M0251905,M0043821,M0061518,M0043823,M0010096,\
          M0001690,M0001380",\
         "2010-01-01", "2021-06-16", usedf=True)
    df.columns=['住户存款','非金融企业存款','政府存款',\
        '中小型准备金率','大型准备金率','超额准备金率','超储率_季度',\
            '基础货币','M0']
    df['date'] = df.index

    name = 'ccl_related'
    columns_type = [Float(),Float(),Float(),Float(),
                    Float(),Float(),Float(),Float(),
                    Float(),DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df,name,dtypelist

def leverage_rate():
    err,df = w.edb("M0341983,M0041754,M0341128,M0340862,M0340881,\
        M0341107,M0340845,M0340864", \
        "2010-06-16", "2021-06-16",usedf=True)
    df.columns=['托管量','待购回',
    '托管量_证券','待购回_证券','待返售_证券',
    '托管量_保险','待购回_保险','待返售_保险']

    dff = pd.DataFrame([])
    dff['总资产']= df['托管量_保险']+df['待返售_保险']
    dff['净资产']=dff['总资产']-df['待购回_保险']
    (dff['总资产']/dff['净资产']).plot()

    dff = df[['托管余额','回购成交量']].fillna(method='ffill').dropna()
    dff['净资产'] = dff['托管余额']-dff['回购成交量']
    (dff['托管余额']/dff['净资产'])[-500:].plot()

def broad_liquid():
    err,df = w.edb("M0011456,M5525763,M0001385,M0061578,M1002334,\
            M0001227,M0001383,M0010075",\
         "2000-06-17", "2021-06-17",usedf=True)
    df.columns=['贷款需求指数','社融_tb','M2_tb',
                '票据直贴利率_6m_长三角','票据_AA+_3y',
                'ppi_tb','M1_tb','DR007_monthly']    
    df['date']=df.index
    name = 'broad_liquid'
    columns_type = [Float(),Float(),Float(),Float(),
                    Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df,name,dtypelist

def rates_us():
    err,df = w.edb("G0000886,G0000887,G0000891,G8455661,M0000185,G0000898,M0000271", "2000-06-21", "2021-08-17",usedf=True)
    df.columns = ['美债1年','美债2年','美债10年','美债10-2','美元兑人民币','libor_3m','美元指数']
    df['date'] = df.index
    name = 'rates_us'
    columns_type=[Float(),Float(),Float(),Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def local():
    name = 'localbond_issue'
    err,df = w.edb("M5658453,M6191591", "2003-12-01", "2021-06-30",usedf=True)
    df.columns = ['地方专项债限额','地方专项债累计发行额']
    df['date'] = df.index

    columns_type=[Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def fundAmt():
    name = 'fundAmt'
    err,df = w.edb("M5207867,M5207864,M5207865,M5207866", \
            "2020-01-01", "2021-08-02",usedf=True)
    df.columns = ['货币基金份额', '股票基金份额', \
        '混合型基金份额','债券基金份额']
    df['date'] = df.index

    columns_type=[Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def indices():
    err,df = w.edb("M0051553,M0340363,M0340367,M0265754,M0051568,M0051567,M0265766,M0265767,M0265768,M0265769",\
         "2003-12-01", "2022-07-31",usedf=True)
    df.columns=['中债总指数','1-5年政金债指数','7-10年政金债指数',\
        '中债信用总指数','中债短融总指数','中债中票总指数','中债企业债AAA指数',\
        '中债企业债AA+指数','中债企业债AA指数','中债企业债AA-指数']
    name = 'bond_indices'
    df['date'] = df.index
    
    columns_type=[Float(),Float(),Float(),Float(),Float(),
                    Float(),Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def hs300():
    err,df = w.wsd("000300.SH", "dividendyield2", \
        "2002-01-01", "2021-06-30", usedf=True)
    df.columns = ['股息率']

    df['date'] = df.index
    name = 'hs300Div'
    columns_type=[Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def rate_syn():
    # 利率同步指标
    err,df = w.edb("S6002167,S5914515,S5700047,S5103920,S5705131,S6604459,M0017126,M0001714,M0001689,M0000271,S0180904,S0180903",\
         "2000-07-02", "2021-08-08",usedf=True)
    df.columns = ['挖掘机销量同比','水泥价格指数','重点企业粗钢产量','重点电厂煤耗总量',\
        '国内铁矿石港口库存量','电影票房收入','PMI','其他存款性公司:总资产',\
        '货币当局:总资产','美元指数','铜价','金价']
    name = 'rate_syn'
    df['date'] = df.index
    columns_type=[Float(),Float(),Float(),Float(),Float(),Float(),
        Float(),Float(),Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def quanti2():
    # err,df = w.edb("M0290392,M0327992,M0265778,\
    #     M0265865,M0265846,M0265884",\
    #      "2000-01-01", "2021-07-01",usedf=True)
    _,df = w.wsd("CBA02501.CS,CBA02511.CS,CBA02521.CS,CBA02531.CS,CBA02541.CS,CBA02551.CS,CBA02561.CS,CBA00101.CS",\
         "close", "2015-01-01", "2021-08-29", "",usedf=True)

    err,df = w.wsd("CBA00623.CS,CBA00653.CS,\
        CBA00621.CS, CBA00651.CS,\
        CBA02411.CS,\
        CBA02523.CS,CBA02553.CS,\
        CBA02521.CS,CBA02551.CS,CBA02552.CS,CBA00652.CS,", \
    "close", "2010-01-01", "2021-07-20", "",usedf=True)
    df.columns = ['国债全价1-3y','国债全价7-10y',
            '国债总财富1-3y','国债总财富7-10y',
            'cd_1y',
            '国开债全价1-3y','国开债全价7-10y',
            '国开债总财富1-3y','国开债总财富7-10y','国开债净价7-10y','国债净价7-10y']
    df['date'] = df.index
    name = 'quanti2'
    columns_type=[DECIMAL(10,4),DECIMAL(10,4),DECIMAL(10,4),
                  DECIMAL(10,4),DECIMAL(10,4),
                  DECIMAL(10,4),DECIMAL(10,4),
                  DECIMAL(10,4),DECIMAL(10,4),DECIMAL(10,4),DECIMAL(10,4),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def bond_future():
    # err,df = w.wsd("T2109.CFE,T2106.CFE,T2103.CFE,T2012.CFE,T2009.CFE,\
    #     T2006.CFE,T2003.CFE,T1912.CFE,T1909.CFE,T1906.CFE,\
    #     T1903.CFE,T1812.CFE,T1809.CFE,T1806.CFE,T1803.CFE,\
    #     T1712.CFE,T1709.CFE,T1706.CFE,T1703.CFE,T1612.CFE,\
    #     T1609.CFE,T1606.CFE,T1603.CFE,T1512.CFE,T1509.CFE", \
    #     "close", "2010-07-08", "2021-07-08", "",usedf=True)
    err,df=w.wsd("T2109.CFE,T2106.CFE,T2103.CFE,T2012.CFE,T2009.CFE,T2006.CFE,T2003.CFE,T1912.CFE,T1909.CFE,T1906.CFE,T1903.CFE,T1812.CFE,T1809.CFE,T1806.CFE,T1803.CFE,T1712.CFE,T1709.CFE,T1706.CFE,T1703.CFE,T1612.CFE,T1609.CFE,T1606.CFE,T1603.CFE,T1512.CFE,T1509.CFE",\
         "volume", "2015-03-20", "2021-07-08", "",usedf=True)
    err,df=w.wsd("T2109.CFE,T2106.CFE,T2103.CFE,T2012.CFE,T2009.CFE,T2006.CFE,T2003.CFE,T1912.CFE,T1909.CFE,T1906.CFE,T1903.CFE,T1812.CFE,T1809.CFE,T1806.CFE,T1803.CFE,T1712.CFE,T1709.CFE,T1706.CFE,T1703.CFE,T1612.CFE,T1609.CFE,T1606.CFE,T1603.CFE,T1512.CFE,T1509.CFE",\
         "open", "2015-03-20", "2021-07-08", "",usedf=True)
    err,df=w.wsd("T2109.CFE,T2106.CFE,T2103.CFE,T2012.CFE,T2009.CFE,T2006.CFE,T2003.CFE,T1912.CFE,T1909.CFE,T1906.CFE,T1903.CFE,T1812.CFE,T1809.CFE,T1806.CFE,T1803.CFE,T1712.CFE,T1709.CFE,T1706.CFE,T1703.CFE,T1612.CFE,T1609.CFE,T1606.CFE,T1603.CFE,T1512.CFE,T1509.CFE",\
         "close", "2015-03-20", "2021-07-08", "",usedf=True)
    # df.columns = ['m1','ppi']
    df['date'] = df.index
    # name='all_treasure_futures'
    name = 'all_treasure_futures_vol'
    columns_type = [Float(),Float(),Float(),Float(),Float(),
                     Float(),Float(),Float(),Float(),Float(),
                     Float(),Float(),Float(),Float(),Float(),
                     Float(),Float(),Float(),Float(),Float(),
                     Float(),Float(),Float(),Float(),Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
def t10():
    err,df = w.wsd("T.CFE", "close,open,high,low,oi_loi,oi_soi,volume",\
         "2015-03-20", "2021-07-11", "order=25",usedf=True)
    df['date'] = df.index
    name='t10'
    columns_type = [Float(),Float(),Float(),
                    Float(),Float(), Float(), Float(),         
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
def bond_future_h():
    # err,df=w.wsi("T.CFE", "open,close",\
    #      "2021-03-01 09:00:00", "2021-07-10 23:48:15", \
    #     "BarSize=60",usedf=True)
    err,df=w.wsi("T.CFE", "open,close",\
         "2021-03-01 09:00:00", "2021-07-10 23:48:15", \
        "BarSize=30",usedf=True)
    df['date']=df.index
    name='t2109_halfhour'
    columns_type = [Float(),Float(),       
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
def bond_future_min():
    err,df=w.wsi("T.CFE", "open,close",\
         "2021-03-01 09:00:00", "2021-07-10 23:48:15", \
        "BarSize=5",usedf=True)
    # err,df = w.wsi("T.CFE", "open,close", \
    #     "2021-01-13 09:00:00", "2021-07-13 10:28:15", "BarSize=60")
    df['date']=df.index
    name='t2109_5min'
    columns_type = [Float(),Float(),       
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
def bond_v2():
    err,df=w.wsi("T2109.CFE,T2106.CFE,T2103.CFE,T2012.CFE,T2009.CFE,\
         T2006.CFE,T2003.CFE,T1912.CFE,T1909.CFE,T1906.CFE,\
         T1903.CFE,T1812.CFE,T1809.CFE,T1806.CFE,T1803.CFE", \
    "open,close", "2018-01-01 09:00:00", "2021-07-21 21:17:00", "BarSize=30",usedf=True)
    df['date']=df.index
    name='t10_30min'
    columns_type = [VARCHAR(10),Float(),Float(),       
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist


def gz_issue_amt():
    # 国债发行
    err,df = w.wset("nationaldebtissueandclosesub",\
        "startdate=2010-07-04;enddate=2021-08-4;\
        frequency=day;maingrade=all;zxgrade=all;\
        datetype=startdate;type=default;bondtype=governmentbonds;\
        bondid=1000008489000000,a101020100000000,a101020200000000,a101020300000000,1000011872000000,a101020400000000,a101020700000000,a101020800000000,a101020b00000000,a101020500000000,1000013981000000,1000002993000000,1000004571000000,a101020a00000000,a101020600000000,1000016455000000,a101020900000000;\
        field=startdate,windcode,issueprice,term,issuer",usedf=True)
    name = 'gz_issue_amt'
    columns_type = [DateTime(),VARCHAR(20),Float(),Float(),VARCHAR(15)]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
def zj_issue_amt():
    # 政金发行
    err,df = w.wset("nationaldebtissueandclosesub",\
        # "startdate=2010-07-04;enddate=2021-08-04;\
        "startdate=2000-07-04;enddate=2010-07-03;\
        frequency=day;maingrade=all;zxgrade=all;\
        datetype=startdate;type=default;bondtype=policybankbonds;\
        bondid=1000008489000000,a101020100000000,a101020200000000,a101020300000000,1000011872000000,a101020400000000,a101020700000000,a101020800000000,a101020b00000000,a101020500000000,1000013981000000,1000002993000000,1000004571000000,a101020a00000000,a101020600000000,1000016455000000,a101020900000000;\
        field=startdate,windcode,name,issueprice,term,issuer",usedf=True)
    name = 'zj_issue_amt'
    columns_type = [DateTime(),VARCHAR(20),VARCHAR(20),\
        Float(),Float(),VARCHAR(15)]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def bond_index():
    err,df = w.wsd("CBA05821.CS,CBA05831.CS,CBA05841.CS,CBA05851.CS,CBA02711.CS,CBA02721.CS,CBA02731.CS,CBA02741.CS,CBA02751.CS,CBA05801.CS,CBA02701.CS,CBA01901.CS,CBA03801.CS", "pct_chg", "2015-01-01", "2021-08-11", "",usedf=True)
    name = 'bond_idx'
    df['date'] = df.index
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
            Float(),Float(),Float(),Float(), Float(),Float(),Float(),          
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist
    
def bond_dura():
    err,df = w.wsd("CBA05821.CS,CBA05831.CS,CBA05841.CS,CBA05851.CS,CBA02711.CS,CBA02721.CS,CBA02731.CS,CBA02741.CS,CBA02751.CS,CBA05801.CS,CBA02701.CS,CBA01901.CS,CBA03801.CS", "duration", "2015-01-01", "2021-08-11", "",usedf=True)
    name = 'bond_dura'
    df['date'] = df.index
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
            Float(),Float(),Float(),Float(), Float(),Float(),Float(),          
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def bond_fund():
    # 基金dura - 中长期纯债
    err,df = w.wsd("000005.OF,000015.OF,000016.OF,000024.OF,000025.OF,000032.OF,\
    000033.OF,000037.OF,000053.OF,000064.OF,000069.OF,000070.OF,000074.OF,\
    000077.OF,000078.OF,000079.OF,000086.OF,000104.OF,000105.OF,000106.OF,000111.OF,000112.OF,000113.OF,000115.OF,000116.OF,000122.OF,000123.OF,000134.OF,000135.OF,000137.OF,000138.OF,000139.OF,000141.OF,000147.OF,000148.OF,000152.OF,000153.OF,000174.OF,000175.OF,000183.OF,000186.OF,000187.OF,000188.OF,000191.OF,000192.OF,000194.OF,000197.OF,000200.OF,000201.OF,000205.OF,000206.OF,000212.OF,000213.OF,\
    000221.OF,000222.OF,000227.OF,000235.OF,000239.OF,000240.OF,000244.OF,000245.OF,000246.OF,000252.OF,000253.OF,000254.OF,000255.OF,000265.OF,000266.OF,000267.OF,000268.OF,000271.OF,000272.OF,000277.OF,000286.OF,000289.OF,000295.OF,000296.OF,000298.OF,000299.OF,000305.OF,000310.OF,000319.OF,000320.OF,000329.OF,000335.OF,000345.OF,000346.OF,000347.OF,000355.OF,000356.OF,000372.OF,000395.OF,000396.OF,000402.OF,000403.OF,000415.OF,000416.OF,000419.OF,000420.OF,000465.OF,000469.OF,000489.OF,000490.OF,000497.OF,000516.OF,000517.OF,000521.OF,000546.OF,000552.OF,000553.OF,000561.OF,000562.OF,000563.OF,000564.OF,000583.OF,000606.OF,000655.OF,",\
        "NAV_adj_return1", "2015-01-01", "2021-08-11", "", usedf=True)
    
    name = 'fund_nav'
    df['date'] = df.index
    columns_type =[DECIMAL(10,6) for _ in range(df.shape[0]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def organs_nav():
    err,df=w.edb("M0265776,M0265774,M0265775,M0265773,M0265777",\
         "2015-01-01", "2021-08-11",usedf=True)
    name = 'organs_nav'
    # df.columns = ['证券','基金','保险','商业银行','信托']
    df['date'] = df.index
    columns_type =[DECIMAL(10,4) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def main(): 
    """
    db_path = "/Users/wdt/Desktop/tpy/db.txt"
    
    l = [daily_fig_SRDI(),
     daily_fig_liquidity_premium(),
     daily_fig_bond_leverage(),
     daily_fig_rates(),
     daily_fig_credit_premium()
    ]


    # DONE 宏观数据上传数据库
    l = [fig_industrial_production(),fig_cpi_ppi_related(),
         fig_upstream(),fig_midstream(),fig_downstream(),
         ]
    """

 
    l = [fig_downstream()]
    l=[daily_fig_bond_leverage()]
    l=[net_financing_amt()]
    l=[rates_us()]
    conn , engine = do.get_db_conn()
    for a,b,c in l:
        # for i in range(len(a)):
            # try:
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
        print(b, '写入完成')
        
main()



