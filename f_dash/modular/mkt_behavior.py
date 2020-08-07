import re
import sys
import datetime as dt
import pandas as pd
import  pymysql

#导入plotly库
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# from WindPy import w



# #图一： 设置多日期看债券市场转移：返回图像和数据
# def daily_bond_transform(dates,duration,bond_type):
#     conn = pymysql.connect(
#         host = '47.116.3.109',	
#         user = 'user1',	
#         passwd = '123456',	
#         db = 'finance',	
#         port=3306,	
#         charset = 'utf8'	
#     )
#     df = pd.read_sql('select * from Net_buy_bond',conn)
#     if type(dates)==tuple:
#         df_cut_t = pd.DataFrame()
#         for date in dates:
#             df_cut_t = df_cut_t.append(df[(df["date"]==date)&(df["期限"]==duration)])
#         df_cut = df_cut_t.groupby("机构名称").aggregate(sum).round(decimals=2)
#         df_cut["机构名称"] = df_cut.index
#         df_cut = df_cut.sort_values(by=bond_type,ascending = True)

#     elif type(dates)==str:
#         df_cut = df[(df["date"]==dates)&(df["期限"]==duration)]
#         df_cut = df_cut.sort_values(by=bond_type,ascending = True)


#     df_out =df_cut[df_cut[bond_type]<=0]
#     df_in = df_cut[df_cut[bond_type]>0]

#     source = list(range(len(df_out)))+len(df_in)*[len(df_cut)+1]
#     target = (len(df_out)*[len(df_cut)+1]+list(range(len(df_out),len(df_cut))))
#     value = list(-df_out[bond_type])+list(df_in[bond_type])
#     label = df_cut["机构名称"]

#     fig = go.Figure(data=[go.Sankey(
#         arrangement = "snap",
#         node = dict(
#         #   pad = 15,
#         #   thickness = 20,
#         #   line = dict(color = "black", width = 0.5),
#         label = label,
#         #   color = "blue"
#         ),
#         link = dict(
#         source = source, 
#         target = target,
#         value = value,
#         ))])
#     fig.update_layout(title_text=duration+bond_type+"<br>市场筹码转移图<a href='www.baidu.com'>@太平洋证券</a>",font_size=10)

#     return fig,df_cut

#图二
def Fig_Net_buy_bond(bond_buyer,bond_duration,bond_type):
    conn = pymysql.connect(
    host = '47.116.3.109',	
    user = 'user1',	
    passwd = '123456',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8')

    df = pd.read_sql('select * from Net_buy_bond',conn)


    dff = df[df["期限"].isin(list(bond_duration))]
    dff = dff[dff["机构名称"]==bond_buyer]
    dff["sum"]=list(dff[bond_type].sum(axis=1))
    dfff = pd.DataFrame(dff,columns=bond_type+["机构名称","期限","合计","sum","date"])

    data = []
    for term in list(bond_duration):
        data.append(
            go.Bar(name=term,
                    x = pd.to_datetime(dfff["date"].unique()).strftime("%Y-%m-%d"),
                    y = dfff[dfff["期限"]==term]["sum"]
               ))
    fig=go.Figure(data=data)
    fig.update_layout(
        title='机构净买入表现',
        yaxis=dict(
        title='亿元',
        titlefont_size=16,
        tickfont_size=14,)
    )
    fig.update_xaxes(
                     rangebreaks=[
                dict(bounds=["sat","mon"]), #hide weekends  
                     ])
    return fig

#图三
def Fig_Repo_amt_prc_for_terms(repo_loaner,repo_terms,flow_or_abs_repo_amt):
    conn = pymysql.connect(	
    host = '47.116.3.109',	
    user = 'user1',	
    passwd = '123456',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8'	
)	
    df = pd.read_sql('select * from Repo_amt_prc_for_terms',conn)
    df["回购余额"]=df["正回购余额(百万)"]-df["逆回购余额(百万)"]
    dff = df[df["期限品种"].isin(list(repo_terms))]#选中的期限
    data=[]
    for x in repo_terms:
        data.append(go.Bar(name= x,
                        x = list(pd.to_datetime(dff["date"].unique()).strftime("%Y-%m-%d")),
                        y = list(pd.DataFrame(dff[(dff["机构类型"]==repo_loaner)&(dff["期限品种"]==x)],columns=[flow_or_abs_repo_amt]).iloc[:,0]/100)
                   ))
    fig=go.Figure(data=data)
    fig.update_layout(
        title='机构质押回购表现',
        yaxis=dict(
        title='亿元',
        titlefont_size=16,
        tickfont_size=14,)
    )
    fig.update_xaxes(
                     rangebreaks=[
                dict(bounds=["sat","mon"]), #hide weekends  
                     ])
    return fig.to_dict()


def fig_margin_newfund_scale():
    fig=go.Figure()
    conn = pymysql.connect(
    host = '47.116.3.109',	
    user = 'dngj',	
    passwd = '603603',	
    db = 'finance',	
    port=3306,	
    charset = 'utf8mb4'	
)
    dff = pd.read_sql('select * from margin_newfund_scale',conn)
    df=dff.iloc[:,:-1]
    date=dff["date"] 
    for column in df.columns:
        fig.add_trace(go.Bar(name=column[:-2],x=date, y=df[column]))
    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.update_layout(title="新发基金规模(亿元)")
    return fig


def fig_margin_newfund_amt():
    fig=go.Figure()
    data=[]
    conn = pymysql.connect(
        host = '47.116.3.109',	
        user = 'user1',	
        passwd = '123456',	
        db = 'finance',	
        port=3306,	
        charset = 'utf8'	
    )
    dff = pd.read_sql('select * from margin_newfund_amt',conn)
    df=dff.iloc[:,:-1]
    data=dff["date"] 
    for column in df.columns:
        fig.add_trace(go.Bar(name=column[:-2],x=data, y=df[column]))
    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.update_layout(title="新发基金数量(个数)")
    return fig

def fig_margin_newfund_amt_slider():
    
    conn = pymysql.connect(
        host = '47.116.3.109',	
        user = 'user1',	
        passwd = '123456',	
        db = 'finance',	
        port=3306,	
        charset = 'utf8'	
    )
    df = pd.read_sql('select * from net_assets_fund_type',conn).round(decimals=2)
    return df["date"]


def fig_net_assets_fund_type(date_slider_fig_net_assets_fund_type):
    conn = pymysql.connect(
        host = '47.116.3.109',	
        user = 'user1',	
        passwd = '123456',	
        db = 'finance',	
        port=3306,	
        charset = 'utf8'	
    )
    df = pd.read_sql('select * from net_assets_fund_type',conn).round(decimals=2)

    dff=df[df["date"]==date_slider_fig_net_assets_fund_type].iloc[:,:-1]
    labels=[]
    for column in dff.columns:
        labels.append(column[:-2])
    values=dff.values[0]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0.2, 0,0])])
    fig.update_layout(showlegend=False,title="存量基金占比（亿元，%）")
    return fig
        