# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:38:21 2020

@author: User
"""


import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from numpy.matrixlib import test
import os
import pandas as pd
import numpy as np
from models import CPI as cpi
from models import PPI as ppi



#%%

dcc_graph_list = [ppi.main()]


def create_macro_prediction_page():

    layout = html.Div(children = [
        html.Div(
            id = 'banner',
            className = 'banner',
            children = html.H4(children='宏观经济数据预测')
            ),
        cpi.main(),
        ppi.main()
        ]
        )

    
    return layout




    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    