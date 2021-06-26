### pandas库连接外部数据库

1. #### 在Python编辑器中导入需要用到的库

   ```python
   import pymysql
   from sqlalchemy import create_engine
   ```

2. #### 创建数据库连接

   ```python
   conn = pymysql.connect(	
           host = host,	
           user = username,	
           passwd = password,	
           db = 'finance',	
           port=port,	
           charset = 'utf8'	
       )	
   engine = create_engine(mysql+pymysql://user:password@host:port/finance?charset=utf8)
   ```

3. #### 从数据库拉取表格，并保存为本地excel文件

   ```python
   # 创建查询语句（SQL语法）
   table_name = 'Net_buy_bond'
   excu = 'select * from ' + table_name
   
   # 利用pd.read_sql()函数，参数为查询语句和数据库连接conn，赋值至df
   df = pd.read_sql(excu, conn)
   
   # 利用.to_excel函数，导出成excel文件
   df.to_excel('现券交易数据.xlsx')
   ```

