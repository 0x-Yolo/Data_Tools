# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:29:25 2020

@author: User
"""
import sys
from modular.macro_prediction import change_freq,seasonal,add_SF
import modular.db_management.data_organize as do
 
import plotly
import plotly.graph_objs as go
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
#导入模型库
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.stattools as st
from statsmodels.tsa.arima_model import ARMA,ARIMA
from itertools import product


#%%
    
def CPI_model(df,date,verbose = 0):
    # 食品
    pig = df[['平均批发价:猪肉:月:环比','CPI:食品烟酒:畜肉类:猪肉:环比']]
    beef = df[['平均批发价:牛肉:月:环比','CPI:食品烟酒:畜肉类:牛肉:环比']]
    veg = df[['前海农产品批发价格指数:蔬菜:月:环比','CPI:食品烟酒:鲜菜:环比']]
    food = [pig,beef,veg]
    pre = np.zeros(shape = (1,4))
    est_summary = []
    for i,df_food in enumerate(food):
        df_food = add_SF(df_food)
        df2 = sm.add_constant(df_food)
        df2 = df2.fillna(0)
        df_train = df2[(df2.index > '2013-12-01')&(df2.index < date)]
        x_test = np.asarray(df2[df2.index == date].iloc[:,[0,1,3]],'float32').reshape(1,-1)
        y = np.asarray(df_train.iloc[:,2],'float32')
        x = np.asarray(df_train.iloc[:,[0,1,3]],'float32')
        est = sm.OLS(y, x).fit()
        pre[0,i] = est.predict(x_test)[0] 
        est_summary.append(est.summary())
    # 非食品
    CPI_non_food = df[(df.index>'2013-12-01')&(df.index<=date)]['CPI:非食品:环比']
    days = CPI_non_food.index
    ndays = len(days)
    x_PPI_lag8 = df['PPI:生产资料:环比'].shift(8)
    x_blent = df['期货结算价(活跃合约):MICEX 布伦特原油:月:环比']
    x_blent_lag1 = df['期货结算价(活跃合约):MICEX 布伦特原油:月:环比'].shift(1)
#    x_blent_lag3 = df['期货结算价(活跃合约):MICEX 布伦特原油:月:环比'].shift(3)    
    x_gas_lag2 = df['期货结算价(活跃合约):IPE英国天然气:月:环比'].shift(2)
    CPI_non_food_x = pd.concat([x_PPI_lag8,x_blent,x_blent_lag1,x_gas_lag2],axis = 1).fillna(0)
    CPI_non_food_x = add_SF(CPI_non_food_x)
    CPI_non_food_x = CPI_non_food_x[CPI_non_food_x.index>'2013-12-01']
    sea = seasonal(CPI_non_food[CPI_non_food.index<date])
    trend = CPI_non_food[CPI_non_food.index<date]-sea
    y_non_food = np.asarray(trend[trend.index<date],'float32')
    x_non_food = np.asarray(CPI_non_food_x[CPI_non_food_x.index<date],'float32')
    x_non_food_test = np.asarray(CPI_non_food_x[CPI_non_food_x.index==date],'float32').reshape(1,-1)
    est_non_food = sm.OLS(y_non_food,x_non_food).fit()
    pre[0,3] = est_non_food.predict(x_non_food_test)[0]+sea[-1]
    est_summary.append(est_non_food.summary())
    if verbose == 1:
        print(est_non_food.summary())
    # 系数
    CPI_agg = df[(df.index>'2013-12-01')&(df.index<date)][['CPI:食品烟酒:畜肉类:猪肉:环比','CPI:食品烟酒:畜肉类:牛肉:环比','CPI:食品烟酒:鲜菜:环比','CPI:非食品:环比','CPI:环比']]
    x_agg = np.asarray(CPI_agg.iloc[:,:-1],'float32')
    y_agg = np.asarray(CPI_agg.iloc[:,-1],'float32')
    est_agg = sm.OLS(y_agg,x_agg).fit()
    summary = pd.DataFrame({'系数':est_agg.params,
                                    'p值':est_agg.pvalues})                                  # 新建df记录各行业系数和p值
    print("即将输出各分项系数...")
    print(summary)                                  
    # 整合
    CPI = df[(df.index>'2013-12-01')&(df.index<=date)][['CPI:环比','CPI:当月同比']]
    CPI.loc[date,'CPI:环比'] = est_agg.predict(pre)[0]
    CPI.loc[date,'CPI:当月同比'] = ((CPI.iloc[-12:-1,0]/100+1).prod()*(est_agg.predict(pre)[0]/100+1)-1)*100
    
    return CPI

#%%
    
def CPI_model2(df,date):
    df = df.fillna(0)
    pre = np.zeros(shape = (1,7))
    # 食品
    pig = df[['平均批发价:猪肉:月:环比','CPI:食品烟酒:畜肉类:猪肉:环比']]
    beef = df[['平均批发价:牛肉:月:环比','CPI:食品烟酒:畜肉类:牛肉:环比']]
    veg = df[['前海农产品批发价格指数:蔬菜:月:环比','CPI:食品烟酒:鲜菜:环比']]
    food = [pig,beef,veg]    
    est_summary = []
    for i,df_food in enumerate(food):
        df_food = add_SF(df_food)
        df2 = sm.add_constant(df_food)
        df2 = df2.fillna(0)
        df_train = df2[(df2.index > '2013-12-01')&(df2.index < date)]
        x_test = np.asarray(df2[df2.index == date].iloc[:,[0,1,3]],'float32').reshape(1,-1)
        y = np.asarray(df_train.iloc[:,2],'float32')
        x = np.asarray(df_train.iloc[:,[0,1,3]],'float32')
        est = sm.OLS(y, x).fit()
        pre[0,i] = est.predict(x_test)[0] 
        est_summary.append(est.summary())
    # 交通工具用燃料
    fuel_x = pd.concat([df['最高零售指导价:柴油:月:环比'].shift(1),df['最高零售指导价:柴油:月:环比']],axis = 1).dropna()
    fuel_y = np.asarray(df[(df.index>'2013-12-01')&(df.index<date)]['CPI:交通和通信:交通工具用燃料:环比'],'float32')
    fuel_x_train = np.asarray(fuel_x[(fuel_x.index>'2013-12-01')&(fuel_x.index<date)],'float32')
    fuel_x_test = np.asarray(fuel_x[fuel_x.index == date],'float32').reshape(1,-1)    
    est_fuel = sm.OLS(fuel_y, fuel_x_train).fit()
    pre[0,3] = est_fuel.predict(fuel_x_test)[0]
    est_summary.append(est_fuel.summary())
    # 生活水电用燃料
    chaiyou = df[(df.index > '2013-11-01')&(df.index <= date)]['最高零售指导价:柴油:月:环比']
    chaiyou_trend = chaiyou - seasonal(chaiyou)
    chaiyou_x = pd.concat([chaiyou_trend.shift(1),chaiyou_trend],axis = 1).dropna()
    energy = df[(df.index > '2013-12-01')&(df.index <= date)]['CPI:居住:水电燃料:环比']
    energy_sea = seasonal(energy)
    energy_trend = energy - energy_sea
    energy_y = np.asarray(energy_trend[energy_trend.index<date],'float32')
    energy_x_train = np.asarray(chaiyou_x[chaiyou_x.index<date],'float32')
    energy_x_test = np.asarray(chaiyou_x[chaiyou_x.index == date],'float32').reshape(1,-1)
    est_energy = sm.OLS(energy_y, energy_x_train).fit()
    pre[0,4] = est_energy.predict(energy_x_test)[0]+energy_sea[date]
    est_summary.append(est_fuel.summary())
    # 衣着和教育
    cloth = df[(df.index > '2013-12-01')&(df.index <= date)]['CPI:衣着:环比']
    edu = df[(df.index > '2013-12-01')&(df.index <= date)]['CPI:教育文化和娱乐:环比']
    pre[0,5] = seasonal(cloth)[date]
    pre[0,6] = seasonal(edu)[date]
    # 系数
    CPI_agg = df[(df.index>'2013-12-01')&(df.index<date)][['CPI:食品烟酒:畜肉类:猪肉:环比','CPI:食品烟酒:畜肉类:牛肉:环比','CPI:食品烟酒:鲜菜:环比',
                                                           'CPI:交通和通信:交通工具用燃料:环比','CPI:居住:水电燃料:环比','CPI:衣着:环比',
                                                           'CPI:教育文化和娱乐:环比','CPI:环比']]
    x_agg = np.asarray(CPI_agg.iloc[:,:-1],'float32')
    y_agg = np.asarray(CPI_agg.iloc[:,-1],'float32')
    est_agg = sm.OLS(y_agg,x_agg).fit()
    summary = pd.DataFrame({'系数':est_agg.params,
                                    'p值':est_agg.pvalues})                                  # 新建df记录各行业系数和p值
    print("即将输出各分项系数...")
    print(summary)                                  
    # 整合
    CPI = df[(df.index>'2013-12-01')&(df.index<=date)][['CPI:环比','CPI:当月同比']]
    CPI.loc[date,'CPI:环比'] = est_agg.predict(pre)[0]
    CPI.loc[date,'CPI:当月同比'] = ((CPI.iloc[-12:-1,0]/100+1).prod()*(est_agg.predict(pre)[0]/100+1)-1)*100
    
    return CPI

#%%

def main():
    hf = do.get_data('high_frequency_for_prediction')
    hf.set_index(['date'],inplace = True)
    hf.index = pd.DatetimeIndex(hf.index)
    mv = do.get_data('Macro_variables_month')
    mv.set_index(['date'],inplace = True)
    mv.index = pd.DatetimeIndex(mv.index)
    hf_month = change_freq(hf, freq = 'M', how = 'mean', percent = 'mom')
    macro_data_all = pd.concat([hf_month,mv],axis = 1)
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    begin_date = (today-timedelta(days=180)).strftime('%Y-%m-%d')
    date_index = pd.date_range(begin_date, end_date,freq = 'M')
    pre_Date = [pd.Timestamp(x).strftime("%Y-%m-%d") for x in date_index.values]
    train = macro_data_all[(macro_data_all.index > '2015-01-01')&(macro_data_all.index < pre_Date[0])][['CPI:当月同比','CPI:环比']]
    test = macro_data_all[macro_data_all.index >= pre_Date[0]][['CPI:当月同比','CPI:环比']]
    pred = np.zeros(shape = (len(pre_Date),4))
    for i,date in enumerate(pre_Date):
        pred[i,[0,2]] = CPI_model2(macro_data_all,date).iloc[-1,:]
        pred[i,[1,3]] = CPI_model(macro_data_all,date).iloc[-1,:]
    pred_df = pd.DataFrame(pred,columns = ['环比预测1','环比预测2','同比预测1','同比预测2'])
    pred_df['date'] = pre_Date
    pred_df['CPI同比真实值'] = list(test[(test.index >= pre_Date[0])&(test.index <= pre_Date[-1])]['CPI:当月同比'])
    pred_df['CPI环比真实值'] = list(test[(test.index >= pre_Date[0])&(test.index <= pre_Date[-1])]['CPI:环比'])
    
    trace1 = go.Scatter(
            x=train.index,
            y=train['CPI:当月同比'],
            name = '训练集真实值'
        )
    trace2 = go.Scatter(
        x=test.index,
        y=test['CPI:当月同比'],
        name = '测试集真实值'
    )
    trace3 = go.Scatter(
            x=pred_df['date'],
            y=pred_df['同比预测1'],
            name = '模型一（七分项）预测值', 
            mode="markers"
           )
    trace4 = go.Scatter(
            x=pred_df['date'],
            y=pred_df['同比预测2'],
            name = '模型二（四分项）预测值', 
            mode="markers"
           )
    
    d = [trace1,trace2, trace3,trace4]
    layout = go.Layout(title =dict(text = 'CPI跟踪与预测',
                                    x = 0.5),
                       legend=dict(orientation="h")
)
    fig = go.Figure(data = d,layout = layout)
    graph = dcc.Graph(id='CPI_fig',figure=fig)
    table = dash_table.DataTable(
                              id = 'CPI_table',
                              columns=[
        {"name": ["", "日期"], "id": "date"},
        {"name": ["环比", "真实值"], "id": "CPI环比真实值"},
        {"name": ["环比", "模型一(七分项)"], "id": "环比预测1"},
        {"name": ["环比", "模型二(四分项)"], "id": "环比预测2"},
        {"name": ["同比", "真实值"], "id": "CPI同比真实值"},
        {"name": ["同比", "模型一(七分项)"], "id": "同比预测1"},
        {"name": ["同比", "模型二(四分项)"], "id": "同比预测2"},
    ]
                                  ,
                              data=round(pred_df,2).to_dict('record'),
                              merge_duplicate_headers=True,
                              style_cell={
        # all three widths are needed
        'minWidth': '120px', 'width': '120px', 'maxWidth': '120px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    }
 #                             style_as_list_view=True,
                              # style_cell_conditional=[
                              #                   {
                              #                       'if': {'column_id': c},
                              #                       'textAlign': 'left'
                              #                   } for c in ['Date', 'Region']
                              #               ],
                              #               style_data_conditional=[
                              #                   {
                              #                       'if': {'row_index': 'odd'},
                              #                       'backgroundColor': 'rgb(248, 248, 248)'
                              #                   }
                              #               ],
                              #               style_header={
                              #                   'backgroundColor': 'rgb(230, 230, 230)',
                              #                   'fontWeight': 'bold'
                              #               }
                              )
                            
    CPI_layout = html.Div(
        [
            html.H6(children='CPI'),
            html.Div(graph),
            html.Div(table)]
        )
    
    return CPI_layout

#%%
    
if __name__ == '__main__':
    main()
    
    

    
    