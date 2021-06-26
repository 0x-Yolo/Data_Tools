#### Pandas包的.read_XXX()函数

* ##### 读写csv文件

  ##### df = pd.read_csv(路径，分隔符，空值处理方法，格式，..)

  ```python
  df = pd.read_csv('D:\tpyzq.csv')
  ```

  

* ##### 读取.xlsx/.xls文件
  
  ##### df = pd.read_excel(路径， sheetname=0，header=0，..)
  
  ```python
  df = pd.read_excel('D:\tpyzq.xlsx', sheetname="测试数据")
  ```

* ##### 导出为excel文件

  ##### df.to.excel('tpyzq01.xlsx')

