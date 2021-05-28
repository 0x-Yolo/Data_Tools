import pymysql
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import pandas as pd
import numpy as np
import datetime as dt#准备工作，配置环境。
import seaborn as sns
import matplotlib.pyplot as ax
import matplotlib.ticker as ticker
import datetime

co_list = ['政策性银行', '全国性商业银行', '城市商业银行', '农商行及农合行', '外资银行', '其他银行', '证券公司', '保险公司',
    '境外机构', '信用社', '其他', '广义基金']
bond_list = ['国债','政金债','地方债','企业债','中票','短融','超短融','PPN','商业银行债','同业存单','合计']
def upload_date(name):
    """
    输入表名
    输出该表的最新日期
    """
    
    dir_date = []
    df = pd.read_sql('select max(date) from {}'.format(name) , conn)
    last_date = df.iloc[-1 , -1]
    
    return last_date 
def df_pre(df):
    df = df.iloc[1:-2,:]
    c = list(df.columns)
    for i in range(2, len(c) , 2):
        c[i] = c[i-1] + '_增加' 
        c[i-1] = c[i-1] + '_月末'
    c[0] = '投资者结构'
    df.columns = c
    return df

def sum_row_SQ(test):
    # 上清
    dff = pd.DataFrame([], columns=test.columns, index = co_list)
    dff.loc['政策性银行'] = test.loc[1]
    dff.loc['全国性商业银行'] = test.loc[4]+test.loc[3]
    dff.loc['城市商业银行'] = test.loc[5]
    dff.loc['农商行及农合行'] = test.loc[6]
    dff.loc['外资银行'] = test.loc[9]
    dff.loc['其他银行'] = test.loc[7]+test.loc[8]

    dff.loc['证券公司'] = test.loc[11]
    dff.loc['保险公司'] = test.loc[12]
    dff.loc['境外机构'] = test.loc[17]
    dff.loc['信用社'] = test.loc[10]

    dff.loc['其他'] = test.loc[14] + test.loc[15] 

    dff.loc['广义基金'] = test.loc[13] + test.loc[16] 

    dff['投资者结构'] = dff.index
    dff = dff.reset_index(drop =True)
    return dff

def sum_col_SQ(test):

    tail1 = '（亿元）_月末';tail2 = '（亿元）_增加'

    dff = pd.DataFrame([],index=co_list,columns=bond_list )
    dff['国债'] = 0;dff['政金债']=0;dff['地方债']=0
    dff['企业债'] = 0# + test['其他公司信用类债券'+tail1].tolist()
    dff['中票'] = test['中期票据'+tail1].tolist()
    dff['短融'] = test['短期融资券'+tail1].tolist()
    dff['超短融'] = test['超短期融资券'+tail1].tolist()
    dff['PPN'] = test['非公开定向债务融资工具'+tail1].tolist()
    dff['商业银行债'] = test['金融债券'+tail1].tolist()
    dff['同业存单'] = test['同业存单'+tail1].tolist()
    dff['合计'] = test[[x for x in test.columns if tail1 in x]].sum(axis=1).tolist()

    dff['国债_hb'] = 0;dff['政金债_hb']=0;dff['地方债_hb']=0
    dff['企业债_hb'] = 0;#test['其他公司信用类债券'+tail2].tolist()
    dff['中票_hb'] = test['中期票据'+tail2].tolist()
    dff['短融_hb'] = test['短期融资券'+tail2].tolist()
    dff['超短融_hb'] = test['超短期融资券'+tail2].tolist()
    dff['PPN_hb'] = test['非公开定向债务融资工具'+tail2].tolist()
    dff['商业银行债_hb'] = test['金融债券'+tail2].tolist()
    dff['同业存单_hb'] = test['同业存单'+tail2].tolist()
    dff['合计_hb'] = test[[x for x in test.columns if tail2 in x]].sum(axis=1).tolist()


    return dff

def sum_row_ZZ(test):
    # 中债
    dff = pd.DataFrame([], columns=test.columns, index = co_list)
    dff.loc['政策性银行'] = test.loc[2]
    dff.loc['全国性商业银行'] = test.loc[4] # +test.loc[3]
    dff.loc['城市商业银行'] = test.loc[5]
    dff.loc['农商行及农合行'] = test.loc[6]+test.loc[7]
    dff.loc['外资银行'] = test.loc[9]
    dff.loc['其他银行'] = test.loc[8]+test.loc[10]

    dff.loc['证券公司'] = test.loc[13]
    dff.loc['保险公司'] = test.loc[12]
    dff.loc['境外机构'] = test.loc[19]
    dff.loc['信用社'] = test.loc[11]

    dff.loc['其他'] = test.loc[15] + test.loc[16] 

    dff.loc['广义基金'] = test.loc[14] + test.loc[17] 

    dff['投资者结构'] = dff.index
    dff = dff.reset_index(drop =True)
    return dff

def sum_col_ZZ(test):
    # 中债
    tail1 = '_月末';tail2 = '_增加'

    dff = pd.DataFrame([],index=co_list,columns=bond_list )
    dff['国债'] = test['国债'+tail1].tolist()
    dff['政金债'] = test[['国家开发银行'+tail1,'中国进出口银行'+tail1,'中国农业发展银行'+tail1]].sum(axis=1).tolist()
    dff['地方债'] = test['地方政府债'+tail1].tolist()
    dff['企业债'] = test['企业债'+tail1].tolist()
    dff['中票'] = test['中期票据'+tail1].tolist()
    dff['短融'] = 0
    dff['超短融'] = 0 
    dff['PPN'] = 0
    dff['商业银行债'] = test[['次级债'+tail1,'普通债'+tail1,'混合资本债'+tail1,'二级资本工具'+tail1]].sum(axis=1).tolist()
    dff['同业存单'] = 0
    dff['合计'] = test['合计'+tail1].tolist()

    dff['国债_hb'] = test['国债'+tail2].tolist()
    dff['政金债_hb'] = test[['国家开发银行'+tail2,'中国进出口银行'+tail2,'中国农业发展银行'+tail2]].sum(axis=1).tolist()
    dff['地方债_hb'] = test['地方政府债'+tail2].tolist()
    dff['企业债_hb'] = test['企业债'+tail2].tolist()
    dff['中票_hb'] = test['中期票据'+tail2].tolist()
    dff['短融_hb'] = 0
    dff['超短融_hb'] = 0 
    dff['PPN_hb'] = 0
    dff['商业银行债_hb'] = test[['次级债'+tail2,'普通债'+tail2,'混合资本债'+tail2,'二级资本工具'+tail2]].sum(axis=1).tolist()
    dff['同业存单_hb'] = 0
    dff['合计_hb'] = test['合计'+tail2].tolist()

    return dff


def get_data():
    """
    输出分机构类型托管数据/上清托管数据/中债托管数据
    """
    path = '/Users/wdt/Desktop/tpy/mycode/【机构行为】/raw_data/P2-托管量'
    name = 'bond_depository'
    ## 上清/中债数据行列合并
    d_sq = pd.DataFrame([])
    d_zz = pd.DataFrame([])
    
    # 读取本地数据
    for dir in os.listdir(path):
        if '~' in dir:
            continue

        month = int(re.findall(r'\d+', dir)[0])
        if month < upload_date(name):
            continue

        if '上清' in dir:
            d = pd.read_excel(path+'/'+dir)
            d = df_pre(d)#预处理，列名的调整
            if d.shape[1] > 20:
                d['其他债券（亿元）_月末']=d['资产支持证券（亿元）_月末']+d['标准化票据（亿元）_月末']
                d['其他债券（亿元）_增加']=d['资产支持证券（亿元）_增加']+d['标准化票据（亿元）_增加']
            
            d = sum_row_SQ(d)
            d = sum_col_SQ(d)

            d['date'] = month
            d_sq = d_sq.append(d)

        elif '中债' in dir:
            d = pd.read_excel(path+'/'+dir)
            d = df_pre(d)

            d = sum_row_ZZ(d)
            d = sum_col_ZZ(d)

            d['date'] = month
            d_zz = d_zz.append(d)
    
    ## 上清/中债数据加合
    data = pd.DataFrame([])
    month_list = d_zz.date.unique()
    month_list.sort()
    for month in month_list:
        arr = np.array(d_zz.loc[d_zz.date == month].iloc[:,:-1]) + \
        np.array(d_sq[d_sq.date == month].iloc[:,:-1])
        d_date = pd.DataFrame(arr,columns = d_zz.columns[:-1],index=d_zz.index.unique())
        d_date['date'] = month
        data = data.append(d_date)

    data['投资者结构'] = data.index
    d_zz['投资者结构'] = d_zz.index
    d_sq['投资者结构'] = d_sq.index

    data = data[['投资者结构','国债', '政金债', '地方债', '企业债', '中票', '短融', '超短融', 'PPN', '商业银行债', '同业存单',
       '合计', '国债_hb', '政金债_hb', '地方债_hb', '企业债_hb', '中票_hb', '短融_hb', '超短融_hb',
       'PPN_hb', '商业银行债_hb', '同业存单_hb', '合计_hb', 'date']]

    return data ,d_sq, d_zz

# * 导入新一期的数据

def monthly_bond_depository():
    name = 'bond_depository'
    df,d_sq,d_zz = get_data()

    columns_type=[VARCHAR(30),Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),
                  Integer()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df,name,dtypelist

l=[monthly_bond_depository()]
for a,b,c in l:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)

