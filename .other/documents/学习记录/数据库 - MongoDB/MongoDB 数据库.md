
#### MongoDB 数据库

##### MongoDB 介绍

MongoDB 属于`文档型数据库`。
这类数据库满足了海量数据的存储和访问需求，同时对字段要求不严格，可以随意地增加、删除、修改字段，且不需要预先定义表结构，所以适用于各种网络应用。

MongoDB 是一个跨平台的 NoSQL 数据库，基于 Key-Value 的形式来保存数据。

它的存储格式非常类似于 Python 的字典，因此用 Python 操作 MongoDB 会非常容易。

##### MongoDB 下载

MongoDB 下载地址：https://www.mongodb.com/download-center/community

##### MongoDB 安装

![1569307144968](http://image-hncg.hnchenguang.com//markdown/20200515093632.png)
![1569307205465](http://image-hncg.hnchenguang.com//markdown/20200515093633.png)
![1569307230152](http://image-hncg.hnchenguang.com//markdown/20200515093634.png)
![1569307244887](http://image-hncg.hnchenguang.com//markdown/20200515093635.png)
![1569307255608](http://image-hncg.hnchenguang.com//markdown/20200515093636.png)
![1569307269478](http://image-hncg.hnchenguang.com//markdown/20200515093637.png)
![1569307279323](http://image-hncg.hnchenguang.com//markdown/20200515093638.png)
直到安装完成，安装过程需要几分钟左右。

##### MongoDB 配置
###### 配置 MongoDB
1、进入 `C:\MongoDB\Server\4.2\data` 目录，在该目录下分别创建 `log` 和 `db` 两个文件夹，如下图所示：
![1569307638850](http://image-hncg.hnchenguang.com//markdown/20200515093639.png)
2、进入 `C:\MongoDB\Server\4.2\data\log` 目录，创建空文件 `mongodb.log`，如下图所示：
![1569307699293](http://image-hncg.hnchenguang.com//markdown/20200515093640.png)
3、进入 `C:\MongoDB\Server\4.2` 创建文件 `mongo.config`，如下图所示：
![1569307723763](http://image-hncg.hnchenguang.com//markdown/20200515093641.png)
4、打开 `C:\MongoDB\Server\4.2\mongo.config` 文件，写入如下配置信息，并保存：

```shell
### 数据文件
dbpath=C:\MongoDB\Server\4.2\data\db
### 日志文件
logpath=C:\MongoDB\Server\4.2\data\log\mongodb.log
### 错误日志采用追加模式，配置这个选项后 MongoDB 的日志会追加到现有的日志文件
### 而不是从新创建一个新文件
logappend=true
### 启用日志文件，默认启用
journal=true
### 这个选项可以过滤掉一些无用的日志信息，若需要调试使用请设置为false
quiet=true
### 端口号 默认为 27017
port=27017
```

###### 测试是否安装成功

进入 `C:\MongoDB\Server\4.2\bin` 目录，运行 `mongod.exe` 一闪而过，然后在浏览器输入：http://localhost:27017/ ，出现如下信息：
```shell
It looks like you are trying to access MongoDB over HTTP on the native driver port.
```
说明我们的 MongoDB 安装成功。
###### 注册为系统服务
<font color="red">本版本的 MongoDB 在安装的时候已经自动注册为系统服务</font>了同时也<font color="red">自动启动</font>了，因此不需要<font color="red">注册</font>和<font color="red">配置</font>步骤。
<font color="red">注册</font>：有三种注册方式，以下一一介绍：
方式一：用管理员权限打开 cmd 命令行，输入如下命令安装 MongoDB 服务：

```shell
sc create MongoDB binPath= "C:\MongoDB\Server\4.2\bin\mongod.exe --service --config=C:\MongoDB\Server\4.2\mongo.config"
```
方式二：进入 C:\MongoDB\Server\4.2\bin 文件夹，使用如下命令：
```shell
mongod --config C:\MongoDB\Server\4.2\mongo.config --install --serviceName "MongoDBServer"
```
方式三：进入 C:\MongoDB\Server\4.2\bin 文件夹，使用如下命令：
```shell
mongod --logpath "C:\MongoDB\Server\4.2\log\mongod.log" --logappend --dbpath "C:\MongoDB\Server\4.2\data\db" --serviceName "MongoDBServer" --install
```
<font color="red">配置</font>：
然后用管理员权限打开 cmd 命令，输入 `services.msc` 打开服务管理器，找到 MongoDB 服务，设置成自动启动，并启动；如果启动不成功，先删除服务，使用如下命令：`sc delete MongoDB`，然后再重新注册系统服务。

###### 配置系统环境变量

电脑 → 属性 → 高级系统设置 → 高级 → 环境变量 → 系统变量 → Path → 编辑 → 新建，填入如下信息：C:\MongoDB\Server\4.2\bin ，如下图所示：
![1569309606396](http://image-hncg.hnchenguang.com//markdown/20200515093642.png)

##### 可视化操作工具

MongoDB 可视化工具 Robo 3T 使用教程：
https://www.cnblogs.com/tugenhua0707/p/9250673.html

Robo 3T 下载：https://robomongo.org/download 点击 <font style="background-color:#3f9e3f;color:white">Download Robo 3T</font> 进行下载。

###### Robo 3T 安装

安装过程很简单，跟普通软件的安装过程是一样的。

###### Robo 3T 使用
启动 Robo 3T 软件，然后点击 Create 如下图所示：
![1569310024110](http://image-hncg.hnchenguang.com//markdown/20200515093643.png)
填写链接地址和端口号，然后点击 Test 进行链接测试，如下图：
![1569310058744](http://image-hncg.hnchenguang.com//markdown/20200515093644.png)
链接测试成功，显示如下信息：
![1569310088009](http://image-hncg.hnchenguang.com//markdown/20200515093645.png)
然后点击 Save 保存链接配置。
![1569310111342](http://image-hncg.hnchenguang.com//markdown/20200515093646.png)
选择要查看的链接，然后点击 Connect 进行链接即可查看 MongoDB 数据库了。

###### 4.2.5.3、创建数据库

<font color="red">右键</font>单击 New Connection，选择 `Create Database`，这里创建一个 `test_data` 的数据库。

###### 4.2.5.4、创建集合

在 test_data 数据库中，<font color="red">右键</font>单击 Collections，选择 Create Collection，这里创建一个 example_1 的集合。

###### 4.2.5.5、插入语句
执行如下插入语句：
```sql
db.getCollection('example_1').insertOne({"name": "张小二 ", "age": 17, "address": "浙江"})
db.getCollection('example_1').insertOne({"name": "刘小三 ", "age": 10, "address": "广东"})
```
结果如下图所示：
![1569310583983](http://image-hncg.hnchenguang.com//markdown/20200515093647.png)
从图中可以看出，集合中的每个元素都是一个 Object 对象，每个对象都有一个 ObjectId。
接下来执行批量插入语句：
```sql
db.getCollection('example_1').insertMany([
  {"name": "朱小三 ", "age": 16, "address": "北京"},
  {"name": "刘小四 ", "age": 20, "address": "上海"},
  {"name": "马小五 ", "age": 25, "address": "广州"},
  {"name": "夏侯晓琪 ", "age": 28, "address": "深圳"}
])
```
注意：
```reStructuredText
_id 读作 Object Id，由时间、机器码、进行pid、自增计数器构成。_id 递增而不重复，同一时间，不同机器上的 _id 不同；同一机器，不同时间的 _id 也不同；同一机器同一时间批量插入的数据 _id 也不同；_id的前八位字符转化为十进制就是时间戳。
```
###### 4.2.5.6、查询语句
查询所有：

```sql
db.getCollection('example_1').find({})
```

查询一条：

```sql
db.getCollection('example_1').find({'age': 25})
db.getCollection('example_1').find({'age': 25, 'address': '上海'})
```

范围查询：

```sql
db.getCollection('example_1').find({'age': {'$gte': 25}}) ## 查询 age 大于 25 的对象
```



###### 4.2.5.7、更新语句

updateOne 和 updateMany。

###### 4.2.5.8、删除语句

deleteOne 和 deleteMany。

慎用删除功能。一般工程上会使用“假删除”，即：在文档里面增加一个字段 `deleted`，如果值为 0 则表示没有删除，如果值为 1 则表示已经被删除了。
默认情况下，`deleted` 字段的值都是 0，如需要执行删除操作，则把这个字段的值更新为 1。而查询数据时，只查询 `deleted` 为 0 的数据。这样就实现了和删除一样的效果，即使误操作了也可以轻易恢复。

###### 4.2.5.9、去重语句

distinct()

操作语句参考文档：
https://blog.csdn.net/fengtingyan/article/details/88371232

###### 4.2.5.10、Robo 3T 安装 zip 版本

打开  https://robomongo.org/download  网址，点击 Download Robo 3T ，然后选择版本，如下图所示：

<img src="http://image-hncg.hnchenguang.com//markdown/20200515093648.png" alt="1571811311244" style="zoom:80%;" /> 

进行下载，然后解压缩到 C:\Robo3T-1.3.1 ，如下图所示：

<img src="http://image-hncg.hnchenguang.com//markdown/20200515093649.png" alt="1571814177427" style="zoom:80%;" />

把 ==robo3t.exe== 固定到 “开始” 屏幕，然后就可以连接 MongoDB 数据库了。

##### 4.2.6、Python 3 操作 MongoDB

###### 4.2.6.1、安装库文件

创建虚拟环境：

```shell
mkvirtualenv PyDatabase
```

安装 pymongo 库：

```shel
pip install -i https://pypi.doubanio.com/simple/ pymongo
```

安装后，如下验证是否安装成功：

```shell
(PyDatabase) λ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import pymongo
>>>
```

###### 4.2.6.2、创建连接

```python
## -*- coding:utf-8 -*-
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('mongodb://服务器IP或域名:端口')
client = MongoClient('mongodb://用户名:密码@服务器IP或域名:端口')
```

###### 4.2.6.3、连接集合

连接集合有两种方式：

**方式一**：

```python
## -*- coding:utf-8 -*-
from pymongo import MongoClient

client = MongoClient()
database = client.数据库名
collection = database.集合名
```

比如：

```python
client = MongoClient()
database = client.test_data
collection = database.example_1
```

**方式二**：

```python
db_name = 'test_data'
collection_name = 'example_1'
client = MongoClient()
database = client[db_name]
collection = database[collection_name]
```

###### 4.2.6.4、插入数据

```python
## -*- coding:utf-8 -*-
from pymongo import MongoClient

db_name = 'test_data'
collection_name = 'example_1'
client = MongoClient()
database = client[db_name]
collection = database[collection_name]
collection.insert_many([
    {"name": "张三 ", "age": 20, "address": "北京"},
    {"name": "李四 ", "age": 23, "address": "上海"},
    {"name": "王五 ", "age": 23, "address": "广州"},
    {"name": "赵六 ", "age": 25, "address": "深圳"},
    {"name": "朱七 ", "age": 25, "address": "天津"},
    {"name": "重八 ", "age": 28, "address": "重庆"}
])
```

###### 4.2.6.5、查询数据

```python
db_name = 'test_data'
collection_name = 'example_1'
client = MongoClient()
database = client[db_name]
collection = database[collection_name]

rows = collection.find(
    {
        'age': {'$lt': 25, '$gt': 20},
        'name': {'$ne': '赵六'}
    }
)

for row in rows:
    print(row)
```

结果如下：

```shell
{'_id': ObjectId('5d8085757ce7f9d636c3e506'), 'name': '李四 ', 'age': 23, 'address': '上海'}
{'_id': ObjectId('5d8085757ce7f9d636c3e507'), 'name': '王五 ', 'age': 23, 'address': '广州'}
```

##### 4.2.7、MongoDB 安装 zip 版本

###### 1、下载并解压缩

打开  https://www.mongodb.com/download-center/community  网址：

<img src="http://image-hncg.hnchenguang.com//markdown/20200515093650.png" alt="1571811040443" style="zoom:80%;" />

把 zip 版本下载下来之后，解压缩到 ==C:\MongoDB-4.2.1== 如下图所示：

<img src="http://image-hncg.hnchenguang.com//markdown/20200515093651.png" alt="1571811688730" style="zoom:80%;" />

###### 2、配置和注册服务

一、把 ==C:\MongoDB-4.2.1\bin== 配置到系统变量的 ==Path== 变量中，如下图所示：

<img src="http://image-hncg.hnchenguang.com/markdown/20200515093652.png"/>

二、在根目录 ==C:\MongoDB-4.2.1== 创建 ==mongo.config== 配置文件，配置内容如下：

```shell
## 数据文件
dbpath=C:\MongoDB-4.2.1\data
## 日志文件
logpath=C:\MongoDB-4.2.1\mongodb.log
## 错误日志采用追加模式，配置这个选项后 MongoDB 的日志会追加到现有的日志文件
## 而不是从新创建一个新文件
logappend=true
## 启用日志文件，默认启用
journal=true
## 这个选项可以过滤掉一些无用的日志信息，若需要调试使用请设置为false
quiet=true
## 配置 MongoDB 绑定 IP 地址
bind_ip=127.0.0.1
## 端口号 默认为 27017
port=27017
```

并在**根目录下手动创建** ==data== 目录和 ==mongodb.log== 文件，如下图所示：

<img src="http://image-hncg.hnchenguang.com/markdown/20200515093653.png"/>

三、注册为系统服务

进入 C:\MongoDB-4.2.1\bin 目录，在该目录下，以管理员身份打开 CMD 然后执行如下命令：

```shell
mongod --serviceName "MongoDBServer" --serviceDisplayName "MongoDBService" --config "C:\MongoDB-4.2.1\mongo.config" --install
或者如下
mongod --config "D:\OtherPrograms\MongoDB\mongo.config" --install
```

在系统服务中，启动 MongoDB 并设置为自动启动。

四、卸载 MongoDB 服务

进入 C:\MongoDB-4.2.1\bin 目录，在该目录下执行如下命令：

```shell
mongod --remove
```

五、其他相关配置
在mongoDB命令行客户端中执行以下命令创建超级用户：

use admin //把当前数据库改为admin系统数据库

//为admin系统数据库创建具有超级权限“root”的超级用户，admin系统数据库的超级用户将同时成为整个MongoDB系统的超级用户。

db.createUser({user:"root",pwd:"12345",roles:["root"]})

db.auth("root","12345") //使用超级用户登录admin数据库，执行该命令前需要保证当前数据库是admin系统数据库。该账户只能登录admin数据库

在MongoDB配置文件（*.cfg）中添加：

auth=true

该配置项使MongoDB的账户授权机制生效。

###### 3、验证安装是否成功

在浏览器输入 http://127.0.0.1:27017/ 出现如下信息说明安装成功：
```shell
It looks like you are trying to access MongoDB over HTTP on the native driver port.
```
到这里 MongoDB zip 方式安装过程就完成了。
