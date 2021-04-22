import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import pandas as pd
import numpy as np
import datetime as dt#准备工作，配置环境。

# 文件夹内现券交易数据完整
input_path = '/Users/wdt/Desktop/tpy/raw_data_pool'

def organize(df):
    ''' 整理数据 '''
    df["Unnamed: 0"].fillna(method="ffill",inplace=True)#填充机构名字
    #df["date"]=pd.to_datetime(df["date"],format="%Y-%m-%d")#整理格式
    columns_names=[]
    for j in range(len(df.columns)):#去掉换行和英文
        columns_name = re.match(".*",df.columns[j]).group()
        columns_names.append(columns_name)
    df.columns = columns_names

    investors = []
    durations = []
    for i in range(len(df)):#去掉换行和英文
        investor = re.match(".*",df["Unnamed: 0"][i]).group()
        investors.append(investor)
        duration = re.match(".*",df["期限"][i]).group()
        durations.append(duration)
    df["Unnamed: 0"]=investors
    df["期限"]=durations

    return df

def upload_date_list():
    '''
    输出一个待更新日期的列表
    最后依照此列表逐个上传
    '''
    dir_date=[]
    df = pd.read_sql('select * from Net_buy_bond' , conn)
    last_date = df.iloc[-1 , -1]

    for dir in os.listdir(input_path+"/现券市场交易情况总结/日报"):
        if '现券' not in dir:
            continue
        attach_time = re.match(".*\\d{8}\\.",dir).group()[-9:-1]
        attach_datetime = pd.to_datetime(attach_time)
        if attach_datetime > end_data:
            dir_date.append(attach_datetime.strftime("%Y%m%d"))
        else:
            pass

    return dir_date

def daily_Net_buy_bond(date):#每天数据的转换
    """
    现券市场净买入数据
    文件是从邮件内自动下载好的
    需要匹配一个最新日期*
    """
    excel_io= input_path+"/现券市场交易情况总结/日报/"+"现券市场交易情况总结日报_"+date+".xls"
    sheet_name = "机构净买入债券成交金额统计表_" + date#读取sheet路径
    df = pd.read_excel(excel_io, header=4, sheet_name=sheet_name,nrows = 120)#
    df["date"]=date # 加盖时间戳
    df = organize(df)
    df.rename(columns={'Unnamed: 0':'机构名称'},inplace=True)
    df.reset_index(drop=True) 
    df=df.replace("—",0)

    name = "Net_buy_bond"
    columns_type=[#图表的数据口径
    String(30),
    String(30),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    DateTime(),
    String(30)]
    dtypelist = dict(zip(df.columns,columns_type))
    return df,name,dtypelist

def daily_Repo_price_for_investors(date):   
    """
    From质押式回购市场交易情况总结日报
    正/逆回购方-利率
    """ 
    # excel_io= input_path+"/质押式回购市场交易情况总结/日报/"+"质押式回购市场交易情况总结日报_"+date+".xls"#读取excel路径
    excel_io = test_path + '/质押式回购市场交易情况总结日报_' + date + '.xls'
    df=pd.read_excel(excel_io,header=1,nrows = 5).iloc[:,1:7]
    df.columns.name="正回购方"
    df.rename(columns={'Unnamed: 1':'机构名称'},inplace=True)
    df["date"]=date
    df.reset_index(drop=True) 
    df=df.replace("—",0)
    name = "Repo_price_for_investors" # 为了对应数据库table名字
    columns_type=[#图表的数据口径
    String(30),
    Float(),
    Float(),
    Float(),
    Float(),
    Float(),
    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))#变成字典形式
    return df,name,dtypelist

def daily_Repo_amt_prc_for_terms(date):
    """
    机构类型-期限品种 —— 正逆回购利率/金额？
    """
    #excel_io= input_path+"\\"+"质押式回购市场交易情况总结日报_"+date+".xls"#读取excel路径
    excel_io = test_path + '/质押式回购市场交易情况总结日报_' + date + '.xls'
    df = pd.read_excel(excel_io,header=8,nrows = 99)
    df["date"]=date
    df["机构类型"].fillna(method="ffill",inplace=True)
    df.reset_index(drop=True) 
    df=df.replace("-",0)
    name = "Repo_amt_prc_for_terms"
    columns_type=[#图表的数据口径
    String(30),
    String(30),
    Float(2),
    Float(2),
    Float(2),
    Float(2),
    Float(2),
    Float(2),
    Float(2),
    Float(2),
    Float(2),
    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))#变成字典形式
    return df,name,dtypelist

def daily_Repo_amt_prc_for_collateral(date):
    """
    机构类型-债券类型 —— 
    """
    #excel_io= input_path+"\\"+"质押式回购市场交易情况总结日报_"+date+".xls"#读取excel路径
    excel_io = test_path + '/质押式回购市场交易情况总结日报_' + date + '.xls'
    df=pd.read_excel(excel_io,header=110,nrows =27).iloc[:,:6]
    df["date"]=date
    df["机构类型"].fillna(method="ffill",inplace=True)
    df.rename(columns={'债券类型':'抵押品类型'},inplace=True) 
    name = "Repo_amt_prc_for_collateral"
    columns_type=[#图表的数据口径
    String(30),
    String(30),
    Float(4),
    Float(2),
    Float(4),
    Float(2),
    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))#变成字典形式       
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

    # * 读取db.txt内的邮箱信息
    db_path = "/Users/wdt/Desktop/tpy/db.txt"
    conn , engine = get_db_conn(db_path)

    for date in upload_date_list():
        # engine = create_engine('mysql+pymysql://dngj:603603@47.116.3.109:3306/finance?charset=utf8')
        l = [daily_Net_buy_bond(date)]
        for a,b,c in l:
            a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print("成功上传"+date+"的本地数据")
#main()