import ReportGenerator as rg
import data_organize as do
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