# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 14:12:12 2020

@author: User
"""


import sys
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from modular.macro_prediction import change_freq,seasonal,add_SF
import modular.db_management.data_organize as do
 
import plotly
import plotly.graph_objs as go
import abc
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.stattools as st
from statsmodels.tsa.arima_model import ARMA,ARIMA
from itertools import product
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html



#%%
def choose_best_ARMA(df):
    ps = range(0, 4)
    qs = range(0, 4)
    parameters = product(ps, qs)
    parameters_list = list(parameters)
    best_aic = float('inf')
    results = []
    for param in parameters_list:
        try:
            model = ARMA(df, order=(param[0], param[1])).fit()
        except ValueError:
            continue
        aic = model.aic
        if aic < best_aic:
            best_model = model
            best_aic = model.aic
            best_param = param
        results.append([param, model.aic])
    results_table = pd.DataFrame(results)
    results_table.columns = ['parameters', 'aic']
    return best_model

#%%
    
class model(object,metaclass = abc.ABCMeta): # 抽象基类
    
    @abc.abstractmethod    
    def PPI_by_Industry(self,industry_names,verbose = 0):
        # 分别预测重要行业的PPI，再将其拟合成最终的PPI
        pass
    
    @abc.abstractmethod    
    def PPI_by_PMI(self,verbose = 0):
        # 通过PMI:主要原材料购进价格来预测PPI环比
        pass
    
class PPI_model(model):
    
    def __init__(self,workbook,date):
        self.workbook = workbook
        self.date = date
   
    def PPI_by_Industry(self,verbose = 0):
        industry_names = list(self.workbook.keys())[0:-1]
        nmonths = 1                                                                        # 预测的总月份数 
        PPI_by_industry_pre = np.zeros(shape=(nmonths,len(industry_names)))                # 新建数组来记录预测值
    
        ######## 对行业分别进行预测 ########
    
        for i,name in enumerate(industry_names):
            df = self.workbook[name].fillna(0)                                                        # 通过名称获取
            df_train = df[(df.index > '2014-02-28')&(df.index < self.date)]                                              # 用date以前的数据建模
            df_test = df[df.index == self.date]                                              # 预测date
            y = np.asarray(df_train.iloc[:,-1])
            x = df_train.iloc[:,:-1]
            x2 = sm.add_constant(x)                                                         # 添加常数1
            est = sm.OLS(y, x2).fit()                                                       # 建模  
            x_test = sm.add_constant(np.asarray(df_test.iloc[:,:-1]), has_constant='add')                                    # 添加常数1
            PPI_by_industry_pre[:,i] = est.predict(x_test)                                  # 逐列添加每个行业的预测值       
            if verbose == 1:                                                                # 如果 verbose=1，输出模型细节
                print(name,"的修正R方为",'{:.2%}'.format(est.rsquared_adj))                                        # 输出修正R方
                summary = pd.DataFrame({
                                    '系数':est.params[1:],
                                    'p值':est.pvalues[1:]})                                  # 新建df记录系数和p值
                print(summary)                                                               # 输出系数和p值
        
    
        ######## 计算各行业的系数并拟合总体PPI ########
                
        agg_x = self.workbook['煤炭'].iloc[:,-1].fillna(0)
        agg_y = self.workbook['PMI数据']['PPI:全部工业品:环比'].fillna(0)
        agg_y = agg_y[(agg_y.index>'2013-12-01')&(agg_y.index < self.date)]
        for i in range(1,len(industry_names)):
            agg_x = pd.concat([agg_x,self.workbook[industry_names[i]].iloc[:,-1]],axis = 1)
        agg_x = agg_x[(agg_x.index > '2013-12-01')&(agg_x.index < self.date)]
        x2 = np.asarray(sm.add_constant(agg_x))                                                  # 添加常数1
        y = np.asarray(agg_y)
        est_coef = sm.OLS(y, x2).fit()                                                       # 建模  
        summary = pd.DataFrame({'系数':est_coef.params,
                                    'p值':est_coef.pvalues})                                  # 新建df记录各行业系数和p值
        print("即将输出各行业系数...")
        print(summary)  
        a = np.ones(shape = (1,1))                                                                      # 输出各行业系数和p值
        x_test_final = np.hstack([a,PPI_by_industry_pre])
        PPI = self.workbook['PMI数据'][['PPI:全部工业品:环比','PPI:全部工业品:当月同比']]
        PPI.index = pd.DatetimeIndex(PPI.index)
        PPI = PPI[(PPI.index>'2013-12-01')&(PPI.index < self.date)]
        ######## 环比数据转为同比数据 ########  
        PPI.loc[self.date,'PPI:全部工业品:环比'] = est_coef.predict(x_test_final)
        PPI.loc[self.date,'PPI:全部工业品:当月同比'] = ((PPI.iloc[-12:-1,0]/100+1).prod()*(est_coef.predict(x_test_final)/100+1)-1)*100
 
        return PPI                                                                        # 返回所有PPI环比和同比
    
    def PPI_by_PMI(self,verbose = 0):
        
        
        df = self.workbook["PMI数据"][['PMI:主要原材料购进价格','PPI:全部工业品:环比']].fillna(0)
        df.columns = ['PMI','y']
        df.index = pd.DatetimeIndex(df.index)
        # df_train = df[df.index < '2018-05-31']                                  # 设定2019年5月以前的数据作训练集
        # df_test = df[df.index >= '2018-05-31']                                  # 设定2019年5月以后的数据作测试集   
        # train_latest_start = '2015-05-01'                                       # 设定训练集的开始时间不能晚于2016年5月
        # train_start_tp = df.index[df.index < train_latest_start]                            # 训练集开始时间集合         
        # mse = 0                                                                 # 首先设定MSE=0
        # for i in train_start_tp:                                                # 遍历训练集开始时间集合中的每一天
        #     train_set = df_train[df_train.index >= i]
        #     test_set = df_test
        #     model = smf.ols('y~PMI',train_set).fit()                          
        #     y_pred = model.predict(test_set.PMI)                                
        #     if mse == 0:
        #         mse = ((y_pred - test_set.y)**2).mean()
        #     elif (((y_pred - test_set.y)**2).mean() < mse ):
        #         mse = ((y_pred - test_set.y)**2).mean()
        #         start = i                                                       # 记录更优的建模开始时间
        #         linear_model_best = model                                       # 记录更优的回归模型
        # print("从",start,"开始建模...")
        
        ######## 建立回归模型 ########
        
        df_final = df[(df.index >= '2008-07-01')&(df.index < self.date)]
        y = np.asarray(df_final.iloc[:,1],'float32')
        x = df_final.iloc[:,0]
        x2 = sm.add_constant(x)                                                         # 添加常数1
        est = sm.OLS(y, x2).fit()
        reg_model = smf.ols('y~PMI',df_final).fit()                             # 建模    
        y_reg_pre = reg_model.params[0]+reg_model.params[1]*df.loc[self.date,'PMI']
        
        
        ######## 对回归残差拟合ARMA模型 ########
        
        df_res = pd.DataFrame(reg_model.resid)
        df_res.index = pd.DatetimeIndex(reg_model.resid.index,freq = 'M')
        best_ARMA = choose_best_ARMA(df_res)
        res_pre = best_ARMA.forecast(steps = 1)[0]
        PPI_mom_pre = y_reg_pre+res_pre
        if verbose == 1:
            print('回归模型：')
            print(reg_model.summary())
            print('ARMA模型：')
            print(best_ARMA.summary())
        ######## 环比数据转为同比数据 ########  
        PPI = self.workbook['PMI数据'][['PPI:全部工业品:环比','PPI:全部工业品:当月同比']]
        PPI.index = pd.DatetimeIndex(PPI.index)
        PPI = PPI[(PPI.index>'2013-12-01')&(PPI.index < self.date)]
        ######## 环比数据转为同比数据 ########  
        PPI.loc[self.date,'PPI:全部工业品:环比'] = PPI_mom_pre
        PPI.loc[self.date,'PPI:全部工业品:当月同比'] = ((PPI.iloc[-12:-1,0]/100+1).prod()*(PPI_mom_pre/100+1)-1)*100
     
        return PPI    
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
    PPI_data = {
        '煤炭': pd.concat([
        hf_month['综合平均价格指数:环渤海动力煤(Q5500K):月:环比'].shift(1),
        hf_month['综合平均价格指数:环渤海动力煤(Q5500K):月:环比'].shift(2),
        hf_month['期货结算价(活跃合约):焦煤:月:环比'],
        hf_month['期货结算价(活跃合约):焦煤:月:环比'].shift(1),
        hf_month['期货结算价(活跃合约):焦煤:月:环比'].shift(2),
        mv['PPI:煤炭开采和洗选业:环比']
        ],axis = 1),
        '石油和天然气开采业': pd.concat([
        hf_month['期货结算价(活跃合约):MICEX 布伦特原油:月:环比'].shift(1),
    	hf_month['期货结算价(活跃合约):IPE英国天然气:月:环比'],	
        hf_month['期货结算价(连续):WTI原油:月:环比'],
        hf_month['期货结算价(连续):WTI原油:月:环比'].shift(2),
        mv['PPI:石油和天然气开采业:环比']
        ],axis = 1),
        '石油加工炼焦':pd.concat([
        hf_month['期货结算价(活跃合约):MICEX 布伦特原油:月:环比'],
       	hf_month['期货结算价(活跃合约):MICEX 布伦特原油:月:环比'].shift(1),
        hf_month['期货结算价(活跃合约):IPE英国天然气:月:环比'],
      	hf_month['钻机数量:总计:美国:当周值:月:环比'],
        mv['PPI:石油、煤炭及其他燃料加工业:环比']
        ],axis = 1),
        '有色冶炼':pd.concat([
        hf_month['期货结算价(活跃合约):阴极铜:月:环比'],
       	hf_month['期货结算价(活跃合约):铝:月:环比'],
        hf_month['期货结算价(活跃合约):铝:月:环比'].shift(1),
      	hf_month['总库存:LME铝:月:环比'],
        hf_month['上期有色金属指数:月:环比'].shift(1),
        mv['PPI:有色金属冶炼及压延加工业:环比']
        ],axis = 1),
        '化学原料及化学品':pd.concat([
        hf_month['期货结算价(活跃合约):甲醇:月:环比'],
       	hf_month['期货结算价(活跃合约):甲醇:月:环比'].shift(1),
        hf_month['期货结算价(活跃合约):甲醇:月:环比'].shift(2),
      	hf_month['期货结算价(活跃合约):聚丙烯:月:环比'].shift(1),
        hf_month['期货结算价(活跃合约):聚丙烯:月:环比'].shift(3),
        hf_month['期货结算价(活跃合约):燃料油:月:环比'],
        mv['PPI:化学原料及化学制品制造业:环比']
        ],axis = 1),
        '化学纤维':pd.concat([
        hf_month['市场价(中间价):涤纶长丝(POY 150D/48F):国内市场:月:环比'],
       	hf_month['市场价(中间价):涤纶长丝(POY 150D/48F):国内市场:月:环比'].shift(1),
        hf_month['CCFEI价格指数:涤纶短纤:月:环比'].shift(1),
      	hf_month['CCFEI价格指数:涤纶短纤:月:环比'].shift(2),
        hf_month['CCFEI价格指数:涤纶短纤:月:环比'].shift(3),
        mv['PPI:化学纤维制造业:环比']    
        ],axis = 1),
        '黑色金属矿采':pd.concat([
        hf_month['中国铁矿石价格指数(CIOPI):国产铁矿石:月:环比'],
       	hf_month['中国铁矿石价格指数(CIOPI):国产铁矿石:月:环比'].shift(1),
       	hf_month['中国铁矿石价格指数(CIOPI):国产铁矿石:月:环比'].shift(2),
      	hf_month['全国主要港口:铁矿石库存:原口径(30港口):月:环比'],
        mv['PPI:黑色金属矿采选业:环比'],          
        ],axis = 1),
        '黑色加工':pd.concat([
        hf_month['Myspic综合钢价指数:月:环比'],
       	hf_month['Myspic综合钢价指数:月:环比'].shift(1),
       	hf_month['Myspic综合钢价指数:月:环比'].shift(2),
        mv['PPI:黑色金属冶炼及压延加工业:环比'],          
        ],axis = 1),
        '农副':pd.concat([
        hf_month['22个省市:平均价:猪肉:月:环比'],
       	hf_month['22个省市:平均价:猪肉:月:环比'].shift(3),
       	hf_month['期货结算价(活跃合约):菜籽油:月:环比'],
        hf_month['平均批发价:羊肉:月:环比'],
        mv['CPI:食品烟酒:畜肉类:猪肉:环比'],
        mv['CPI:食品烟酒:畜肉类:猪肉:环比'].shift(3),
        mv['PPI:农副食品加工业:环比'],          
        ],axis = 1),
        '非金属矿物制品业':pd.concat([
        hf_month['水泥价格指数:全国:月:环比'],
       	hf_month['水泥价格指数:全国:月:环比'].shift(1),
        mv['PPI:非金属矿物制品业:环比'],          
        ],axis = 1),
        'PMI数据': mv[['PMI:主要原材料购进价格','PPI:全部工业品:当月同比','PPI:全部工业品:环比']] 
    
        }
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    begin_date = (today-timedelta(days=180)).strftime('%Y-%m-%d')
    date_index = pd.date_range(begin_date, end_date,freq = 'M')
    pre_Date = [pd.Timestamp(x).strftime("%Y-%m-%d") for x in date_index.values]
    train = mv[(mv.index > '2015-01-01')&(mv.index < pre_Date[0])][['PPI:全部工业品:当月同比','PPI:全部工业品:环比']]
    test = mv[mv.index >= pre_Date[0]][['PPI:全部工业品:当月同比','PPI:全部工业品:环比']]
    pred = np.zeros(shape = (len(pre_Date),4))
    for i,date in enumerate(pre_Date):
        pred[i,[0,2]] = PPI_model(PPI_data,date).PPI_by_Industry().iloc[-1,:]
        pred[i,[1,3]] = PPI_model(PPI_data,date).PPI_by_PMI().iloc[-1,:]
    pred_df = pd.DataFrame(pred,columns = ['环比预测1','环比预测2','同比预测1','同比预测2'])
    pred_df['date'] = pre_Date
    pred_df['PPI同比真实值'] = list(test[(test.index >= pre_Date[0])&(test.index <= pre_Date[-1])]['PPI:全部工业品:当月同比'])
    pred_df['PPI环比真实值'] = list(test[(test.index >= pre_Date[0])&(test.index <= pre_Date[-1])]['PPI:全部工业品:环比'])
        
    trace1 = go.Scatter(
            x=train.index,
            y=train['PPI:全部工业品:当月同比'],
            name = '训练集真实值'
        ) 
    trace2 = go.Scatter(
            x=test.index,
            y=test['PPI:全部工业品:当月同比'],
            name = '测试集真实值'
        )
    trace3 = go.Scatter(
            x=pred_df['date'],
            y=pred_df['同比预测1'],
            name = '分行业预测值', 
            mode="markers"
           )
    trace4 = go.Scatter(
            x=pred_df['date'],
            y=pred_df['同比预测2'],
            name = 'PMI预测值',  
            mode="markers"
           )
    
    d = [trace1,trace2,trace3,trace4]
    layout = go.Layout(title =dict(text = 'PPI跟踪与预测',
                                x = 0.5),
                   legend=dict(orientation="h")
)
    fig = go.Figure(data = d,layout = layout)    
    graph = dcc.Graph(
        id='PPI_fig',
        figure=fig
    )
    table = dash_table.DataTable(
                         id = 'PPI_table',
                         columns=[
   {"name": ["", "日期"], "id": "date"},
   {"name": ["环比", "真实值"], "id": "PPI环比真实值"},
   {"name": ["环比", "模型一(分行业)"], "id": "环比预测1"},
   {"name": ["环比", "模型二(PMI)"], "id": "环比预测2"},
   {"name": ["同比", "真实值"], "id": "PPI同比真实值"},
   {"name": ["同比", "模型一(分行业)"], "id": "同比预测1"},
   {"name": ["同比", "模型二(PMI)"], "id": "同比预测2"},
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
                            
    PPI_layout = html.Div(
        [
            html.H6(children='PPI'),
            html.Div(graph),
            html.Div(table)]
        )
    
    return PPI_layout
    

#%%
    
if __name__ == '__main__':
    main()
    
    
    