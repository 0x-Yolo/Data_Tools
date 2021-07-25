### 1. 安装Python解释器
https://www.python.org/downloads/release/python-383/

* **注意勾选Add Python 3.8 to PATH**

### 2. 安装Pycharm

[https://www.jetbrains.com/pycharm/download/#section=windows](https://www.jetbrains.com/pycharm/download/)

### 3. 在Pycharm中新建第一个python项目

* **基本解释器**选择第一步Python解释器的安装地址
* **位置**是自定义项
* 新建完成后，需要将自建函数库手动配置入python所在文件夹中(python38/lib/..)

#### 3.1 导入模块

* No module names xxx：xxx模块未安装，前往python packages安装即可
  * pandas/numpy
  * pymysql/sqlalchemy
  * Matplotlib/seaborn
* 导入需要的模块，如from cashRate import *
* 调用相关函数换图
