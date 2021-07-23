## 画图代码库

**便于日常调用**

### cashRate——资金数据与息差情况

#### 函数列表

* ##### RepoRate()

* ##### cashrate_1D()

* ##### cashrate_7D()

* ##### vol_1D()

* ##### r_dr_7D()

* ##### r_gc_7D()

* ##### repoVolRatio()

* ##### irs()

* ##### cd6M()

* ##### msPaper()

  * 中票(1,3,5Y)息差

* ##### gk_local()



------


### rateDiff——利率水平
* ##### yieldCurve(bond='gz')

  * 国债/国开债到期收益率曲线对比以及所处历史位置

* ##### gz(year=1)

  * 国债到期收益率曲线及分位数

* ##### gk(year=1)

* ##### CurveChange(bond='gz')

  * 国债收益率曲线变动
  * base基准日：2021-01-04

* ##### local_gz

  * 

* ##### gk_gz

* ##### cd_r007

* ##### msP

  * 中票收益率





------
### rateLevel——利差情况

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

