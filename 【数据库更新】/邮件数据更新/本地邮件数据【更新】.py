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
import data_organize as do
# 文件夹内现券交易数据完整

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

def upload_date_list(name):
    '''
    输出一个待更新日期的列表
    最后依照此列表逐个上传
    '''
    dir_names=[]
    latest_date = do.get_latest_date(name)

    if name == 'Net_buy_bond':
        path = input_path+"/现券市场交易情况总结/日报"
    elif 'Repo' in name :
        path = input_path+'/质押式回购市场交易情况总结/日报'

    for dir in os.listdir(path ):
        if 'DS' in dir or 'xlsx' in dir :
            continue 
        # print(dir)
        attach_time = re.match(".*\\d{8}\\.",dir).group()[-9:-1]
        attach_datetime = pd.to_datetime(attach_time)
        if attach_datetime > latest_date:
            dir_names.append(dir)
        else:
            pass
    return dir_names

def daily_Net_buy_bond(dir_name):#每天数据的转换
    """
    现券市场净买入数据
    文件是从邮件内自动下载好的
    需要匹配一个最新日期*
    """
    date = re.match(".*\\d{8}\\.",dir_name).group()[-9:-1]
    excel_io= input_path+"/现券市场交易情况总结/日报/" + dir_name
    sheet_name = "机构净买入债券成交金额统计表_" + date#读取sheet路径
    df = pd.read_excel(excel_io, header=4, sheet_name=sheet_name,nrows = 120)#
    df["date"]=date # 加盖时间戳
    df = organize(df)
    df.rename(columns={'Unnamed: 0':'机构名称'},inplace=True)
    df = df.reset_index(drop=True) 
    df=df.replace("—",0)
    df=df.replace('---',0)

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

def daily_Repo_price_for_investors(dir_name):   
    """
    From质押式回购市场交易情况总结日报
    正/逆回购方-利率
    """ 
    date = re.match(".*\\d{8}\\.",dir_name).group()[-9:-1]
    excel_io= input_path+"/质押式回购市场交易情况总结/日报/" + dir_name

    df=pd.read_excel(excel_io,header=1,nrows = 5).iloc[:,1:7]
    df.columns.name="正回购方"
    df.rename(columns={'Unnamed: 1':'机构名称'},inplace=True)
    df["date"]=date
    df.reset_index(drop=True) 
    df=df.replace('-',0)
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

def daily_Repo_amt_prc_for_terms(dir_name):
    """
    机构类型-期限品种 —— 正逆回购利率/金额？
    """    
    date = re.match(".*\\d{8}\\.",dir_name).group()[-9:-1]
    excel_io= input_path+"/质押式回购市场交易情况总结/日报/" + dir_name
    
    tmp = pd.read_excel(excel_io)
    # print(tmp.shape,date)
    if tmp.shape[0] == 206:
        h =8; nr = 121
    elif tmp.shape[0] == 178:
        h = 8; nr = 99

    df = pd.read_excel(excel_io,header=h,nrows = nr)
    # print(df.shape)
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

def daily_Repo_amt_prc_for_collateral(dir_name):
    """
    机构类型-债券类型 —— 
    """
    date = re.match(".*\\d{8}\\.",dir_name).group()[-9:-1]
    excel_io= input_path+"/质押式回购市场交易情况总结/日报/" + dir_name
    
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
    df=df.replace("-",0)
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

def main():
    input_path = '/Users/wdt/Desktop/tpy/raw_data_pool'

    # * 读取db.txt内的数据库信息
    conn,engine = do.get_db_conn()
    dir_list = upload_date_list('Net_buy_bond')
    dir_list.sort()
    for dir in dir_list:
        if 'xlsx' in dir :
            print(dir)# 0522.xlsx
            continue
        l = [daily_Net_buy_bond(dir)]
        for a,b,c in l:
            a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print("成功上传"+dir+"的本地数据")

    dir_list = upload_date_list('Repo_price_for_investors')
    dir_list.sort()
    for dir in dir_list:
        if 'xlsx' in dir :
            print(dir)# 0522.xlsx
            continue
        l = [
            daily_Repo_price_for_investors(dir), 
            daily_Repo_amt_prc_for_terms(dir),
            daily_Repo_amt_prc_for_collateral(dir),
            ]
        for a,b,c in l:
            a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print("成功上传"+dir+"的本地数据")
