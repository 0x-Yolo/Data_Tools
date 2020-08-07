import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import pandas as pd
import pathlib

import modular.mkt_behavior as mkt_b
import modular.config as conf

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

def create_mkt_behavior_page():
    a,b=create_mkt_behavior_card()

    WORDCLOUD_PLOTS = [
    dbc.CardHeader(html.H6("杠杆监测仪表")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Tabs(                            
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label = '基金净值比例（亿元）',
                                        children=[
                                            dcc.Loading(
                                                id="loading_fig_net_assets_fund_type",
                                                children=[dcc.Graph(figure=mkt_b.fig_net_assets_fund_type("2020年07月"),id="fig_net_assets_fund_type")],
                                                type="default",
                                                )
                                            ],
                                    )],
                        ),
                    ),
                    dbc.Col(
                        [
                            dcc.Tabs(
                                id="tabs",
                                children=[
                                    dcc.Tab(
                                        label="新发基金规模(亿元)",
                                        children=[
                                            dcc.Loading(
                                                id="loading-fig_margin_newfund_scale",
                                                children=[dcc.Graph(figure=mkt_b.fig_margin_newfund_scale(),id="fig_margin_newfund_scale")],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="新发基金规模(个数)",
                                        children=[
                                            dcc.Loading(
                                                id="loading-fig_margin_newfund_amt",
                                                children=[
                                                    dcc.Graph(figure=mkt_b.fig_margin_newfund_amt(),id="fig_margin_newfund_amt")
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                        md=8,
                    ),
                ]
            )
        ]
    ),]

    return dbc.Container([html.Div(WORDCLOUD_PLOTS),a,b])




def create_mkt_behavior_card():
    
    c1 = html.Div([
        dbc.CardHeader(html.H6("回购行为观测")),
        #html.P("123123123"),
        dbc.CardBody(
            [
            dcc.Loading(
                id = "mkt_b_bond",   
                children=
                [
                    dbc.Alert(
                            "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                            id="no-data-alert-bigrams_comp",
                            color="warning",
                            style={"display": "none"},
                                ),    
                    dbc.Row([### 融资行为
                            dbc.Col([#左边的dropdown，选择什么类型的机构
                                dcc.Dropdown(
                                    id='repo_loaner',
                                    options=[{'label': i, 'value': i} for i in conf.Inter_Graph.repo_loaner_OL],
                                    value='基金公司及产品'
                                )
                            ],style={'width': '33%', 'display': 'inline-block'}),

                            #########
                            dbc.Col([#中间的dropdown，选择期限品种
                                dcc.Dropdown(
                                    id='repo_terms',
                                    options=[{'label': i, 'value': i} for i in conf.Inter_Graph.repo_terms_OL],
                                    value=['R001','R007','R014'],
                                    multi=True
                                )
                            ],style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
                            
                            
                            dbc.Col([#右边的dropdown，选择是逆回购余额还是逆回购净额
                                dcc.Dropdown(
                                    id='flow_or_abs_repo_amt',
                                    options=[{"label":"回购余额(亿元)","value":"回购余额"},
                                            {"label":"回购净额(亿元)","value":"净融入金额(考虑今日到期量)(百万)"}],
                                    value='回购余额',
                                )
                            ],style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
                        ]),
                    dcc.Graph(id='investors_net_repo_for_terms'),
                ],
                ),
            ],
            style={"marginTop": 0, "marginBottom": 0},
            ),       
    ])

    
    c2 = html.Div([#债券净买入图
            dbc.CardHeader(html.H6("债券买卖观测")),
            dbc.CardBody(
                [
                dcc.Loading(
                id = "mkt_b_repo",   
                children=
                [
                    dbc.Alert(
                            "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                            id="no-data-alert-bigrams_comp",
                            color="warning",
                            style={"display": "none"},
                                ),    
                    dbc.Row([### 融资行为
                        dbc.Col([#投资者类型，多选，累加
                        dcc.Dropdown(
                            id='bond_buyer',
                            options=[{'label': i, 'value': i} for i in conf.Inter_Graph.bond_buyer_OL],
                            value='基金公司及产品',
                        )
                        ],style={'width': '33%', 'float': 'left','display': 'inline-block'}),

                        dbc.Col([#债券资产的期限
                        dcc.Dropdown(
                            id='bond_duration',
                            options=[{'label': i, 'value': i} for i in conf.Inter_Graph.bond_duration_OL],
                            value=['7-10年','3-5年','1-3年'],
                            multi=True
                        )
                        ],style={'width': '33%', 'float': 'middle', 'display': 'inline-block'}),

                        dbc.Col([#债券资产品种
                        dcc.Dropdown(
                            id='bond_type',
                            options=[{'label': i, 'value': i} for i in conf.Inter_Graph.bond_type_OL],
                            value=['合计'],
                            multi=True
                        )],style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
                        ]),
                    dcc.Graph(id='Net_buy_bond'),
                ])
                ],style={"marginTop": 0, "marginBottom": 0}),
             ])
    
    
    return c1,c2

def create_mkt_behavior_gauge():
    
    return 1

def create_mkt_behavior_tab():
    
    return 1
    



# def create_layout(app):
#     # Page layouts
#     return html.Div(
#         [
#             html.Div([Header(app)]),
#             # page 1
#             html.Div(
#                 [
#                     # Row 3
#                     html.Div(
#                         [
#                             html.Div(
#                                 [
#                                     html.H5("Product Summary"),
#                                     html.Br([]),
#                                     html.P(
#                                         "\
#                                     As the industry’s first index fund for individual investors, \
#                                     the Calibre Index Fund is a low-cost way to gain diversified exposure \
#                                     to the U.S. equity market. The fund offers exposure to 500 of the \
#                                     largest U.S. companies, which span many different industries and \
#                                     account for about three-fourths of the U.S. stock market’s value. \
#                                     The key risk for the fund is the volatility that comes with its full \
#                                     exposure to the stock market. Because the Calibre Index Fund is broadly \
#                                     diversified within the large-capitalization market, it may be \
#                                     considered a core equity holding in a portfolio.",
#                                         style={"color": "#ffffff"},
#                                         className="row",
#                                     ),
#                                 ],
#                                 className="product",
#                             )
#                         ],
#                         className="row",
#                     ),
#                     # Row 4
#                     html.Div(
#                         [
#                             html.Div(
#                                 [
#                                     html.H6(
#                                         ["Fund Facts"], className="subtitle padded"
#                                     ),
#                                 ],
#                                 className="six columns",
#                             ),
#                             html.Div(                              [
#                                     html.H6(
#                                         "Average annual performance",
#                                         className="subtitle padded",
#                                     ),
#                                     dcc.Graph(
#                                         id="graph-1",
#                                         figure={
#                                             "data": [
#                                                 go.Bar(
#                                                     x=[
#                                                         "1 Year",
#                                                         "3 Year",
#                                                         "5 Year",
#                                                         "10 Year",
#                                                         "41 Year",
#                                                     ],
#                                                     y=[
#                                                         "21.67",
#                                                         "11.26",
#                                                         "15.62",
#                                                         "8.37",
#                                                         "11.11",
#                                                     ],
#                                                     marker={
#                                                         "color": "#97151c",
#                                                         "line": {
#                                                             "color": "rgb(255, 255, 255)",
#                                                             "width": 2,
#                                                         },
#                                                     },
#                                                     name="Calibre Index Fund",
#                                                 ),
#                                                 go.Bar(
#                                                     x=[
#                                                         "1 Year",
#                                                         "3 Year",
#                                                         "5 Year",
#                                                         "10 Year",
#                                                         "41 Year",
#                                                     ],
#                                                     y=[
#                                                         "21.83",
#                                                         "11.41",
#                                                         "15.79",
#                                                         "8.50",
#                                                     ],
#                                                     marker={
#                                                         "color": "#dddddd",
#                                                         "line": {
#                                                             "color": "rgb(255, 255, 255)",
#                                                             "width": 2,
#                                                         },
#                                                     },
#                                                     name="S&P 500 Index",
#                                                 ),
#                                             ],
#                                             "layout": go.Layout(
#                                                 autosize=False,
#                                                 bargap=0.35,
#                                                 font={"family": "Raleway", "size": 10},
#                                                 height=200,
#                                                 hovermode="closest",
#                                                 legend={
#                                                     "x": -0.0228945952895,
#                                                     "y": -0.189563896463,
#                                                     "orientation": "h",
#                                                     "yanchor": "top",
#                                                 },
#                                                 margin={
#                                                     "r": 0,
#                                                     "t": 20,
#                                                     "b": 10,
#                                                     "l": 10,
#                                                 },
#                                                 showlegend=True,
#                                                 title="",
#                                                 width=330,
#                                                 xaxis={
#                                                     "autorange": True,
#                                                     "range": [-0.5, 4.5],
#                                                     "showline": True,
#                                                     "title": "",
#                                                     "type": "category",
#                                                 },
#                                                 yaxis={
#                                                     "autorange": True,
#                                                     "range": [0, 22.9789473684],
#                                                     "showgrid": True,
#                                                     "showline": True,
#                                                     "title": "",
#                                                     "type": "linear",
#                                                     "zeroline": False,
#                                                 },
#                                             ),
#                                         },
#                                         config={"displayModeBar": False},
#                                     ),
#                                 ],
#                                 className="six columns",
#                             ),
#                         ],
#                         className="row",
#                         style={"margin-bottom": "35px"},
#                     ),
#                     # Row 5
#                     html.Div(
#                         [
#                             html.Div(
#                                 [
#                                     html.H6(
#                                         "Hypothetical growth of $10,000",
#                                         className="subtitle padded",
#                                     ),
#                                     dcc.Graph(
#                                         id="graph-2",
#                                         figure={
#                                             "data": [
#                                                 go.Scatter(
#                                                     x=[
#                                                         "2008",
#                                                         "2009",
#                                                         "2010",
#                                                         "2011",
#                                                         "2012",
#                                                         "2013",
#                                                         "2014",
#                                                         "2015",
#                                                         "2016",
#                                                         "2017",
#                                                         "2018",
#                                                     ],
#                                                     y=[
#                                                         "10000",
#                                                         "7500",
#                                                         "9000",
#                                                         "10000",
#                                                         "10500",
#                                                         "11000",
#                                                         "14000",
#                                                         "18000",
#                                                         "19000",
#                                                         "20500",
#                                                         "24000",
#                                                     ],
#                                                     line={"color": "#97151c"},
#                                                     mode="lines",
#                                                     name="Calibre Index Fund Inv",
#                                                 )
#                                             ],
#                                             "layout": go.Layout(
#                                                 autosize=True,
#                                                 title="",
#                                                 font={"family": "Raleway", "size": 10},
#                                                 height=200,
#                                                 width=340,
#                                                 hovermode="closest",
#                                                 legend={
#                                                     "x": -0.0277108433735,
#                                                     "y": -0.142606516291,
#                                                     "orientation": "h",
#                                                 },
#                                                 margin={
#                                                     "r": 20,
#                                                     "t": 20,
#                                                     "b": 20,
#                                                     "l": 50,
#                                                 },
#                                                 showlegend=True,
#                                                 xaxis={
#                                                     "autorange": True,
#                                                     "linecolor": "rgb(0, 0, 0)",
#                                                     "linewidth": 1,
#                                                     "range": [2008, 2018],
#                                                     "showgrid": False,
#                                                     "showline": True,
#                                                     "title": "",
#                                                     "type": "linear",
#                                                 },
#                                                 yaxis={
#                                                     "autorange": False,
#                                                     "gridcolor": "rgba(127, 127, 127, 0.2)",
#                                                     "mirror": False,
#                                                     "nticks": 4,
#                                                     "range": [0, 30000],
#                                                     "showgrid": True,
#                                                     "showline": True,
#                                                     "ticklen": 10,
#                                                     "ticks": "outside",
#                                                     "title": "$",
#                                                     "type": "linear",
#                                                     "zeroline": False,
#                                                     "zerolinewidth": 4,
#                                                 },
#                                             ),
#                                         },
#                                         config={"displayModeBar": False},
#                                     ),
#                                 ],
#                                 className="six columns",
#                             ),
#                             html.Div(
#                                 [
#                                     html.H6(
#                                         "Price & Performance (%)",
#                                         className="subtitle padded",
#                                     ),
#                                 ],
#                                 className="six columns",
#                             ),
#                             html.Div(
#                                 [
#                                     html.H6(
#                                         "Risk Potential", className="subtitle padded"
#                                     ),
#                                     html.Img(
#                                         src=app.get_asset_url("risk_reward.png"),
#                                         className="risk-reward",
#                                     ),
#                                 ],
#                                 className="six columns",
#                             ),
#                         ],
#                         className="row ",
#                     ),
#                 ],
#                 className="sub_page",
#             ),
#         ],
#         className="page",
#     