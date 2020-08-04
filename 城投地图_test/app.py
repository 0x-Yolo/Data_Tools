# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:19:47 2020

@author: User
"""

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import json

server = flask.Flask(__name__) 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,server=server,external_stylesheets=external_stylesheets)

json_io=r"城投地图_test\geojson-map-china\china.json"
gs_data = open(json_io, encoding='utf8').read()
gs_data = json.loads(gs_data)

Credit_Assistant_io=r"城投地图_test\Credit_Assistant.xlsx"

#整理plotly需要的格式：
for i in range(len(gs_data["features"])):
    gs_data["features"][i]["id"]=gs_data["features"][i]["properties"]["id"]#id前置
    gs_data["features"][i]["name"]=gs_data["features"][i]["properties"]["name"]
### 匹配id和区域
geo_id=[]
geo_name=[]
for i in range(len(gs_data["features"])):
    geo_id.append(gs_data["features"][i]["id"])
    geo_name.append(gs_data["features"][i]['properties']["name"])
geo_data=pd.DataFrame({"id":geo_id,"区域":geo_name})
data = pd.read_excel(r"城投地图_test\城投债数据_t.xlsx")
GK=pd.read_excel(Credit_Assistant_io,sheet_name="国开可比基准",skiprows=1,index_col=0).iloc[2:,:]
GK_yield_base=GK.tail(1).T
GK_yield_base.columns=["GK_yield"]
GK_yield_base["期限"]=[1,2,3,4,5]

## 定义根据债券余额加权的点乘积：
def weighted_premium(dff_VS_GK):
    weighted_premium=np.dot(dff_VS_GK["券种利差"],dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"]/dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"].sum())
    return round(weighted_premium,2)

def get_credit_premium():
    data= pd.read_excel(Credit_Assistant_io,skiprows=1,index_col=0).iloc[2:,:]
    index_code=pd.read_excel(Credit_Assistant_io,skiprows=1,index_col=0).iloc[1,:].tolist()
    index_name=pd.read_excel(Credit_Assistant_io).iloc[0,1:].tolist()
    str=","
    err,df=w.edb(str.join(index_code),"2019-01-01", dt.datetime.today().strftime("%Y-%m-%d"),"Fill=Previous",usedf=True)
    df.columns=index_name
    return df

def get_credit_vs_gk_data():
    GK_yield_base=GK_updated_yield()
    dff_VS_GK=pd.merge(df[df["期限"]<5],GK_yield_base,left_on=["期限_匹配"],right_on=["期限"],how="left")
    dff_VS_GK["券种利差"]=(dff_VS_GK["债券估值(YY)\n[单位] %"]-dff_VS_GK["GK_yield"])*100
    dff_VS_GK=dff_VS_GK[dff_VS_GK["券种利差"].isna()==False]
    return dff_VS_GK



def province_credit_premium_fig():
    fig = px.choropleth_mapbox(dff_province_credit_premium, geojson=gs_data, locations='id', color='信用利差',
            range_color=(20, 400),
           zoom=3, center = {"lat": 37.4189, "lon": 116.4219},
           mapbox_style='carto-positron',
           hover_data = ["区域"],
           custom_data=["区域"]
           )
 #   layout = dict(margin={"r":0,"t":0,"l":0,"b":0},clickmode="event+select")

    fig.update_geos(fitbounds="locations", visible=True)  
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(clickmode="event+select")

    return fig


info_dimension="券种利差","债券余额\n[日期] 最新\n[单位] 亿"



## 筛选非PPN
data = data[data["证券简称"].str.contains("PPN")==False]
#确定债券的可比期限
data["含权债行权期限"]=data["含权债行权期限"].fillna(10)
data["含权债行权期限"]=data["含权债行权期限"]*365
df=pd.DataFrame(data=data)
df["期限"]=((data[["含权债行权期限","剩余期限(天)\n[日期] 最新\n[单位] 天"]].min(axis=1))/365).round(2)
df["期限_匹配"]=((data[["含权债行权期限","剩余期限(天)\n[日期] 最新\n[单位] 天"]].min(axis=1))/365).round(0)
dff_VS_GK=pd.merge(df[df["期限"]<5],GK_yield_base,left_on=["期限_匹配"],right_on=["期限"],how="left")
dff_VS_GK["券种利差"]=(dff_VS_GK["债券估值(YY)\n[单位] %"]-dff_VS_GK["GK_yield"])*100
dff_VS_GK=dff_VS_GK[dff_VS_GK["券种利差"].isna()==False]
info_dimension=["券种利差","债券余额\n[日期] 最新\n[单位] 亿"]
province_credit_premium=dff_VS_GK.groupby("区域")[info_dimension].apply(lambda x : weighted_premium(x))
dff_province_credit_premium=pd.merge(pd.DataFrame(province_credit_premium,columns=["信用利差"]),geo_data,left_on="区域",right_on="区域")
# 每个省份对应的城市
province_city = []
for name,group in dff_VS_GK.groupby("区域")['城市']:
    temp = dict()
    temp['label'] = name
    temp['value'] = group.unique().tolist()
    province_city.append(temp)
    
available_cities = dff_VS_GK['城市'].unique()

#fig = province_credit_premium_fig(province_credit_premium)
info_dimension="券种利差","债券余额\n[日期] 最新\n[单位] 亿"
app.layout = html.Div(
    
    [
        html.Div(
        [dcc.Graph(id='China-bond-map',figure=province_credit_premium_fig()
 #             clickData = {'points': [{'区域':'江苏省'}]},     
 #             figure = fig
              ),
         dcc.Graph( id='bond-by-city')]
        ,style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        
        dcc.Dropdown(id = 'choose-of-cities',
                  options = [{'label': i, 'value': i} for i in available_cities],
                  value=['上海市','北京市'],
                  placeholder="请选择选择想要比较的城市",
                  multi = True),

        dcc.Graph(id = 'compare-bond-by-city')
    ]
    
)



@app.callback(
    dash.dependencies.Output('bond-by-city', 'figure'),
    [dash.dependencies.Input('China-bond-map', 'clickData'),
    dash.dependencies.Input('China-bond-map', 'figure')],
    )
def update_figure(clickData,figure):
    if clickData is None:
        clickData = {'points':[{'location':'江苏省'}]}
        province = clickData['points'][0]['location']

        df_province = dff_VS_GK[dff_VS_GK['区域'] == province]
        dff = df_province.groupby("城市")["券种利差","债券余额\n[日期] 最新\n[单位] 亿"].apply(lambda x : weighted_premium(x))
        dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
        fig = px.bar(dff2, x="城市", y="信用利差")

    #  fig.update_layout(transition_duration=500)

        return fig

    if clickData is not None:
        return px.line(data=1)



    
 

@app.callback(
    dash.dependencies.Output('compare-bond-by-city', 'figure'),
    [dash.dependencies.Input('choose-of-cities', 'value')])
def compare_figure(cities):
    df_cities = dff_VS_GK[dff_VS_GK['城市'].isin(cities)]
    dff = df_cities.groupby("城市")["券种利差","债券余额\n[日期] 最新\n[单位] 亿"].apply(lambda x : weighted_premium(x))
    dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
    fig = px.bar(dff2, x="城市", y="信用利差")
    return fig



if __name__ == '__main__':
    server.run()

#dff = dff_VS_GK[dff_VS_GK['城市'].isin(cities)]
#dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
#fig = px.bar(dff2, x="index", y="信用利差")
#fig


