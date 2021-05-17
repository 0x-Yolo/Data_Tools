# 使用Python导出数据库的数据

1. 在Python编辑器中导入需要用到的库

   ```python
   import data_organize as do
   ```

2. 导出为excel文件

   ```python
   # 事先了解数据表的名称
   table_name = 'Net_buy_bond'
   # 利用data_organize库内的函数从数据库获取表格
   mydata = do.get_data(table_name)
   # 导出为Excel
   mydata.to_excel('现券交易数据.xlsx',index = False)
   ```

