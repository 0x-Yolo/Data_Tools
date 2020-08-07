# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

import datetime as dt
import pandas as pd
import  pymysql


# %%
class Inter_Graph: 
    
    #定义基本属性 
    conn = pymysql.connect(
        host = '47.116.3.109',	
        user = 'user1',	
        passwd = '123456',	
        db = 'finance',	
        port=3306,	
        charset = 'utf8'	
    )
    df = pd.read_sql('select * from Net_buy_bond',conn)
    bond_type_OL = df.columns[3:-1].tolist()
    bond_duration_OL = df["期限"].unique().tolist()
    bond_buyer_OL = df["机构名称"].unique().tolist()[:-1]
    
    dff = pd.read_sql('select * from Repo_amt_prc_for_terms',conn)
    repo_terms_OL = dff["期限品种"].unique().tolist()
    repo_loaner_OL = dff["机构类型"].unique().tolist()


# %%


