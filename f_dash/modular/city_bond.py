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
import modular.data_organize as do
import demjson
from datetime import datetime
from datetime import timedelta
import pymysql
import modular.config as conf


server = flask.Flask(__name__) 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,server=server,external_stylesheets=external_stylesheets)

# ------------------------------------新建函数----------------------------------

## 定义根据债券余额加权的点乘积：
def weighted_premium(dff_VS_GK):
    
    weighted_premium=np.dot(dff_VS_GK["券种利差"],dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"]/dff_VS_GK["债券余额\n[日期] 最新\n[单位] 亿"].sum())
    return round(weighted_premium,2)


# %%
def fig_province_credit_premium(agg_method,value):

    dff_VS_GK = conf.get_ir_diff()
    geo_data,gs_data = conf.get_geo_data()
    info_dimension=["券种利差","债券余额\n[日期] 最新\n[单位] 亿"]
    # 计算每个区域按照债券余额加权平均的利差
    province_credit_premium=dff_VS_GK.groupby("区域")[info_dimension].apply(lambda x : weighted_premium(x))
    province_credit_premium_df=pd.DataFrame(province_credit_premium,columns=["信用利差"])     
    map_province_credit_premium=pd.merge(province_credit_premium_df,geo_data,left_on="区域",right_on="区域")
    if agg_method == 'by_volumn':
        fig = px.choropleth_mapbox(map_province_credit_premium, 
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
        fig.update_traces(customdata=map_province_credit_premium["区域"])
    return fig



# %%
def fig_city_credit_premium(clickData,figure):
    if clickData == None:
        clickData = {'points':[{'customdata':'江苏省'}]}
    province = clickData["points"][0]["customdata"]
    dff_VS_GK = conf.get_ir_diff()
    info_dimension=["券种利差","债券余额\n[日期] 最新\n[单位] 亿"]
    df_province = dff_VS_GK[dff_VS_GK['区域'] == province]
    dff = df_province.groupby("城市")[info_dimension].apply(lambda x : weighted_premium(x))
    dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
    province_credit_premium=dff_VS_GK.groupby("区域")[info_dimension].apply(lambda x : weighted_premium(x))
    province_credit_premium_df=pd.DataFrame(province_credit_premium,columns=["信用利差"])
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

# %%
    
def fig_compare_city_bond(cities):
    dff_VS_GK = conf.get_ir_diff()
    info_dimension=["券种利差","债券余额\n[日期] 最新\n[单位] 亿"]
    # 计算每个城市按照债券余额加权平均的利差
    city_credit_premium=dff_VS_GK.groupby("城市")[info_dimension].apply(lambda x : weighted_premium(x))
    city_credit_premium_df=pd.DataFrame(city_credit_premium,columns=["信用利差"]).reset_index()
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

# %% 
        
def fig_compare_issuer(clickData,figure):
    
        if clickData == None:
            clickData = {'points':[{'customdata':'上海市'}]}
        city = clickData["points"][0]["customdata"]
        dff_VS_GK = conf.get_ir_diff()
        info_dimension=["券种利差","债券余额\n[日期] 最新\n[单位] 亿"]
        df_city = dff_VS_GK[dff_VS_GK['城市'] == city]
        dff = df_city.groupby("主体名称")[info_dimension].apply(lambda x : weighted_premium(x))
        dff2 = pd.DataFrame(dff,columns = ['信用利差']).reset_index()
        city_credit_premium=dff_VS_GK.groupby("城市")[info_dimension].apply(lambda x : weighted_premium(x))
        city_credit_premium_df=pd.DataFrame(city_credit_premium,columns=["信用利差"]).reset_index()
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


# %%
        
def tab_individual_bond(clickData,figure):
    dff_VS_GK = conf.get_ir_diff()
    columns_for_table = ['证券代码','证券简称','主体名称','上市日期','债券余额\n[日期] 最新\n[单位] 亿',
                         '剩余期限(天)\n[日期] 最新\n[单位] 天','债券估值(YY)\n[单位] %','期限_匹配','券种利差']
    table_columns = [ "证券代码","证券简称",'主体名称',"上市日期","债券余额(亿)",
                     "剩余期限(天)","债券估值","期限(年)","券种利差"] 
    df_table = dff_VS_GK[columns_for_table]
    df_table.columns = table_columns
    df_table.loc[:,'券种利差'] = round(df_table.loc[:,'券种利差'],2)
    if clickData == None:
         clickData = {'points':[{'customdata':'上海大宁资产经营(集团)有限公司'}]}
    dff = df_table[df_table['主体名称'] == clickData["points"][0]["customdata"]]
 #    dff2 = dff.drop(['主体名称'],axis = 1)
    
    return dff.to_dict("records")


