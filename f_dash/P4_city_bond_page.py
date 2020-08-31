import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from numpy.matrixlib import test
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import demjson
from datetime import datetime
from datetime import timedelta
import pymysql
import modular.city_bond as mkt_c
import modular.config as conf

server = flask.Flask(__name__) 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,server=server,external_stylesheets=external_stylesheets)



dff_VS_GK = conf.get_ir_diff()
# 所有城市
available_cities = dff_VS_GK['城市'].unique()
table_columns = [ "证券代码","证券简称",'主体名称',"上市日期","债券余额(亿)",
                 "剩余期限(天)","债券估值","期限(年)","券种利差"]

## 定义根据债券余额加权的点乘积：
def weighted_premium(dff_VS_GK):
    weighted_premium=np.dot(dff_VS_GK["券种利差"],dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"]/dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"].sum())
    return round(weighted_premium,2)


def create_city_bond_page():
    layout = html.Div(
    className="container scalable",
    children = [
        html.Div(
            id = 'banner',
            className = 'banner',
            children = html.H6(children='城投债利差地图')         
            ),
        html.Div(
            id = 'top_row',
            
            children = [
                html.Div(
                            
                            children = [
                                html.Div(
                                    id="choose_of_aggregating_method_outer",
                                    children=[
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="choose_of_level_or_change",
                                                    options=[
                                                        {"label": "利差水平", "value": "by_level"},
                                                        {"label": "利差变化", "value": "by_change"},
                                                    ],
                                                    value="by_level",
                                                    placeholder="请选择利差水平或变化"
                                                ),
                                            ],style={'width': '33%', 'display': 'inline-block'}
                                            
                                        ),
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="choose_of_aggregating_method",
                                                    options=[
                                                        {"label": "兴业研究利差数据（中位数）", "value": "by_medium"},
                                                        {"label": "其他", "value": "other_methods"},
                                                    ],
                                                    value="by_medium",
                                                    placeholder="请选择省份利差计算方法"
                                                ),
                                            ],style={'width': '33%', 'display': 'inline-block'}
                                            
                                        ),
                                        html.Div(    
                                            [
                                                dcc.Dropdown(id = 'choose_of_frequency',
                                                              options = [{'label': "1周", 'value': "1_week"},
                                                                         {'label': "2周", 'value': "2_week"},
                                                                         {'label': "3周", 'value': "3_week"},
                                                                         {'label': "1个月", 'value': "1_month"},
                                                                         {'label': "2个月", 'value': "2_month"},
                                                                         {'label': "3个月", 'value': "3_month"},
                                                                         {'label': "半年", 'value': "6_month"},
                                                                         {'label': "一年", 'value': "12_month"}],
                                                              value='1_week',
                                                              placeholder="请选择想要比较的时间频率",
                                                              multi = False)
                                                    
                                            ],style={'width': '33%', 'display': 'inline-block'}
                                            )
                                        
                                        ],style={
                                                'borderBottom': 'thin lightgrey solid',
                                                'backgroundColor': 'rgb(250, 250, 250)',
                                                'padding': '10px 5px'
                                            }
                                    ),
                                
                                 ]),
                                            
                html.Div(
                        children = dcc.Graph(id='China_bond_map'),
                        style={'width': '49%', 'display': 'inline-block'}
                    ),                     
                html.Div(
                        
                        children = dcc.Graph( id='bond_by_province'),
                        style={'width': '49%', 'display': 'inline-block'}
                      
                    ),
                    ]
                ),
                
                html.Div(
                    id = 'second_row',
                    children = [ 
                     
                      html.Div(children=html.H6("请选择想要比较的城市：")
                               ,style={
                                        'borderBottom': 'thin lightgrey solid',
                                        'backgroundColor': 'rgb(250, 250, 250)',
                                        'padding': '10px 5px'
                                            }),
                      html.Div(
                                    children = dcc.Dropdown(id = 'choose_of_cities',
                                                              options = [{'label': i, 'value': i} for i in available_cities],
                                                              placeholder="请选择想要比较的城市",
                                                              multi = True)
                                    ),
                      
                      html.Div(
                          [
                              html.Div(
                          children = dcc.Graph(id = 'compare_bond_by_city'),
                          style={'width': '49%', 'display': 'inline-block'}
                          ),
                              html.Div(
                          children = dcc.Graph(id='bond_by_issuer'),
                          style={'width': '49%', 'display': 'inline-block'}

                          )
                              ]
                          )
                      
                      ]
                    ),
                html.Div(
                    id = 'third_row',
                    children = dash_table.DataTable(
                              id = 'individual_bond_table',
                              columns=[
                                  {"name": i, "id": i} for i in table_columns
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

    return layout
                    
