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
import models
   
        
#%%
path = os.getcwd()+'\\models'
files = os.listdir(path)
dcc_graph_list = []
for i in files:
    os.system(i)
    dcc_graph_list.append(graph)

def create_macro_prediction_page():

    layout = html.Div(children = dcc_graph_list)
    
    return layout





    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    