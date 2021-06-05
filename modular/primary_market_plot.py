import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import DateTime
# %matplotlib inline
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

import data_organize as do
# plt.rcParams['font.family']=['Kaiti SC']
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False  


# * 一级综收
df = do.get_data('primary_rate_sec')
# df = pd.read_excel('/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/专题数据/一级发行数据/利率债一级_新.xlsx',sheet_name = '数据（导入）')
# 这步是用来去除异常值的，之后有啥异常值还可以在这边改。
df = df[df['综收较估值'] < 40]
df = df.loc[df['发行起始日'] >= '2020-01-01']

def GK():
    df_gk = df[df['发行人全称']=='国家开发银行'][['发行起始日','发行期限(年)','发行人全称','全场倍数','综收较估值','综收较二级']]
    qcbs_quantile_gk = df_gk.groupby('发行期限(年)').apply(lambda df:np.nanquantile(df['全场倍数'],[0.25,0.5,0.75]))
    
    maturity = [1,3,5,7,10,20]
    n = len(maturity)
    
    plt.style.use({'font.size' : 12})     
    fig,ax = plt.subplots(nrows=n,ncols=1,figsize=(4.15*2,1.42*2*n),dpi = 300)
    for i in range(n):
        m = maturity[i]
        temp = df_gk[df_gk['发行期限(年)']==m]
        temp.index = temp['发行起始日']

        ax[i].fill_between(temp.index, 0, temp['全场倍数'], \
            facecolor='Lightblue', alpha=0.5,label='全场倍数')
        ax_ = ax[i].twinx()
        ax_.scatter(temp.index,temp['综收较估值'] ,color='#f0833a',\
            s=10,label = '综收较估值')
        ax[i].axhline(y=qcbs_quantile_gk[qcbs_quantile_gk.index ==m].iloc[0][0],\
            ls='--',color='#3778bf',label='全场倍数25%',lw=2)
        ax[i].axhline(y=qcbs_quantile_gk[qcbs_quantile_gk.index ==m].iloc[0][1],\
        ls='--',color='#3778bf',label='全场倍数50%',lw=1)
        ax[i].axhline(y=qcbs_quantile_gk[qcbs_quantile_gk.index ==m].iloc[0][2],\
        ls='--',color='#3778bf',label='全场倍数75%',lw=2)
        ax[i].grid( linestyle='--', linewidth=1,alpha=0.5)

        ax[i].set_ylabel ('全场倍数')
        ax_.set_ylabel ('综收较估值')
        ax[i].set_title('国开{}年'.format(m))

        # ax_.legend(loc=2, bbox_to_anchor=(1.05,1),borderaxespad = 0.) 
        # ax[i].legend(loc=2, bbox_to_anchor=(1.05,0.25),borderaxespad = 0.) 
        ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.88,-0.3),\
            borderaxespad = 0.,frameon=False) 
        ax[i].legend(ncol=4,loc=3,bbox_to_anchor=(-0.1,-0.3),\
            borderaxespad = 0.,frameon=False)  
    fig.tight_layout()
    return fig


def GZ():
    df_gk = df[df['发行人全称']=='中华人民共和国财政部'][['发行起始日','发行期限(年)','发行人全称','全场倍数','综收较估值','综收较二级']]
    qcbs_quantile_gk = df_gk.groupby('发行期限(年)').apply(lambda df:np.nanquantile(df['全场倍数'],[0.25,0.5,0.75]))

    maturity = [1,3,5,7,10,30,50]
    n = len(maturity)
    fig,ax = plt.subplots(nrows=n,ncols=1,figsize=(4.15*2,1.42*2*n),dpi = 300)
    for i in range(n):
        m = maturity[i]
        temp = df_gk[df_gk['发行期限(年)']==m]
        temp.index = temp['发行起始日']

        ax[i].fill_between(temp.index, 0, temp['全场倍数'], \
            facecolor='Lightblue', alpha=0.5,label='全场倍数')
        ax_ = ax[i].twinx()
        ax_.scatter(temp.index,temp['综收较估值'] ,color='#f0833a',s=10,\
            label='综收较估值')
        ax[i].axhline(y=qcbs_quantile_gk[qcbs_quantile_gk.index ==m].iloc[0][0],\
            ls='--',color='#3778bf',label='全场倍数25%',lw=2)
        ax[i].axhline(y=qcbs_quantile_gk[qcbs_quantile_gk.index ==m].iloc[0][1],\
        ls='--',color='#3778bf',label='全场倍数50%',lw=1)
        ax[i].axhline(y=qcbs_quantile_gk[qcbs_quantile_gk.index ==m].iloc[0][2],\
        ls='--',color='#3778bf',label='全场倍数75%',lw=2)
        ax[i].grid( linestyle='--', linewidth=1,alpha=0.5)

        # ax[i].xaxis.set_major_locator(years)
        # ax[i].xaxis.set_major_formatter(yearsFmt)
        # ax[i].xaxis.set_minor_locator(months)
        ax_.legend(ncol=1,loc=3, bbox_to_anchor=(0.88,-0.3),\
            borderaxespad = 0.,frameon=False) 
        ax[i].legend(ncol=4,loc=3,bbox_to_anchor=(-0.1,-0.3),\
            borderaxespad = 0.,frameon=False)  
        ax[i].set_ylabel ('全场倍数')
        ax_.set_ylabel ('综收较估值')
        ax[i].set_title('国债{}年'.format(m))
    fig.tight_layout()
    return fig

def GK_html():
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
        pyplt(fig, filename = './html/'+''.join(['国开',str(i),'年']))
    return fig_list

def GZ_html():
    fig_list = []
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
        fig_list.append(fig)
        pyplt(fig, filename = './html/'+''.join(['国债',str(i),'年']))
    return fig_list
