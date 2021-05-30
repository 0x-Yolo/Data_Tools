import pandas as pd
import data_organize as do
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime

df = pd.read_excel('./cd.xlsx')
name = 'interbank_dps_vol_weekly'
data = do.get_data(name)

dff = df[['截止日期','总发行量(亿元)', '总偿还量(亿元)', '净融资额(亿元)']]
dff.columns = data.columns
dff

d = dff.iloc[:-2,:].append(\
    data.iloc[3:,:]\
        )

columns_type=[DateTime(),Float(),Float(),Float()]
dtypelist = dict(zip(d.columns,columns_type))

conn,engine = do.get_db_conn()
for a,b,c in [(d,name,dtypelist)]:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'replace',index=False,dtype=c)
    print(b, '写入完成')
