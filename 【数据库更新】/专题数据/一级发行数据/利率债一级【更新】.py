import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pymysql
from sqlalchemy.types import String, Float, Integer, VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do

cols = ['证券代码', '交易代码', '债券简称', '发行起始日', '缴款日', '发行规模(亿)', '发行期限(年)', '特殊期限',
       '发行人全称', '加权利率', '全场倍数', '边际利率', '边际倍数', '久期', '中债估值', '综收', '二级成交价',
       '综收较估值', '综收较二级']

## * 更新
def pmy_rate_sec():
    name = 'primary_rate_sec'
    last_date = do.get_latest_date(name)
    df = pd.read_excel('/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/专题数据/一级发行数据/利率债一级_新.xlsx',\
    sheet_name = '数据（导入）')
    df = df[cols]
    df['date'] = df['发行起始日']
    df = df.loc[df.date>last_date]

    columns_type=[VARCHAR(30),VARCHAR(30),VARCHAR(30),DateTime(),DateTime(),
                Float(),Float(),VARCHAR(30),VARCHAR(30),
                Float(),Float(),Float(),Float(),Float(),Float(),
                Float(),Float(),Float(),Float(),
                DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    return df, name , dtypelist

l = [pmy_rate_sec()]
for a,b,c in l:
    do.upload_data(a,b,c, method='append')



