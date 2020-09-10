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

def create_economy_following_page():
    gauge=create_economy_following_gauge("123")
    
    container = html.Div([
            dbc.Row([
                dbc.Col([
                    create_economy_following_card("123")
                ]),
                dbc.Col([
                    create_economy_following_card("123")
                ]),
            ]),
        ])

    page=dbc.Container([gauge,container])
    
    return page


def create_economy_following_card(title):
    title=title
    card = html.Div([
        dbc.CardHeader(html.H6(title)),
        dbc.CardBody([
            dbc.Alert(
                            "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                            id="no-data-alert-",
                            color="warning",
                            style={"display": "none"},
                                ),
            dbc.Row([
            ]),
            dcc.Graph(id='xxx'),
        ])
    ])
    return card

def create_economy_following_gauge(title):
    title=title
    
    GAUGE = html.Div([
        dbc.CardHeader(html.H6(title)),
        dbc.Alert(
             "Not enough data to render these plots, please adjust the filters",
            id="no-data-alert",
            color="warning",
            style={"display": "none"},
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='x1'),
                ]),
                dbc.Col([
                    dcc.Graph(id='x2'),
                ]),
                dbc.Col([
                    dcc.Graph(id='x3'),
                ]),
            ])
        ])
    ])
    
    return GAUGE
    
