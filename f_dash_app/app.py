

import os
import re
import sys
import dash
from datetime import datetime as dt
import pandas as pd
import  pymysql

import flask
#导入plotly库
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import datetime as dt

import modular.config as conf
import modular.mkt_behavior as mkt_b

import P1_mkt_behavior_page
import P2_economy_following_page
import P3_mkt_pattern_playbook

#导入数据


# %%

server = flask.Flask(__name__) 
app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])


##各类style文件
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 60,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE= {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
 
navbar = html.Div([
    dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("TPYZQ", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)])

sidebar = html.Div(
    [
        html.H5("Dashboard", className="display-4"),
        html.Hr(),
        html.P(
            "金融市场观测与跟踪", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("金融市场行为数据", href="/page-1", id="page-1-link"),
                dbc.NavLink("基本面高频跟踪", href="/page-2", id="page-2-link"),
                dbc.NavLink("算法拟合与预测", href="/page-3", id="page-3-link"),
                dbc.NavLink("我们的观点", href="/page-4", id="page-4-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([navbar,dcc.Location(id="url"),sidebar,content])





## 所有的绘图和逻辑都存放在 behavior向下



# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
#########定义交互的方式

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return P1_mkt_behavior_page.create_mkt_behavior_page()
    elif pathname == "/page-2":
        return P2_economy_following_page.create_economy_following_page()
    elif pathname == "/page-3":
        return P3_mkt_pattern_playbook.create_mkt_pattern_playbook_page()
    elif pathname == "/page-4":
        return html.P("敬请期待")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



# %%
@app.callback(
    Output('investors_net_repo_for_terms', 'figure'),
    [Input('repo_loaner', 'value'),
        Input('repo_terms', 'value'),
        Input('flow_or_abs_repo_amt', 'value')])
def update_graph_repo(repo_loaner,repo_terms,flow_or_abs_repo_amt):
    
    fig = mkt_b.Fig_Repo_amt_prc_for_terms(repo_loaner,repo_terms,flow_or_abs_repo_amt)
    return fig


# %%
@app.callback(
    Output('Net_buy_bond', 'figure'),
    [Input('bond_buyer', 'value'),
        Input('bond_duration', 'value'),
        Input('bond_type', 'value')])
def update_graph_buy(bond_buyer,bond_duration,bond_type):
    
    fig = mkt_b.Fig_Net_buy_bond(bond_buyer,bond_duration,bond_type)
    return fig


# @app.callback(
#     Output('fig_net_assets_fund_type', 'figure'),
#     [Input('date_slider_fig_net_assets_fund_type', 'value')])
# def update_fig_net_assets_fund_type(date_slider_fig_net_assets_fund_type):
#     fig=mkt_b.fig_net_assets_fund_type(date_slider_fig_net_assets_fund_type)
#     return fig



if __name__ == '__main__':
    app.run_server(debug=True)#线上使用
    #server.run()#本地调试用



