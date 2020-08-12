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


## 定义根据债券余额加权的点乘积：
def weighted_premium(dff_VS_GK):
    weighted_premium=np.dot(dff_VS_GK["券种利差"],dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"]/dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"].sum())
    return round(weighted_premium,2)


def create_city_bond_page():
      banner = dbc.CardHeader(html.H6("城投债利差地图：请点击省份查看具体城市利差"))
      dropdown_outer = html.Div(
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
                        )
      top_row = html.Div(
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
      second_row = html.Div(
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
                        )
      third_row = html.Div(
                        id = 'third_row',
                        className = 'row',
                        children = dash_table.DataTable(
                                  id = 'individual_bond_table',
                                  columns=[
                                      {"name": i, "id": i}
                                      for i in [ "证券代码","证券简称",'主体名称',"上市日期","债券余额(亿)",
                     "剩余期限(天)","债券估值","期限(年)","券种利差"]
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
      return dbc.Container([banner,dbc.CardBody([dropdown_outer,top_row,second_row,third_row])])
                    
