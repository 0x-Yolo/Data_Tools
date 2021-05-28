import pandas as pd

df = pd.read_csv()
name = 'interbank_dps'

columns_type=[Float(),Float(),Float(),\
    Float(),Float()]
dtypelist = dict(zip(df.columns,columns_type))


for a,b,c in [rates()]:
    a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
    print(b, '写入完成')
