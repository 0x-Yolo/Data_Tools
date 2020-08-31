import re
import sys
import datetime as dt
import pandas as pd
import numpy as np
import  pymysql
from sqlalchemy import create_engine


def upload_data(df,name,method="append"):
    df= df
    name = name
    method = method
    engine = create_engine('mysql+pymysql://dngj:603603@47.116.3.109:3306/finance?charset=utf8mb4')
    df.to_sql(name=name,con = engine,schema='finance',if_exists = method ,index=False)
    return 

# 设定需要上传的时间段
def get_un_upload_timerange(table_name):
    conn = pymysql.connect(
    host = '47.116.3.109',	
    user = 'dngj',	
    passwd = '603603',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8mb4'	
)
    excu="select * from "
    table_name=table_name
    dff = pd.read_sql(excu+table_name,conn)
    t=dff.sort_values("date",ascending=False).head(1)["date"].values[0]
    start_time=np.datetime_as_string(t, unit='D')
    rpt_date=dt.datetime.now().strftime('%Y-%m-%d')#设定报告期，读取报告写作日时间
    conn.close()
    return start_time,rpt_date

def get_data(table_name):
    conn = pymysql.connect(
    host = '47.116.3.109',	
    user = 'dngj',	
    passwd = '603603',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8mb4'	
)
    excu="select * from "
    table_name=table_name
    dff = pd.read_sql(excu+table_name,conn)
    return dff


def get_all_table_name():
    # 获取数据库所有表名
    conn = pymysql.connect(
        host = '47.116.3.109',	#你的数据库ip
        user = 'dngj',	#你的用户名
        passwd = '603603',	#你的密码
        db = 'finance',	#你的database名称
        port=3306,	
        charset = 'utf8'	
    )
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

