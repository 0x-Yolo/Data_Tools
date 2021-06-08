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

plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False


def str2int(s):
    if type(s)!=str:
        return str(0)
    return int(s[:4]+s[5:7]+s[8:10])

def organize(df):    
    '''衍生列'''
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
            if not l[i]:
                # 跳过无隐含评级的行
                continue
            l[i] = dict_[l[i]]
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

    return df

def get_stat_table(df):
    '''计算统计数据'''
    trade_dt_list = df['时间'].unique()
    trade_dt_list.sort()
    stat_table = pd.DataFrame([],index = trade_dt_list)

    for date in trade_dt_list:
        df_date = df.loc[df['时间']==date]

        stat_table.loc[date, '均价'] = df_date.loc[(df_date['风险偏好']>0), 'price'].mean()
        stat_table.loc[date, '笔数'] = df_date.loc[(df_date['风险偏好']>0)].shape[0]
        stat_table.loc[date, '风险偏好指数'] = df_date.loc[(df_date['风险偏好']>0), '风险偏好'].mean()
        
        stat_table.loc[date, '情绪指数'] = (-1)*df_date.loc[(df_date['风险偏好']>0) \
            &(df_date['估值偏离']>-80)&(df_date['估值偏离']<80), '估值偏离'].mean()
    

        stat_table.loc[date, '平均期限'] = df_date.loc[(df_date['风险偏好']>0), '剩余期限'].mean()
        stat_table.loc[date, '信用扩张指数'] = df_date.loc[(df_date['风险偏好']>0), '风险偏好'].std()
        

    return stat_table



def upload1(df):
    name = 'secondary_credit_sec'
    columns_type = [VARCHAR(30),VARCHAR(30),Float(),DateTime(),DateTime(),
                    VARCHAR(30),Float(),Float(),DateTime(),
                    Float(),VARCHAR(30),Float(),Float(),
                    VARCHAR(30),VARCHAR(30),VARCHAR(30),
                    VARCHAR(30),VARCHAR(300),VARCHAR(30),
                    VARCHAR(30),VARCHAR(30),
                    VARCHAR(10),Float(),
                    Integer(),Integer(),Integer(),Integer(),Integer()]
    dtypelist = dict(zip(df.columns,columns_type))

    # for c in df.columns:
    #     df[c] = df[c].replace('',np.nan,regex=True)
    df['行权日'] = df['行权日'].replace(0,np.nan,regex=True)
    return df, name ,dtypelist


def upload2(stat):
    stat['date'] = stat.index
    name = 'secondary_credit_sec_stat'
    columns_type = [Float(),Float(),Float(),Float(),\
        Float(),Float(),DateTime()]
    dtypelist = dict(zip(stat.columns,columns_type))
    return stat , name , dtypelist



def main():
    # * Step1:获取数据
    d = pd.DataFrame([])
    for dir in os.listdir('./tmp_data'):
        if ('~$' in dir) | ('成交统计' not in dir):
            continue
        print(dir)

        x= int(re.findall(r'\d+', dir)[0])
        y= int(re.findall(r'\d+', dir)[1])
        z= int(re.findall(r'\d+', dir)[2])
        date = dt.datetime(int(x),int(y),int(z))
        dirr = pd.read_excel('./tmp_data'+'/'+dir,\
            sheet_name='信用债成交',header=1)
        dirr['时间'] = date
        dirr['估值时间'] = dirr['时间'] - dt.timedelta(days=1)
        d = d.append(dirr[['方向','代码','价格','时间','估值时间']])

    df = d.reset_index(drop = True)
    for idx in df.index:
        # q
        if type(df.loc[idx,'价格']) == str:
            print(idx)
            df.drop(idx,axis=0,inplace = True)

    # * Step2:添加windapi指标
    w.start()
    for idx in df.index:
        if idx < 2563:
            continue
        print(idx)

        code = df.loc[idx,'代码']
        net_price = df.loc[idx,'价格']
        net_date = df.loc[idx,'时间'].strftime("%Y%m%d")
        last_date=df.loc[idx,'估值时间'].strftime("%Y%m%d")

        # 修正非交易日
        # 方法：寻找一个银行间债券标的作为基准（xxxx国债），然后检查在当天的市场最近交易日是否与其相符
        df.loc[idx ,'估值时间'] = w.wss('010001.IB', \
        "last_trade_day","tradeDate={}".format(last_date)).Data[0][0]
        last_date = df.loc[idx,'估值时间'].strftime("%Y%m%d")
        
        # 基本信息
        
        df.loc[idx,['名字','type','rating','债券期限','城投','发行人','发行方式']] = w.wsd(code,\
            "sec_name,windl1type,latestissurercreditrating,\
            term2,municipalbond,issuer,issue_issuemethod",\
            last_date,last_date,'TradingCalendar=NIB',usedf=True)[1].values[0]


        # 【到期估值】
        df.loc[idx,'到期估值'] = w.wsd(code, "yield_cnbd", last_date, last_date,
            "credibility=4;PriceAdj=YTM;TradingCalendar=NIB").Data[0][0]
        if df.loc[idx,'到期估值'] == None:
            df.loc[idx,'到期估值'] = 0

        # 【行权估值】
        df.loc[idx,'行权估值'] = w.wsd(code, "yield_cnbd", last_date, last_date,
            "credibility=3;PriceAdj=YTM;TradingCalendar=NIB").Data[0][0]
        if df.loc[idx,'行权估值'] == None:
            df.loc[idx,'行权估值'] = 0
        
        # 【部分债无行权日】
        df.loc[idx,'行权日'] = w.wsd(code, "nxoptiondate",net_date,net_date, "type=All").Data[0][0]
        if df.loc[idx,'行权日'] == None :
            df.loc[idx,'行权日'] = 0
        # 【】
        df.loc[idx,'行业'] = w.wsd(code,"industry_csrc12_n",last_date,last_date,"industryType=3;TradingCalendar=NIB").Data[0][0]
        df.loc[idx,'企业性质']=w.wsd(code, "nature1", last_date, last_date, ";TradingCalendar=NIB").Data[0][0]
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
            
            price = x
        df.loc[idx,'price'] = price

        # 【估值偏离】
        ## 用当前成交价price和到期/行权估值的最小距离
        if df.loc[idx, '到期估值']==0:
            x =( w.wsd(code, "couponrate2").Data[0][0] - df.loc[idx,'price'] )* 100
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

    # * Step3:生成统计数据
    df = df[['方向','代码','价格','时间','估值时间',\
        '名字','到期估值','行权估值','行权日','price','type','估值偏离',\
        '剩余期限','rating','债券期限','城投','行业',\
            '发行人','企业性质','隐含评级','发行方式']]
    df = organize(df)
    stat_table = get_stat_table(df)

    # * Step4:原始数据与统计数据写进数据库
    conn,engine = do.get_db_conn()
    l = [upload2(stat_table),upload1(df)]
    # l = [upload1(df)]
    for a,b,c in l:
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)








