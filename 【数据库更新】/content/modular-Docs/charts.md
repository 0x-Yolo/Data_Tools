## 画图代码库

**便于日常调用**

### cashRate库——资金数据与息差情况

*该库内函数可自主设置start(起始日)与end(结束日)，不设置则输出默认区间*

#### 资金数据

* ##### RepoRate()

  * R001, R007, R021

* ##### cashrate_1D()

  * R001, GC001, DR001

* ##### cashrate_7D()

  * R007, GC007, DR007

* ##### vol_1D()

  * 隔夜成交量

* ##### r_dr_7D()

* ##### r_gc_7D()

* ##### repoVolRatio()

  * R001成交量与R007成交量占比

* ##### irs()

  * IRS_1y_FR007, IRS_5y_FR007, IRS_5y_shibor3m

#### 息差情况

* ##### cd6M()

* ##### msPaper()

  * 中票(1,3,5Y)息差

* ##### gk_local()



------


### rateDiff——利率水平
* ##### yieldCurve(bond='gz')

  * 国债/国开债各期限到期收益率曲线对比以及所处历史位置
  * 对比基准日:现值与2020年底
  * **bond** in {'gz', 'gk'}

* ##### gz(year=1)

  * 国债到期收益率曲线及分位数
  * **year** in {1, 3, 5, 7, 10}

* ##### gk(year=1)

  * 同上

* ##### CurveChange(bond='gz')

  * 国债收益率曲线变动
  * base基准日：2021-01-04

* ##### local_gz_5y()

  * 地方债5年-国开债5年利差

* ##### gk_gz()

  * 国开10年-国债10年利差

* ##### cd3m_r007()

  * 3个月存单-R007利差

* ##### msP()

  * 中票收益率（AAA/AA+, 1y/5y）



------
### rateLevel库——利差情况

#### 国债国开与非国开

* ##### term1

* ##### term2

* ##### implicitRate

* ##### gk_nf_kh

#### 期限利差

* ##### term_gz

* ##### term_10_1

* ##### termSpots_10_1

* ##### termSpots_30_10

* ##### gz_barbell

* ##### gk_barbell

* ##### termSpots_gk_gz

* ##### spreads_gk_gz_1d

* ##### nf_kh_gk_10y

* ##### new_gk_old

#### 信用利差

* ##### creditSpreads

* ##### gradeSpreads

#### 中外利差

* ##### spreads_cn_us_2y

* ##### spreads_cn_us_1y

* ##### spreads_exchange

* ##### spreads_cn_us_mkt

* ##### termUS

