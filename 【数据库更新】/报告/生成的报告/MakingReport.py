import ReportGenerator as rg
import data_organize as do

# * 周报 
weekreport = rg.weeklyReport(isMonth = False)
base = '2021-05-21'
end = '2021-05-28'
start = '2021-05-24'
## ! 含有base_day
weekreport.cash_cost(base, end)
weekreport.monetary_policy_tools(base, end)
weekreport.interbank_deposit(base, end)
weekreport.rates_change(base, end)#bp
## * 二级 :近两周 
weekreport.secondary_credit('2021-05-17', end)
weekreport.secondary_rate('2021-05-17', end)
## * 一级 :近两周 
weekreport.prmy_mkt_weekly_issue(start, end)
## * 现券
weekreport.fig_net_data(start, end)
## * 综收 2020以来
weekreport.prmy_mkt_sentiment()

weekreport.print_all_jpg()



# * 月报
month = rg.weeklyReport(isMonth = True)
base = '2021-04-30'
end = '2021-05-28'
start='2021-05-01'
## ! 含有base_day
month.cash_cost(base, end)
month.monetary_policy_tools(base, end)
month.interbank_deposit(base, end)
month.rates_change(base, end)

month.secondary_credit(start, end)
month.secondary_rate(start, end)
month.prmy_mkt_weekly_issue(start,end)

month.fig_net_data(start, end)

month.print_all_jpg()

# 不同机构不同均线现券净买入
pdfreport = rg.weeklyReport()
pdfreport.net_buy_amt()
pdfreport.title = '机构在国债、政金债、地方政府债的净买入量'
pdfreport.print_all_fig()


# * 1
macro_report = rg.MacroReport()
macro_report.fig_all()
macro_report.print_all_fig()
# * 2
net_report = rg.Report()
net_report.title = '5.10-5.14现券'
net_report.fig_net_data('2021-05-10','2021-05-14')
net_report.print_all_fig()
# * 3
report1 = rg.Report()
report1.title = '量化指标观察'
report1.pic_SRDI()
report1.fig_liquidity_premium()
report1.fig_bond_leverage()
report1.fig_rates()
report1.fig_credit_premium()
report1.fig_bond_premium()
report1.fig_industries_premium()
report1.fig_credit_premium_v2()
report1.fig_liquid_v2()
report1.print_all_fig()

