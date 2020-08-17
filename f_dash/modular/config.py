# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

import datetime as dt
import pandas as pd
import  pymysql
import json


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
def get_geo_data():
    json_io=r"f_dash\modular\geojson-map-china\china.json"
    gs_data = open(json_io, encoding='utf8').read()
    gs_data = json.loads(gs_data)
    # 整理plotly需要的格式：
    for i in range(len(gs_data["features"])):
        gs_data["features"][i]["id"]=gs_data["features"][i]["properties"]["id"]#id前置
        gs_data["features"][i]["name"]=gs_data["features"][i]["properties"]["name"]
    # 匹配id和区域
    geo_id=[]
    geo_name=[]
    for i in range(len(gs_data["features"])):
        geo_id.append(gs_data["features"][i]["id"])
        geo_name.append(gs_data["features"][i]['properties']["name"])
    geo_data=pd.DataFrame({"id":geo_id,"区域":geo_name})
    return geo_data,gs_data

# %%
def get_ir_diff():
    conn = pymysql.connect(
        host = '47.116.3.109',	
        user = 'dngj',	
        passwd = '603603',	
        db = 'finance',	
        port=3306,	
        charset = 'utf8mb4'	
        )
    # 城投债数据
    data=pd.read_sql('select * from Credit_Premium',conn)
    # 基准利率数据
    sql_cmd = 'SELECT * FROM interest_rate_day ORDER BY interest_rate_day.index desc LIMIT 1'
    ir = pd.read_sql(sql_cmd,conn)
    conn.close()
    # 城投债数据筛选非PPN
    data = data[data["证券简称"].str.contains("PPN")==False]
    columns_to_use = ['证券代码', '证券简称', '主体名称', '是否城投债',
                      '上市日期', '债券余额\n[日期] 最新\n[单位] 亿',
                      '剩余期限(天)\n[日期] 最新\n[单位] 天',
                      '估价收益率(%)(中债)\n[日期] 最新收盘日\n[估值类型] 推荐',
                      '含权债行权期限', '债券估值(YY)\n[单位] %', 
                      '是否次级债', '区域', '城市', '是否存在担保']
    df = data[columns_to_use]
    # 确定城投债的可比期限
    df.loc[:,"含权债行权期限"]=df.loc[:,"含权债行权期限"].fillna(10)*365
    df.loc[:,"期限"]=((df[["含权债行权期限","剩余期限(天)\n[日期] 最新\n[单位] 天"]].min(axis=1))/365).round(2)
    df.loc[:,"期限_匹配"]=((df[["含权债行权期限","剩余期限(天)\n[日期] 最新\n[单位] 天"]].min(axis=1))/365).round(0)
    # 选择国开利率作为基准利率
    GK_yield_base = ir[['中债国开债到期收益率:1年','中债国开债到期收益率:2年','中债国开债到期收益率:3年','中债国开债到期收益率:4年','中债国开债到期收益率:5年']].T
    GK_yield_base.columns=["GK_yield"]
    GK_yield_base["期限"]=[1,2,3,4,5]
    GK_yield_base = GK_yield_base.reset_index(drop = True)
    # 合并城投债数据和基准利率
    dff_VS_GK=pd.merge(df[df["期限"]<5],GK_yield_base,left_on=["期限_匹配"],right_on=["期限"],how="left")
    # 计算利差
    dff_VS_GK["券种利差"]=(dff_VS_GK["债券估值(YY)\n[单位] %"]-dff_VS_GK["GK_yield"])*100
    dff_VS_GK=dff_VS_GK[dff_VS_GK["券种利差"].isna()==False]
    return dff_VS_GK
    
# %%
def get_xyct():  
    geo_data = get_geo_data()[0]
    xyct = pd.read_excel('modular/信用利差(中位数)城投债不同省份.xls',index_col = 'date',encoding = 'gbk')
    xyct.columns = [i[2] for i in xyct.columns.str.split(":")]
    # 将省份名称和地图数据对应
    province = []
    for i in range(xyct.shape[1]):
        for j in geo_data['区域']:
            if xyct.columns[i] in j:
                province.append(j)
    xyct.columns = province
    return xyct

