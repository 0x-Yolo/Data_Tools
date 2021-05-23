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
import data_organize as do

from WindPy import w


def fig_industrial_production():
    name = 'fig_industrial_production'
    last_date = do.get_latest_date(name)
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
    last_date = do.get_latest_date(name)
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
    last_date = do.get_latest_date(name)
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
    last_date = do.get_latest_date(name)
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
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb("S2707379,S2707380,S2726996,S6126413, \
                  S0049599,S0000293,S6500614,S6424740, \
                  S6604459,S6604460,S0000066,S0237842,S0031550",
                last_date, today_date,usedf = True)
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

def main():
    conn,engine = do.get_db_conn() 
    w.start()
    # 宏观周报数据
    l =    [
            fig_industrial_production(),
            fig_cpi_ppi_related(),
            fig_upstream(),fig_downstream(),fig_midstream()
            ]

    for a,b,c in l:
        if len(np.array(a)) == 0:
            print(b , '已是最新，无需更新')
            continue
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print('成功更新表',b, '至',do.get_latest_date(b))

