import re
import sys
import datetime as dt
import pandas as pd
import numpy as np
import  pymysql
from sqlalchemy import create_engine
from WindPy import w


def upload_data(df,name,method="append"):
    df= df
    name = name
    method = method
    engine = create_engine('mysql+pymysql://dngj:603603@47.116.3.109:3306/finance?charset=utf8mb4')
    df.to_sql(name=name,con = engine,schema='finance',if_exists = method ,index=False)
    print("您已经成功上传"+name)
    return 

# 设定需要上传的时间段
def get_upload_timerange(table_name):
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
    
    if type(dff["date"])!=np.datetime64:
        dff["date"]=pd.to_datetime(dff["date"])
    else:
        pass
    exist_date=dff.sort_values("date",ascending=False).head(1)["date"].values[0]
    start_date=dff.sort_values("date",ascending=True).head(1)["date"].values[0]
    conn.close()
    return start_date,exist_date

def get_data(table_name,how="transed"):
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
    
    if how == "transed":
        dff.columns=["date"]+trans_index(dff.columns[1:])
        conn.close()
        return dff

    elif how == "raw":
        conn.close()
        return dff
    
    else:
        conn.close()
        pass 


def data_time_tange(dff):
    if type(dff["date"])!=np.datetime64:
        dff["date"]=pd.to_datetime(dff["date"])
    else:
        pass
    exist_date=dff.sort_values("date",ascending=False).head(1)["date"].values[0]
    start_date=dff.sort_values("date",ascending=True).head(1)["date"].values[0]
    
    return start_date,exist_date



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

def quantile(column, quantile=5):
    q = pd.qcut(column, quantile)
    return len(q.levels)- q.labels

def drop_noisy_cut_tail(df):
    df_copy = df.copy()
    df_describe = df_copy.describe()
    
    for column in df.columns:
        mean = df_describe.loc['mean',column]
        std = df_describe.loc['std',column]
        minvalue = mean - 3*std
        maxvalue = mean + 3*std
        df_copy = df_copy[df_copy[column] >= minvalue]
        df_copy = df_copy[df_copy[column] <= maxvalue]
    return df_copy


def trans_index(list,how="c2n"):
    conn = pymysql.connect(
    host = '47.116.3.109',	
    user = 'dngj',	
    passwd = '603603',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8mb4'	
)
    excu="select * from "
    table_name="指标字典"
    d = pd.read_sql(excu+table_name,conn)
    if how=="c2n":
        index_name=[]
        for x in list:
            index_name.append(d[d["指标ID"]==x]["指标名称"].values[0])

        word="成功转换指标代码"
    elif how=="n2c":
        index_name=[]
        for x in list:
            index_name.append(d[d["指标名称"]==x]["指标ID"].values[0])
        word="成功转换指标名称"
    else:
        index_name=0
        word="转换失败" 
    
    print(word)
    return index_name

def refresh_data(table_name):
    w.start()
    today=dt.datetime.today()
    data = get_data(table_name,how="raw")
    start_date,exist_date=data_time_tange(data)
    exist_date=pd.to_datetime(exist_date)
    #需要保证原始数据库的表头为wind代码
    index_code_list= "'"+",".join(data.columns[1:].tolist())+"'"
    err,df= w.edb(index_code_list,exist_date,today,usedf=True)
    df.reset_index(inplace=True)
    df.rename(columns={'index':'date'},inplace=True)
    upload_data(df,table_name)
    print("您已经成功刷新数据")
    return 