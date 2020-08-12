# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:19:47 2020

@author: User
"""

import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from numpy.matrixlib import test
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import json
import data_organize as do
import demjson
from datetime import datetime
from datetime import timedelta
import pymysql


server = flask.Flask(__name__) 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,server=server,external_stylesheets=external_stylesheets)

# ------------------------------------新建函数----------------------------------

## 定义根据债券余额加权的点乘积：
def weighted_premium(dff_VS_GK):
    weighted_premium=np.dot(dff_VS_GK["券种利差"],dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"]/dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"].sum())
    return round(weighted_premium,2)

# ------------------------------------地图所需数据------------------------------
json_io=r"geojson-map-china\china.json"
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
Credit_Assistant_io=r"Credit_Assistant.xlsx"

# -----------------------------------从数据库读取数据-----------------------------
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

# -----------------------------------数据处理------------------------------------
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
df["含权债行权期限"]=df["含权债行权期限"].fillna(10)*365
df["期限"]=((df[["含权债行权期限","剩余期限(天)\n[日期] 最新\n[单位] 天"]].min(axis=1))/365).round(2)
df["期限_匹配"]=((df[["含权债行权期限","剩余期限(天)\n[日期] 最新\n[单位] 天"]].min(axis=1))/365).round(0)
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
info_dimension=["券种利差","债券余额\n[日期] 最新\n[单位] 亿"]
# 计算每个区域按照债券余额加权平均的利差
province_credit_premium=dff_VS_GK.groupby("区域")[info_dimension].apply(lambda x : weighted_premium(x))
province_credit_premium_df=pd.DataFrame(province_credit_premium,columns=["信用利差"])
# 计算每个城市按照债券余额加权平均的利差
city_credit_premium=dff_VS_GK.groupby("城市")[info_dimension].apply(lambda x : weighted_premium(x))
city_credit_premium_df=pd.DataFrame(city_credit_premium,columns=["信用利差"]).reset_index()
# 合并画地图所需的数据框
dff_province_credit_premium=pd.merge(province_credit_premium_df,geo_data,left_on="区域",right_on="区域")
# 制作表格所需数据
columns_for_table = ['证券代码','证券简称','主体名称','上市日期','债券余额\n[日期] 最新\n[单位] 亿',
                     '剩余期限(天)\n[日期] 最新\n[单位] 天','债券估值(YY)\n[单位] %','期限_匹配','券种利差']
table_columns = [ "证券代码","证券简称",'主体名称',"上市日期","债券余额(亿)",
                 "剩余期限(天)","债券估值","期限(年)","券种利差"]

df_table = dff_VS_GK[columns_for_table]
df_table.columns = table_columns
df_table['券种利差'] = round(df_table['券种利差'],2)

# 每个城市对应的省份
city_province = {}
for name,group in dff_VS_GK.groupby("城市")['区域']:
    city_province[name] = group.tolist()[0]
# 所有城市
available_cities = dff_VS_GK['城市'].unique()

# --------------------------------------构建app---------------------------------------

# 布局
app.layout = html.Div(
    className="container scalable",
    children = [
        html.Div(
            id = 'banner',
            className = 'banner',
            children = html.H6(children='城投债利差地图：请点击省份查看具体城市利差')         
            ),
        html.Div(
            className="app_main_content",
            children = [
                html.Div(
                    id="choose_of_aggregating_method_outer",
                    children=[
                        
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="choose_of_aggregating_method",
                                    options=[
                                        {"label": "按照债券余额加权平均", "value": "by_volumn"},
                                        {"label": "其他", "value": "other_methods"},
                                    ],
                                    value="by_volumn",
                                    placeholder="请选择省份利差计算方法"
                                ),
                            ],
                            className="three columns",
                        ),
                        html.Div(    
                            [
                                dcc.Dropdown(
                                    id="choose_of_level_or_change",
                                    options=[
                                        {"label": "利差水平", "value": "ir_diff_level"},
                                        {"label": "利差变化", "value": "ir_diff_change"},
                                    ],
                                    value="ir_diff_level",
                                    placeholder="请选择利差水平/利差变化"
                                )
                            ],
                            id="choose_of_level_or_change_outer",
                            className="three columns",
                            )
                        
                        ]
                    ),
                html.Div(
                    id = 'top_row',
                   className = 'row', 
                   children = [        
                      html.Div(
                          className = 'seven columns',
                          children = dcc.Graph(id='China_bond_map')
                          ),
                      html.Div(
                          className = 'five columns',
                          children = dcc.Graph( id='bond_by_city')
                          )
                      ]
                    ),
                html.Div(children=html.H6("请选择想要比较的城市：")),
                html.Div(
                    children = dcc.Dropdown(id = 'choose_of_cities',
                                              options = [{'label': i, 'value': i} for i in available_cities],
                                              value=['上海市','北京市','苏州市','南京市','杭州市','宁波市'],
                                              placeholder="请选择想要比较的城市",
                                              multi = True)
                    ),
                
                html.Div(
                    id = 'second_row',
                    className = 'row', 
                    children = [        
                      
                      html.Div(
                          className = 'six columns',
                          children = dcc.Graph(id = 'compare_bond_by_city')
                          ),
                      html.Div(
                          className = 'six columns',
                          children = dcc.Graph(id='bond_by_issuer')
                          )
                      ]
                    ),
                html.Div(
                    id = 'third_row',
                    className = 'row',
                    children = dash_table.DataTable(
                              id = 'individual_bond_table',
                              columns=[
                                  {"name": i, "id": i}
                                  for i in table_columns
                                  ],
                              data=[],
                              style_as_list_view=True,
                              style_cell_conditional=[
                                                {
                                                    'if': {'column_id': c},
                                                    'textAlign': 'left'
                                                } for c in ['Date', 'Region']
                                            ],
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }
                                            ],
                                            style_header={
                                                'backgroundColor': 'rgb(230, 230, 230)',
                                                'fontWeight': 'bold'
                                            }
                              )
                            )
                ]
            )
        ]
    )

 


@app.callback(
    dash.dependencies.Output('China_bond_map', 'figure'),
    [dash.dependencies.Input('choose_of_aggregating_method', 'value'),
     dash.dependencies.Input('choose_of_level_or_change', 'value')]
    )
def province_credit_premium_fig(agg_method,value):
    if agg_method == 'by_volumn':
        fig = px.choropleth_mapbox(dff_province_credit_premium, 
                geojson=gs_data, locations='id', color='信用利差',
                range_color=(20, 400),
               zoom=2, center = {"lat": 37.4189, "lon": 116.4219},
               mapbox_style='white-bg',
               hover_data = ["区域"],
               custom_data = ["区域"]
           )
 #   layout = dict(margin={"r":0,"t":0,"l":0,"b":0},clickmode="event+select")
        fig.update_geos(fitbounds="locations", visible=True)  
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(clickmode="event+select")
        fig.update_traces(customdata=dff_province_credit_premium["区域"])
    return fig

@app.callback(
    dash.dependencies.Output('bond_by_city', 'figure'),
    [dash.dependencies.Input('China_bond_map', 'clickData'),
    dash.dependencies.Input('China_bond_map', 'figure')],
    )
def update_figure(clickData,figure):
    if clickData == None:
        clickData = {'points':[{'customdata':'江苏省'}]}
    province = clickData["points"][0]["customdata"]
    df_province = dff_VS_GK[dff_VS_GK['区域'] == province]
    dff = df_province.groupby("城市")[info_dimension].apply(lambda x : weighted_premium(x))
    dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
    dff3 = province_credit_premium_df.reset_index()
    trace1 = go.Bar(
            x = dff2['城市'],
            y = dff2['信用利差'],
            name = '各城市',
            marker = dict(
                color = '#9370DB'
                )   
        )
    trace2 = go.Scatter(
            x = dff2['城市'],
            y = np.tile(dff3[dff3['区域'] == clickData["points"][0]["customdata"]]['信用利差'].tolist()[0],100),
            mode = 'lines',
            line = dict(
                width = 2,
                dash ="dash"
                ),
            name = clickData["points"][0]["customdata"],
            )
    data = [trace1,trace2]  
    layout = go.Layout(
        title = {
            'text':''.join((clickData["points"][0]["customdata"],'各城市信用利差')),
            'x':0.5
            }      
)
    fig = go.Figure(data = data,layout = layout)    
          
    
    return fig


# @app.callback(
#     dash.dependencies.Output('selected-data', 'children'),
#     [dash.dependencies.Input('China-bond-map', 'clickData')]
#     )
# def update_figure(clickData):
#     result = clickData["points"]
#     return result
    

@app.callback(
    dash.dependencies.Output('compare_bond_by_city', 'figure'),
    [dash.dependencies.Input('choose_of_cities', 'value')])
def compare_figure(cities):
    dff = city_credit_premium_df[city_credit_premium_df['城市'].isin(cities)]
    provinces = set([city_province[i] for i in cities])
    dff2 = province_credit_premium_df.reset_index()
    trace1 = go.Bar(
            x = dff['城市'],
            y = dff['信用利差'],
            name = '各城市',
            marker = dict(
                color = '#9370DB'
                )   
        )
    data = [trace1]    
    for i in provinces:
        data.append(
            
            go.Scatter(
            x = dff['城市'],
            y = np.tile(dff2[dff2['区域'] == i]['信用利差'].tolist()[0],1000),
            mode = 'lines',
            line = dict(
                width = 2,
                dash ="dash"
                ),
            name = i
            )
            
        )
        layout = go.Layout(
            title = {'text':'各城市利差对比',
                     'x':0.5},
            yaxis = {'title':'利差'})
        fig = go.Figure(data = data,layout = layout)
        fig.update_layout(clickmode="event+select")
        fig.update_traces(customdata=dff["城市"])         
        
    return fig

@app.callback(
    dash.dependencies.Output('bond_by_issuer', 'figure'),
    [dash.dependencies.Input('compare_bond_by_city', 'clickData'),
    dash.dependencies.Input('compare_bond_by_city', 'figure')],
    )
def update_figure(clickData,figure):
    if clickData == None:
        clickData = {'points':[{'customdata':'上海市'}]}
    city = clickData["points"][0]["customdata"]
    df_city = dff_VS_GK[dff_VS_GK['城市'] == city]
    dff = df_city.groupby("主体名称")[info_dimension].apply(lambda x : weighted_premium(x))
    dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
    trace1 = go.Scatter(
            x = dff2['主体名称'],
            y = dff2['信用利差'],
            mode = 'markers',
            name = '各主体',
            marker = dict(
                color = '#DA70D6',
                size = 10,
                opacity = 0.8
                )   
        )
    trace2 = go.Scatter(
            x = dff2['主体名称'],
            y = np.tile(city_credit_premium_df[city_credit_premium_df['城市'] == clickData["points"][0]["customdata"]]['信用利差'].tolist()[0],100),
            mode = 'lines',
            line = dict(
                width = 2,
                dash ="dash"
                ),
            name = clickData["points"][0]["customdata"]
            )
    data = [trace1,trace2]     
    layout = go.Layout(
        yaxis = {'title':'利差'},
        xaxis = {'title':'各主体',
                 'visible':False},
        title = {'text':''.join((clickData["points"][0]["customdata"],'各主体信用利差')),
                 'x':0.5})
    fig = go.Figure(data = data,layout = layout)
    fig.update_layout(clickmode="event+select")
    fig.update_traces(customdata=dff2["主体名称"])       
    return fig


@app.callback(
    dash.dependencies.Output('individual_bond_table', 'data'),
    [dash.dependencies.Input('bond_by_issuer', 'clickData'),
    dash.dependencies.Input('bond_by_issuer', 'figure')],
    )
def update_figure(clickData,figure):
    if clickData == None:
        clickData = {'points':[{'customdata':'上海大宁资产经营(集团)有限公司'}]}
    dff = df_table[df_table['主体名称'] == clickData["points"][0]["customdata"]]
#    dff2 = dff.drop(['主体名称'],axis = 1)
    return dff.to_dict("records")
    



if __name__ == '__main__':
    server.run()

#dff = dff_VS_GK[dff_VS_GK['城市'].isin(cities)]
#dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
#fig = px.bar(dff2, x="index", y="信用利差")
#fig


