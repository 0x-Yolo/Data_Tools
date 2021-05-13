import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re

from WindPy import w

def upload_date(name):
    """
    输入表名
    输出该表的最新日期
    """
    
    dir_date = []
    df = pd.read_sql('select * from {}'.format(name) , conn)
    last_date = df.iloc[-1 , -1]
    
    # start_date = last_date + dt.timedelta(days = 1)
    # end_date = dt.datetime.now()
    # return start_date , end_date
    return last_date 


def daily_fig_SRDI():
    name = 'fig_SRDI'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1004529,M0330244,M0330245,M0330246,M0330247,M0330248,M0330249,M0330250,M0330251,M0330252,M0330253',
               last_date,today_date.strftime("%Y-%m-%d"), "Fill=Previous",usedf=True)
    
    if df.shape[1] == 1:
        return [],name,[]

    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M']
    df['date'] = df.index
    df = df.dropna(axis = 0)
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def daily_fig_liquidity_premium():
    name = 'fig_liquidity_premium'
    
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb('M0017139,M0041653,M0220163,\
    M0017142,M0048486,M1010889,M1010892,M0329545,\
    M1011048', \
        last_date,today_date,"Fill=Previous",usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["shibor_7d","质押回购利率_7天","存款类质押回购利率_7天",
                "shibor_3m","IRS：FR007：1y","存单_AAA_3m","存单_AAA_1y","MLF：1年",
                 "国股银票转贴现收益率_3m"]
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_fig_bond_leverage():
    name = 'fig_bond_leverage'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041739,M5639029',last_date,today_date,usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns = ['成交量:银行间质押式回购', '债券市场托管余额']
    # df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(4),
                  Float(1),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name, dtypelist

def daily_fig_rates():
    name = 'fig_rates'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb('S0059744,S0059746,S0059747,S0059749,M1004263,M1004265,M1004267,M1004271',
                 last_date,today_date,"Fill=Previous",usedf=True)
        
    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["1年国债","3年国债","5年国债","10年国债","1年国开","3年国开","5年国开","10年国开"]
    df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[df.date > last_date]

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
    name = 'fig_credit_premium'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))
    
    err,df=w.edb("M0048432,M0048434,M0048435, \
                  M0048422,M0048424,M0048425, \
                  M0048412,M0048414,M0048415, \
                  M1004265,S0059746,          \
                  M1010704,M1010706,M1010708, \
                  M1015080,S0059738",
                 last_date,today_date,usedf=True)

    if df.shape[1] == 1:
        return [],name,[]

    df.columns=["中债城投债到期收益率(AAA):1年","中债城投债到期收益率(AAA):3年","中债城投债到期收益率(AAA):5年",
                "中债城投债到期收益率(AA+):1年","中债城投债到期收益率(AA+):3年","中债城投债到期收益率(AA+):5年",
                "中债城投债到期收益率(AA):1年","中债城投债到期收益率(AA):3年","中债城投债到期收益率(AA):5年",
                "中债国开债到期收益率:3年","中债国债到期收益率:3年",
                "中债商业银行二级资本债到期收益率(AAA-):1年","中债商业银行二级资本债到期收益率(AAA-):3年","中债商业银行二级资本债到期收益率(AAA-):5年",
                "中债可续期产业债到期收益率(AAA):3年","中债中短期票据到期收益率(AAA):3年"]
    df['date'] = df.index
    df = df.loc[df.date > last_date]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def fig_industrial_production():
    name = 'fig_industrial_production'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("S5704502,S5715680,S5708175,S5715660,S5417017,S5914175",
                    last_date,today_date,usedf = True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ["日均产量：粗钢：国内", "日均产量：焦炭：重点企业(旬)",
                  "高炉开工率(163家):全国", "产能利用率:电炉:全国",
                  "PTA产业链负荷率:PTA工厂","浮法玻璃:产能利用率"]
    df['date'] = df.index
    df = df.loc[df.date>last_date]
    columns_type = [Float(),
                  Float(),
                  Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def fig_cpi_ppi_related():
    name = 'fig_cpi_ppi_related'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("S0000241,S0000242,S0000240,S0000236,    \
           S5065111,S5065112,S0143884,S5042881,S0105896,S0031505,\
           S0248945,M6424471",
          last_date, today_date,usedf = True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ["食用农产品价格指数:蛋类:周环比", "食用农产品价格指数:蔬菜类:周环比",
                  "食用农产品价格指数:禽类:周环比", "食用农产品价格指数",
                  '平均批发价:28种重点监测蔬菜', '平均批发价:7种重点监测水果','平均价:猪肉:全国',
                  '中国大宗商品价格指数:总指数','南华综合指数','CRB现货指数:综合',
                  '农产品批发价格200指数','iCPI:总指数:日环比']
    df['date'] = df.index
    df = df.loc[df.date>last_date]
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def fig_upstream():
    name = 'fig_upstream'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("S5104570,S5125686,S5111905,S5111903,\
            S5705040,S5705131,S0031648,S0031645,\
            M0066355,M0066356,S0049493,S0049494,S0200868",
            last_date, today_date, usedf = True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['综合平均价格指数:环渤海动力煤','炼焦煤库存:六港口合计',
                  '现货价:原油:英国布伦特Dtd','现货价:原油:美国西德克萨斯中级轻质原油(WTI)',
                  'Mylpic矿价指数:综合','国内铁矿石港口库存量','伦敦现货白银:以美元计价',
                  '伦敦现货黄金:以美元计价','期货收盘价(活跃合约):阴极铜','期货收盘价(活跃合约):铝',
                  '库存期货:阴极铜','库存期货:铝','南华焦炭指数']
    df['date'] = df.index
    df = df.loc[df.date>last_date]
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def fig_midstream():
    name = 'fig_midstream'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("S5705039,S0247603,S0181750,S5914515,S5907373,S5416650,M0067419,M0066359,\
                M0066348,M0066350", \
                   last_date, today_date, usedf = True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['Mylpic综合钢价指数','库存:主要钢材品种:合计','库存:螺纹钢(含上海全部仓库)',
                  '水泥价格指数:全国','中国玻璃价格指数','中国盛泽化纤价格指数',
                  '期货收盘价(活跃合约):PVC','期货收盘价(活跃合约):天然橡胶',
                  '期货收盘价(活跃合约):黄大豆1号','期货收盘价(活跃合约):黄玉米']
    df['date'] = df.index
    df = df.loc[df.date>last_date]
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def fig_downstream():
    name = 'fig_downstream'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb("S2707379,S2707380,S2726996,S6126413, \
                  S0049599,S0000293,S6500614,S6424740, \
                  S6604459,S6604460,S0000066,S0237842,S0031550",
                start, end,usedf = True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['30大中城市:商品房成交套数','30大中城市:商品房成交面积','100大中城市:成交土地溢价率:当周值',
                  '当周日均销量:乘用车:厂家零售','柯桥纺织:价格指数:总类','义乌中国小商品指数:总价格指数',
                  '中关村电子价格产品指数','中国公路物流运价指数','电影票房收入','电影观影人次',
                  'CCFI:综合指数','CICFI:综合指数','波罗的海干散货指数(BDI)']
    df['date'] = df.index
    df=df.loc[df.date>last_date]
    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df , name , dtypelist

def industial_premium():
    name = 'fig_industries_premium'
    last_date = upload_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb("M1008950,M1008953,M1008973,M1008971,M1008964", 
                   start, end, usedf = True) 
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ["信用利差_地产","信用利差_钢铁","信用利差_煤炭",\
                  "信用利差_有色","信用利差_汽车"]
    df['date'] = df.index
    df=df.loc[df.date>last_date]

    columns_type = [Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df,name,dtypelist



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

def main():
    w.start()

    # @ 读取db.txt内的邮箱信息
    db_path = "/Users/wdt/Desktop/tpy/db.txt"
    conn , engine = get_db_conn(db_path)

    l =    [daily_fig_SRDI(),
            daily_fig_bond_leverage(),
            daily_fig_credit_premium(),
            daily_fig_liquidity_premium(),
            daily_fig_rates(),industial_premium()
            ]
    # 宏观周报数据
    l2 =    [
            fig_industrial_production(),
            fig_cpi_ppi_related(),
            fig_upstream(),fig_downstream(),fig_midstream()
            ]

    for a,b,c in l:
        if len(np.array(a)) == 0:
            print(b , '已是最新，无需更新')
            continue
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print('成功更新表',b)

if __name__=='__main__':
    main()