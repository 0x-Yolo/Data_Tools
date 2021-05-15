import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
from WindPy import w
import data_organize as do
w.start()

def str2int(s):
    if type(s)==int:
        return s
    return int(s[:4]+s[5:7]+s[8:10])

conn,engine = do.get_db_conn()
# 导入数据，邮件/本地
df = pd.read_sql('select * from finance.CreditBondTrading_v3',conn)
# test
data = pd.read_excel('./examples/21010426-0430.xlsm',sheet_name='数据')
data.loc[(data['行权日'] == 0) & (data['价格']>20)]
data.loc[(data['代码'] == '102100828.IB') ] # idx=70



# 添加windapi指标
for idx in df.index:
    print(idx)
    code = df.loc[idx,'代码']
    net_price = df.loc[idx,'价格']
    net_date = df.loc[idx,'时间'].strftime("%Y%m%d")
    last_date=df.loc[idx,'估值时间'].strftime("%Y%m%d")

    # 修正非交易日
    df.loc[idx ,'估值时间'] = w.wss("000001.SH", \
    "lastradeday_s","tradeDate={}".format(last_date)).Data[0][0]
    last_date = df.loc[idx,'估值时间'].strftime("%Y%m%d")
    
    # 基本信息
    df.loc[idx,['名字','type','rating','债券期限','城投','发行人','发行方式']] = w.wsd(code,\
        "sec_name,windl1type,latestissurercreditrating,\
         term2,municipalbond,issuer,issue_issuemethod",usedf=True)[1].values[0]
   
    # 【到期估值】
    df.loc[idx,'到期估值'] = w.wsd(code, "yield_cnbd", last_date, last_date,
         "credibility=4;PriceAdj=YTM").Data[0][0]
    if df.loc[idx,'到期估值'] == None:
        df.loc[idx,'到期估值'] = w.wsd(code, "yield_cnbd", net_date, net_date,
         "credibility=4;PriceAdj=YTM").Data[0][0]
        print('遇到新股',code)
    if df.loc[idx,'到期估值'] == None:
        # 188035
        print('新股且无法读取今日估值,跳过',code , net_date)
        continue

    # 【行权估值】
    df.loc[idx,'行权估值'] = w.wsd(code, "yield_cnbd", last_date, last_date,
         "credibility=3;PriceAdj=YTM").Data[0][0]
    if df.loc[idx,'行权估值'] == None:
        df.loc[idx,'行权估值'] = w.wsd(code, "yield_cnbd", net_date, net_date,
         "credibility=3;PriceAdj=YTM").Data[0][0]
        print('遇到新股',code)
    if df.loc[idx,'到期估值'] == None:
        print('无法读取到期估值,跳过',code , net_date)
    
    # 【部分债无行权日】
    df.loc[idx,'行权日'] = w.wsd(code, "nxoptiondate",net_date,net_date, "type=All").Data[0][0]
    if df.loc[idx,'行权日'] == None:
        df.loc[idx,'行权日'] = 0
    # 【】
    df.loc[idx,'行业'] = w.wsd(code,"industry_csrc12_n",last_date,last_date,"industryType=3").Data[0][0]
    df.loc[idx,'企业性质']=w.wsd(code, "nature1", last_date, last_date, "").Data[0][0]
    df.loc[idx,'隐含评级'] = w.wsd(code, "rate_latestMIR_cnbd", net_date, net_date, "").Data[0][0]
    # 【price】
    if df.loc[idx,'价格']<20:
        price = df.loc[idx,'价格']
    else: 
        x = w.wss(code, "calc_yield","","balanceDate={};bondPrice={};\
            bondPriceType=1;maturityDate={}".\
            format(int(net_date),net_price,\
            str2int(df.loc[idx,'行权日'])) ).Data[0][0]

        if not x:
            print('price超过20的且无值：',idx) # 
            continue

        if x < 0.3:
            price = w.wss(code, "calc_yield","","balanceDate={};bondPrice={};\
                bondPriceType=1".\
                format(int(net_date),net_price)).Data[0][0]
            # test
            print(code,net_date,'bc1小于0.3用了不含行权日的到期收益率')
        else:
            price = x
    df.loc[idx,'price'] = price
    # 【估值偏离】
    ## 用当前成交价price和到期/行权估值的最小距离
    if df.loc[idx, '到期估值']==0:
        x =( w.wsd(code, "couponrate2").Data[0][0] - df.loc[1,'price'] )* 100
    else:
        if abs(df.loc[idx,'price']-df.loc[idx,'到期估值']) > abs(df.loc[idx,'price']-df.loc[idx,'行权估值']):
            x = (df.loc[idx,'price']-df.loc[idx,'行权估值'])*100
        else:
            x = (df.loc[idx,'price']-df.loc[idx,'到期估值'])*100
    df.loc[idx,'估值偏离'] = x
    # 【剩余期限】
    if abs(df.loc[idx,'price'] - df.loc[idx,'到期估值']) > abs(df.loc[idx,'price'] - df.loc[idx,'行权估值']):
        x = w.wsd(code,"termifexercise", net_date, net_date, "").Data[0][0]
    else:
        x = w.wsd(code,"ptmyear", net_date, net_date, "").Data[0][0]
    df.loc[idx,'剩余期限'] = x


# 存入数据库
for i in range(20):
    print(df.columns[i],df.iloc[0,i])

columns_type = [VARCHAR(30),VARCHAR(30),Float(),DateTime(),DateTime(),
                  VARCHAR(30),Float(),Float(),DateTime(),
                  Float(),VARCHAR(30),Float(),Float(),
                  VARCHAR(30),VARCHAR(30),VARCHAR(30),
                  VARCHAR(30),VARCHAR(40),VARCHAR(30),
                  VARCHAR(30),VARCHAR(30)]
dtypelist = dict(zip(df.columns,columns_type))

for c in df.columns:
    df[c] = df[c].replace('',np.nan,regex=True)
df['行权日'] = df['行权日'].replace(0,np.nan,regex=True)
l = [(df,'CreditBondTrading',dtypelist)]
for a,b,c in l:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
    

## * 自生成的列
def anal_grouping(se):
    """按照剩余期限对债券分类"""
    l = se.tolist()
    for i in range(len(l)):
        if l[i] <= 0.33:
            l[i] = '0.33'
        elif l[i] <= 0.5:
            l[i] = '0.5'
        elif l[i] <= 1:
            l[i] = '1'
        elif l[i] <= 2:
            l[i] = '2'
        elif l[i] <= 3:
            l[i] = '3'
        elif l[i] <= 5:
            l[i] = '5'
        elif l[i] <= 7:
            l[i] = '7'
        else:
            l[i] = '7+'
    return l
def get_riskpreference(se):
    """按照隐含评级对债券分类"""
    dict_ = {'AAA+' : 1,'AAA' : 2,'AAA-' : 3,'AA+' : 4,'AA' : 5,\
    'AA(2)' : 6,'AA-' : 7,'A+' : 8,'A' : 9,'A-' : 10} 
    l = se.tolist()
    for i in range(len(l)):
        l[i] = dict_(l[i])
    return l
def find_keywords(se,s):
    """按照债券名称中的关键词对债券分类"""
    l = se.tolist()
    for i in range(len(l)):
        if s in l[i]:
            l[i] = 1
        else:
            l[i] = 0
    return l

df['剩余期限分组'] = anal_grouping(df['剩余期限'])
df['风险偏好'] = get_riskpreference(df['隐含评级'])

df['地产'] = (df['行业']=='房地产业').astype(int).tolist()
df['钢铁'] = (df['行业']=='黑色金属冶炼和压延加工业').astype(int).tolist()
df['煤炭'] = (df['行业']=='煤炭开采和洗选业').astype(int).tolist()

df['永续'] = find_keywords(df['名字'], 'N')
df['PPN'] = find_keywords(df['名字'], 'PPN')

# 找到excel文件内函数对应windapi，拉取，上传