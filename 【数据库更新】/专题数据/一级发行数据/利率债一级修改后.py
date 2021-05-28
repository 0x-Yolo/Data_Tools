import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=True)
import warnings
warnings.filterwarnings('ignore')
import plotly as py
import plotly.graph_objs as go
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from matplotlib.backends.backend_pdf import PdfPages

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()
cf.set_config_file(offline=True, world_readable=True)

df = pd.read_excel('/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/wind专题数据/一级发行数据/利率债一级-0518.xlsx',sheet_name = '数据（导入）')

# 这步是用来去除异常值的，之后有啥异常值还可以在这边改。
df = df[df['综收较估值'] < 40]

df_gk = df[df['发行人全称']=='国家开发银行'][['发行起始日','发行期限(年)','发行人全称','全场倍数','综收较估值','综收较二级']]
# 全场倍数的25\50\75分位数 
qcbs_quantile_gk = df_gk.groupby('发行期限(年)').apply(lambda df:np.nanquantile(df['全场倍数'],[0.25,0.5,0.75]))

def GK():
    fig_list = []

    df_gk = df[df['发行人全称']=='国家开发银行'][['发行起始日','发行期限(年)','发行人全称','全场倍数','综收较估值','综收较二级']]
    # 全场倍数的25\50\75分位数 
    qcbs_quantile_gk = df_gk.groupby('发行期限(年)').apply(lambda df:np.nanquantile(df['全场倍数'],[0.25,0.5,0.75]))

    maturity = [1,3,5,7,10,15,20]
    pyplt = py.offline.plot

    for ii in range(1,8):
        i = maturity[ii-1]   # 遍历不同期限
        temp = df_gk[df_gk['发行期限(年)']==i]
        trace1 = go.Scatter(
            x = temp['发行起始日'],
            y = temp['全场倍数'],
            fill = 'tozeroy',
            mode= 'none',# 无边界线
            name = "全场倍数",
            fillcolor = 'Lightblue'
        )
        trace2 = go.Scatter(
            x = temp['发行起始日'],
            y = temp['综收较估值'],
            mode= 'markers',# 无边界线
            name = "综收较估值",
            yaxis="y2",
            line = {'color': 'Chocolate'}
        )
    #    trace3 =  go.Scatter(
    #        x = temp['发行起始日'],
    #        y = temp['综收较二级'],
    #        mode= 'lines',# 无边界线
    #        name = "综收较二级",
    #        yaxis="y2",
    #        line = {'color':'Cadetblue'}
    #    )
        trace4 = go.Scatter(
            x = temp['发行起始日'],
            y = np.tile(qcbs_quantile_gk[qcbs_quantile_gk.index ==i].iloc[0][0],2000),
            mode= 'lines',
            name = "全场倍数25%",
            line={
            "width": 3,  
            "color": "Dodgerblue",  
            "dash": "dash"  # 指定为虚线
            })
        
        trace5 = go.Scatter(
            x = temp['发行起始日'],
            y = np.tile(qcbs_quantile_gk[qcbs_quantile_gk.index ==i].iloc[0][1],2000),
            mode= 'lines',
            name = "全场倍数50%",
            line={
            "width": 1,  
            "color": "Dodgerblue",  
            "dash": "dash"  # 指定为虚线
            }
        )
        trace6 =  go.Scatter(
            x = temp['发行起始日'],
            y = np.tile(qcbs_quantile_gk[qcbs_quantile_gk.index ==i].iloc[0][2],2000),
            mode= 'lines',
            name = "全场倍数75%",
            line={
            "width": 3,  
            "color": "Dodgerblue",  
            "dash": "dash"  # 指定为虚线
            }
        )
        data = [trace1, trace2,trace4,trace5,trace6]
        layout = go.Layout(title =dict(text = ''.join(['国开',str(i),'年']),
                                        x = 0.5,
                                        yanchor = 'middle') ,
                        yaxis = dict(title = '全场倍数'),
                        yaxis2 = dict(title = '综收较估值',overlaying='y', side='right'),
                        xaxis = dict( 
                        tickformat = '%Y-%m', 
                        tick0 = '2015-01-01',
                        dtick = 'M3',
                        ticks = 'inside'), # 设置每隔一季度就是一个tick
                        legend=dict(orientation="h"),
                #         height = 800,
                #        width = 1000)
                        )
            #设置图离图像四周的边距
        

        fig = go.Figure(data = data, layout = layout)#设置图像的大小
        fig_list.append(fig)
    
        # 保存
        # pyplt(fig, filename = './html/'+''.join(['国开',str(i),'年']))
    return fig_list


t = GK()



def GZ():
    df_gk = df[df['发行人全称']=='中华人民共和国财政部'][['发行起始日','发行期限(年)','发行人全称','全场倍数','综收较估值','综收较二级']]
    # 全场倍数的25\50\75分位数 
    qcbs_quantile_gk = df_gk.groupby('发行期限(年)').apply(lambda df:np.nanquantile(df['全场倍数'],[0.25,0.5,0.75]))

    maturity = [1,3,5,7,10,30,50]
    pyplt = py.offline.plot
    for i in maturity:   # 遍历不同期限
        temp = df_gk[df_gk['发行期限(年)']==i]
        trace1 = go.Scatter(
            x = temp['发行起始日'],
            y = temp['全场倍数'],
            fill = 'tozeroy',
            mode= 'none',# 无边界线
            name = "全场倍数",
            fillcolor = 'Lightblue'
        )
        trace2 = go.Scatter(
            x = temp['发行起始日'],
            y = temp['综收较估值'],
            mode= 'markers',# 无边界线
            name = "综收较估值",
            yaxis="y2",
            line = {'color': 'Chocolate'}
        )
    #    trace3 =  go.Scatter(
    #        x = temp['发行起始日'],
    #        y = temp['综收较二级'],
    #        mode= 'lines',# 无边界线
    #        name = "综收较二级",
    #        yaxis="y2",
    #        line = {'color':'Cadetblue'}
    #    )
        trace4 = go.Scatter(
            x = temp['发行起始日'],
            y = np.tile(qcbs_quantile_gk[qcbs_quantile_gk.index ==i].iloc[0][0],2000),
            mode= 'lines',
            name = "全场倍数25%",
            line={
            "width": 3,  
            "color": "Dodgerblue",  
            "dash": "dash"  # 指定为虚线
            })
        
        trace5 = go.Scatter(
            x = temp['发行起始日'],
            y = np.tile(qcbs_quantile_gk[qcbs_quantile_gk.index ==i].iloc[0][1],2000),
            mode= 'lines',
            name = "全场倍数50%",
            line={
            "width": 1,  
            "color": "Dodgerblue",  
            "dash": "dash"  # 指定为虚线
            }
        )
        trace6 =  go.Scatter(
            x = temp['发行起始日'],
            y = np.tile(qcbs_quantile_gk[qcbs_quantile_gk.index ==i].iloc[0][2],2000),
            mode= 'lines',
            name = "全场倍数75%",
            line={
            "width": 3,  
            "color": "Dodgerblue",  
            "dash": "dash"  # 指定为虚线
            }
        )
        data = [trace1, trace2,trace4,trace5,trace6]# ,trace7,trace8,trace9
        layout = go.Layout(title =dict(text = ''.join(['国债',str(i),'年']),
                                        x = 0.5,
                                        yanchor = 'middle') ,
                        yaxis = dict(title = '全场倍数'),
                        yaxis2 = dict(title = '综收较估值',overlaying='y', side='right'),
                        xaxis = dict( 
                        tickformat = '%Y-%m', 
                        tick0 = '2015-01-01',
                        dtick = 'M3',
                        ticks = 'inside'), # 设置每隔一季度就是一个tick
                        legend=dict(orientation="h"),
                #         height = 800,
                #        width = 1000)
                        )
            #设置图离图像四周的边距
        
        fig = go.Figure(data = data, layout = layout)#设置图像的大小
        pyplt(fig, filename = './html/'+''.join(['国债',str(i),'年']))
    return fig


# 2020以后
def after2020():
    df_2020 = df[df['发行起始日']>'2019-12-31'][['发行起始日','发行期限(年)','发行人全称','全场倍数','综收较估值','综收较二级']]
    maturity2020 = [1,3,5,7,10]
    df_qcbs_quantile_2020 = df.groupby(['发行人全称','发行期限(年)']).\
        apply(lambda df:np.nanquantile(df['全场倍数'],[0.25,0.5,0.75])).reset_index()
    issuer = ['国家开发银行', '中华人民共和国财政部']

    for i in issuer:
        for year in maturity2020:
            temp = df_2020[(df_2020['发行人全称']==i)&(df_2020['发行期限(年)']==year)]    
            trace1 = go.Scatter(
                x = temp.groupby('发行起始日').apply(lambda df: df['全场倍数'].mean()).sort_index().index,
                y = temp.groupby('发行起始日').apply(lambda df: df['全场倍数'].mean()).sort_index(),
                fill = 'tozeroy',
                mode= 'none',# 无边界线
                name = "全场倍数",
                fillcolor = 'Lightblue'
            )
            trace2 = go.Scatter(
                x = temp.groupby('发行起始日').apply(lambda df: df['综收较估值'].mean()).sort_index().index,
                y = temp.groupby('发行起始日').apply(lambda df: df['综收较估值'].mean()).sort_index(),
                mode= 'markers',# 无边界线
                name = "综收较估值",
                yaxis="y2",
                line = {'color': 'Chocolate'}
            )
            trace3 =  go.Scatter(
                x = temp.groupby('发行起始日').apply(lambda df: df['综收较二级'].mean()).sort_index().index,
                y = temp.groupby('发行起始日').apply(lambda df: df['综收较二级'].mean()).sort_index(),
                mode= 'markers',# 无边界线
                name = "综收较二级",
                yaxis="y2",
                line = {'color':'Firebrick'}
            )
            trace4 = go.Scatter(
                x = temp['发行起始日'],
                y = np.tile(df_qcbs_quantile_2020[(df_qcbs_quantile_2020['发行人全称'] == i)&(df_qcbs_quantile_2020['发行期限(年)'] == year)].iloc[:,2].tolist()[0][0],200),
                mode= 'lines',
                name = "全场倍数25%",
                line={
                "width": 3,  
                "color": "Dodgerblue",  
                "dash": "dash"  # 指定为虚线
                })

            trace5 = go.Scatter(
                x = temp['发行起始日'],
                y = np.tile(df_qcbs_quantile_2020[(df_qcbs_quantile_2020['发行人全称'] == i)&(df_qcbs_quantile_2020['发行期限(年)'] == year)].iloc[:,2].tolist()[0][1],200),
                mode= 'lines',
                name = "全场倍数50%",
                line={
                "width": 1,  
                "color": "Dodgerblue",  
                "dash": "dash"  # 指定为虚线
                }
            )
            trace6 =  go.Scatter(
                x = temp['发行起始日'],
                y = np.tile(df_qcbs_quantile_2020[(df_qcbs_quantile_2020['发行人全称'] == i)&(df_qcbs_quantile_2020['发行期限(年)'] == year)].iloc[:,2].tolist()[0][2],200),
                mode= 'lines',
                name = "全场倍数75%",
                line={
                "width": 3,  
                "color": "Dodgerblue",  
                "dash": "dash"  # 指定为虚线
                }
            )

            data = [trace1, trace2,trace3,trace4,trace5,trace6]
            name = '国开'
            if i == '中华人民共和国财政部':
                name = '国债'
            
            layout = go.Layout(title =dict(text = ''.join([name,str(year),'年']),
                                            x = 0.5,
                                            yanchor = 'middle') ,
                            yaxis = dict(title = '全场倍数'),
                            yaxis2 = dict(title = '综收较估值',overlaying='y', side='right'),
                            xaxis = dict( 
                            type = 'date',
                                tickformat = '%Y-%m-%d',
                            tick0 = '2020-01-01',
                            dtick = 86400000*15,
                            ticks = 'inside'), # 设置每隔一季度就是一个tick
                            legend=dict(orientation="h")
                        #      height = 750,
                        #      width = 1400)
                            )


            #设置图离图像四周的边距

            fig = go.Figure(data = data, layout = layout)#设置图像的大小
            pyplt(fig, filename = './html/'+''.join([i,str(year),'年']))
    return 



