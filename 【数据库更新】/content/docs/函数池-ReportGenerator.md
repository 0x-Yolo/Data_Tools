# ReportGenerator



## Class weeklyReport(isMonth = False)

### Methods

* #### cash_cost(base,end)

  ###### 资金利率

  * ###### base: 基准日，如上周五或上月末最后一天
  * ###### end: 图像终止日，本周最后一个交易日
  * ###### *start: 图像起始日为2020-01-01

* #### monetary_policy_tools(base, end)

  ###### 公开市场投放

  * ###### *start: 图像起始日为2020-10-01

* #### interbank_deposit(base, end)

  ###### 存单价格与净融资量

  * ###### *start: 图像起始日为2020-01-01

* #### prmy_mkt_weekly_issue(start, end)

  ###### 一级市场发行

* #### prmy_mkt_sentiment()

  ###### 国开/国债全场倍数与综收

* #### rates_change(start, end)

  ###### 各券种到期收益率变动

  * ###### start: 基准日(上周五)

  * ###### end: 终止日

* #### fig_net_data(start, end)

  ###### 各机构久期分布、各机构新债净买入情况

* #### net_buy_amt()

  ###### 各机构利率债净买入(pdf)

* #### secondary_credit(start, end)

  ###### 二级信用债

* #### secondary_rate(start, end)

  ###### 二级利率债