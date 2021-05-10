import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re

# 数据导入和合并
data = pd.read_excel('test.xlsx' ,sheet_name='信用债成交',header=1)
data['时间'] = dt.date(2021,4,30)
# 合并

# 提取原数据主键
df = data[['代码', '价格', '时间']]
df['估值时间'] = data['时间'] -1

## * windapi的列
# 名字、到期估值、行权估值、行权日、price、type、估值偏离、剩余期限、
# rating、永续、城投、行业、发行人、企业性质、隐含评级
df['名字']

w.wsd("122660.SH,1080092.IB", "yield_cnbd", "2021-04-06", "2021-05-05", "credibility=1")

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