
四、安装 MySQL 链接库

```shell
pip install -i https://pypi.doubanio.com/simple/ mysqlclient
```

五、验证 MySQL 安装结果

```powershell
(DjangoDev) λ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import MySQLdb
>>> MySQLdb.__version__
'1.4.4'
>>>
```

