import re
import sys
import datetime as dt
import pandas as pd
import numpy as np
import  pymysql
from sqlalchemy import create_engine
path = input('输入存放数据库信息的地址')
# path = '/Users/wdt/db.txt'

# path = "/Users/wdt/Desktop/tpy/db.txt"
# get_db_conn('/Users/wdt/Desktop/tpy/test01.txt')

def get_db_conn(io = path):
    '''
    path:::存有数据库账号信息的txt
    '''
    
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

def upload_data(df,name,method="append"):
    """输入要上传的df/表名/方法"""
    df= df
    name = name
    method = method

    conn, engine = get_db_conn(path)

    df.to_sql(name=name,con = engine,schema='finance',if_exists = method ,index=False)
    return 

# 设定需要上传的时间段
def get_un_upload_timerange(table_name):
    conn, engine = get_db_conn(path)

    excu="select * from "
    table_name=table_name
    dff = pd.read_sql(excu+table_name,conn)
    t=dff.sort_values("date",ascending=False).head(1)["date"].values[0]
    start_time=np.datetime_as_string(t, unit='D')
    rpt_date=dt.datetime.now().strftime('%Y-%m-%d')#设定报告期，读取报告写作日时间
    conn.close()
    return start_time,rpt_date

def get_data(table_name, start=0 ,end =0):
    """获取表名"""
    conn, engine = get_db_conn(path)
    excu="select * from "
    table_name=table_name

    excu_date = " where date >= '{}' and date <= '{}';".format(start , end)
    if start == 0:
        excu_date = ''
    dff = pd.read_sql(excu+table_name+excu_date,conn)
    return dff

def get_all_table_name():
    # 获取数据库所有表名
    conn, engine = get_db_conn(path)

    cursor = conn.cursor()
    cursor.execute('select table_name from information_schema.tables where table_schema="finance" ')
    A = cursor.fetchall()
    return A

def set_data_index(df):
    df.index=df["date"]
    return df


# for table_name in refresh_table_list:
#     start_time,rpt_date=get_un_upload_timerange(table_name)
#     df=read_data_from_wind(wind_code,start_time,rpt_date)
#     upload_data(df,table_name,"append")

def daily_uplpad_table_names():
    df=get_data("resoure_table")
    daily_uplpad_table_names=df[df["daily_upload_by_wind"]==1]["table_name"].tolist()
    return daily_uplpad_table_names

def get_latest_date(table_name):
    conn, engine = get_db_conn(path)
    excu="select max(date) from "
    table_name=table_name
    return pd.read_sql(excu+table_name ,conn).iloc[-1,-1]

