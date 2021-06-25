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
# from do4myself import data_organize as do

input_path = '/Users/wdt/Desktop/tpy/raw_data_pool'
# test_path = '/Users/wdt/Desktop/tpy/raw_data_pool/download data'


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


Net_buy_bond = pd.DataFrame()
def get_Net_buy_bond(input_path):#每天数据的转换
    """
    现券市场交易日报
    """
    global Net_buy_bond
    #excel_io= input_path+"/现券市场交易情况总结/日报/"+"现券市场交易情况总结日报_"+date+".xls"
    path = input_path+"/现券市场交易情况总结/日报"
    # 读取path下所有的文件名，并从按日期远到近排序
    dir_list = os.listdir(path)
    dir_list.sort()

    for dir in dir_list:
        if 'DS' in dir:# 跳过系统内的DS_store 
            continue
        excel_io = path + '/' + dir
        date = re.match(".*\d{8}\.",dir).group()[-9:-1] # 获取文件名中的date
        sheet_name = "机构净买入债券成交金额统计表_"+re.match(".*\d{8}\.",dir).group()[-9:-1]#读取sheet路径
        df = pd.read_excel(excel_io, header=4, sheet_name=sheet_name,nrows = 120)#
        df["date"] = date # 加盖时间戳
        df = organize(df)
        df=df.replace("—",0)
        Net_buy_bond = Net_buy_bond.append(df)

    Net_buy_bond.columns.name
    Net_buy_bond.rename(columns={'Unnamed: 0':'机构名称'},inplace=True)
    Net_buy_bond.reset_index(drop=True) 
    return Net_buy_bond
Net_buy_bond = get_Net_buy_bond(input_path)


Repo_price_for_investors = pd.DataFrame()
def get_Repo_price_for_investors(input_path):#每天数据的        
    """
    From质押式回购市场交易情况总结日报
    正/逆回购方-利率
    """ 
    path = input_path + '/质押式回购市场交易情况总结/日报'
    global Repo_price_for_investors
    for dir in os.listdir(path):
        if '质押式' not in dir:
            continue
        excel_io = path + '/' + dir
        date = re.match(".*\d{8}\.",dir).group()[-9:-1]
        df=pd.read_excel(excel_io,header=1,nrows = 5).iloc[:,1:7]
        df.columns.name="正回购方"
        df["date"]=date
        df=df.replace("—",0)
        Repo_price_for_investors = Repo_price_for_investors.append(df)
    Repo_price_for_investors.reset_index(drop=True) 
    Repo_price_for_investors.rename(columns={'Unnamed: 1':'机构名称'},inplace=True)
    return Repo_price_for_investors
# Repo_price_for_investors = get_Repo_price_for_investors(test_path)


Repo_amt_prc_for_terms = pd.DataFrame()
def get_Repo_amt_prc_for_terms(input_path):
    """
    机构类型-期限品种 —— 正逆回购利率/金额？
    """
    path = input_path + '/质押式回购市场交易情况总结/日报'
    global Repo_amt_prc_for_terms
    for dir in os.listdir(path):
        if '质押式' not in dir:
            continue
        excel_io = path + '/' + dir
        date = re.match(".*\d{8}\.",dir).group()[-9:-1]

        tmp = pd.read_excel(excel_io)
        # print(tmp.shape,date)
        if tmp.shape[0] == 206:
            h =8; nr = 121
        elif tmp.shape[0] == 178:
            h = 8; nr = 99

        df = pd.read_excel(excel_io,header=h,nrows = 121)
        df["date"]=date
        df["机构类型"].fillna(method="ffill",inplace=True)
        df=df.replace("-",0)
        Repo_amt_prc_for_terms = Repo_amt_prc_for_terms.append(df)
    Repo_amt_prc_for_terms.reset_index(drop=True)
    Repo_amt_prc_for_terms = Repo_amt_prc_for_terms.replace("-",0)
    return Repo_amt_prc_for_terms
Repo_amt_prc_for_terms = get_Repo_amt_prc_for_terms(test_path)


Repo_amt_prc_for_collateral = pd.DataFrame()
def get_Repo_amt_prc_for_collateral(input_path):
    """
    机构类型-债券类型 —— 
    """
    path = input_path + '/质押式回购市场交易情况总结/日报'
    global Repo_amt_prc_for_collateral
    for dir in os.listdir(path):
        if '质押式' not in dir:
            continue
        excel_io = path + '/' + dir
        date = re.match(".*\d{8}\.",dir).group()[-9:-1]

        tmp = pd.read_excel(excel_io)
        # print(tmp.shape,date)
        if tmp.shape[0] == 206:
            h = 132; nr = 33
        elif tmp.shape[0] == 178:
            h = 110; nr = 27

        df=pd.read_excel(excel_io,header=h,nrows =nr).iloc[:,:6]
        df["date"]=date
        df["机构类型"].fillna(method="ffill",inplace=True)
        df.rename(columns={'债券类型':'抵押品类型'},inplace=True) 
        Repo_amt_prc_for_collateral = Repo_amt_prc_for_collateral.append(df)
    Repo_amt_prc_for_collateral.reset_index(drop=True)
    Repo_amt_prc_for_collateral = Repo_amt_prc_for_collateral.replace("-",0)    
    return Repo_amt_prc_for_collateral
Repo_amt_prc_for_collateral = get_Repo_amt_prc_for_collateral(test_path)

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

db_path = "/Users/wdt/Desktop/tpy/db.txt"
conn , engine = get_db_conn(db_path)

## * 将现券交易净买入数据上传数据库
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
dtypelist = dict(zip(Net_buy_bond.columns,columns_type))

Net_buy_bond.to_sql(name=name,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=dtypelist)
