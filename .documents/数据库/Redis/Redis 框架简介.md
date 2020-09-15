Redis 数据库

在线 Redis 练习：http://try.redis.io/

教程：http://c.biancheng.net/redis/

官网地址：https://redis.io/

百度百科：https://baike.baidu.com/item/Redis/6549233

##### 4.3.1、Redis 介绍

Redis 属于`键值数据库`。具有极高的读写能力，用于处理大量数据的高访问负载比较合适。

##### 4.3.2、Redis 安装和配置


下载地址为：https://redis.io/download 在该页面有简单的安装过程和使用引导。

1、配置编译环境：

```shell
yum install -y gcc gcc-c++ jemalloc-devel epel-release tcl tar zip openssl openssl-devel automake glibc-static autoconf libtool make build-essential
```
2、创建 Redis 安装目录：

```shell
[root@localhost ~]# mkdir /ext/redis/
```
3、下载 Redis 安装源码：

```shell
[root@localhost Downloads]# wget http://download.redis.io/releases/redis-5.0.5.tar.gz
[root@localhost Downloads]# tar -zxvf redis-5.0.5.tar.gz 
[root@localhost Downloads]# cd redis-5.0.5/
```
4、编译 Redis 源码：

```shell
make MALLOC=libc
```
5、安装 Redis 程序：

```shell
make PREFIX=/ext/redis install
```
6、建立 Redis 软连接：

```shell
ln -s /ext/redis/bin/redis-server /usr/bin/redis-server -f
ln -s /ext/redis/bin/redis-cli /usr/bin/redis-cli -f
ln -s /ext/redis/bin/redis-sentinel /usr/bin/redis-sentinel -f
ln -s /ext/redis/bin/redis-check-rdb /usr/bin/redis-check-rdb -f
ln -s /ext/redis/bin/redis-check-aof /usr/bin/redis-check-aof -f
```
7、以后台程序方式运行： 在命令后加上 & 号

```shell
[root@localhost ~]# redis-server &
```
由于这里没有带上 redis.conf 配置文件，因此使用的是默认配置。

如果不使用默认配置，则可以通过启动参数的方式来告诉 redis 使用指定配置文件。

8、指定配置文件方式启动：

```shell
redis-server <配置文件>
```
9、客户端连接服务：

```shell
[root@localhost ~]# redis-cli
127.0.0.1:6379> set foo bar
OK
127.0.0.1:6379> get foo
"bar"
127.0.0.1:6379> 
```

### Redis 异常处理
1、Executing test client: couldn't execute "src/redis-benchmark": no such file or directory.
则执行以下两个步骤：

```shell
sudo make distclean
sudo make
```
2、(error) MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error．(错误) misconf redis被配置以保存数据库快照，但misconf redis目前不能在硬盘上持久化。用来修改数据集合的命令不能用，请使用日志的错误详细信息。
在终端执行如下命令：

```shell
config set stop-writes-on-bgsave-error no
```
也就是关闭配置项 stop-writes-on-bgsave-error 解决该问题。

### Redis 配置参数
配置文件 redis.conf 参数说明：
1、Redis 默认不是以守护进程的方式运行，可以通过该配置项修改，使用yes启用守护进程
```shell
daemonize no
```
2、当 Redis 以守护进程方式运行时，Redis默认会把pid写入/var/run/redis.pid文件，可以通过pidfile指定
```shell
pidfile /var/run/redis.pid
```
3、指定Redis监听端口，默认端口为6379，作者在自己的一篇博文中解释了为什么选用6379作为默认端口，因为6379在手机按键上MERZ对应的号码，而MERZ取自意大利歌女Alessia Merz的名字
```shell
port 6379
```
4、绑定的主机地址
```shell
bind 127.0.0.1
```
5、当客户端闲置多长时间后关闭连接，如果指定为0，表示关闭该功能
```shell
timeout 300
```
6、指定日志记录级别，Redis总共支持四个级别：debug、verbose、notice、warning，默认为verbose
```shell
loglevel verbose
```
7、日志记录方式，默认为标准输出，如果配置Redis为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给/dev/null
```shell
logfile stdout
```
8、设置数据库的数量，默认数据库为0，可以使用SELECT &lt;dbid&gt;命令在连接上指定数据库 id：

```shell
databases 16
```
9、指定在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合
```shell
save &lt;seconds&gt; &lt;changes&gt;
```
Redis默认配置文件中提供了三个条件：
```shell
save 900 1
save 300 10
save 60 10000
```
分别表示900秒（15分钟）内有1个更改，300秒（5分钟）内有10个更改以及60秒内有10000个更改。

10、指定存储至本地数据库时是否压缩数据，默认为yes，Redis采用LZF压缩，如果为了节省CPU时间，可以关闭该选项，但会导致数据库文件变的巨大

```shell
rdbcompression yes
```
11、指定本地数据库文件名，默认值为 dump.rdb
```shell
dbfilename dump.rdb
```
12、指定本地数据库存放目录
```shell
dir ./
```
13、设置当本机为slav服务时，设置master服务的IP地址及端口，在Redis启动时，它会自动从master进行数据同步

```shell
slaveof <masterip> <masterport>
```
14、当master服务设置了密码保护时，slav服务连接master的密码
```shell
masterauth <master-password>
```
15、设置Redis连接密码，如果配置了连接密码，客户端在连接Redis时需要通过AUTH &lt;password&gt; 命令提供密码，默认关闭

```shell
requirepass foobared
```
16、设置同一时间最大客户端连接数，默认无限制，Redis可以同时打开的客户端连接数为Redis进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，Redis会关闭新的连接并向客户端返回max number of clients reached错误信息
```shell
maxclients 128
```
17、指定Redis最大内存限制，Redis在启动时会把数据加载到内存中，达到最大内存后，Redis会先尝试清除已到期或即将到期的Key，当此方法处理 后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。Redis新的vm机制，会把Key存放内存，Value会存放在swap区
```shell
maxmemory <bytes>
```
18、指定是否在每次更新操作后进行日志记录，Redis在默认情况下是异步的把数据写入磁盘，如果不开启，可能会在断电时导致一段时间内的数据丢失。因为 redis本身同步数据文件是按上面save条件来同步的，所以有的数据会在一段时间内只存在于内存中。默认为no
```shell
appendonly no
```
19、指定更新日志文件名，默认为appendonly.aof
```shell
appendfilename appendonly.aof
```
20、指定更新日志条件，共有3个可选值： 
no：表示等操作系统进行数据缓存同步到磁盘（快） 
always：表示每次更新操作后手动调用fsync()将数据写到磁盘（慢，安全） 
everysec：表示每秒同步一次（折衷，默认值）
```shell
appendfsync everysec
```
21、指定是否启用虚拟内存机制，默认值为no，简单的介绍一下，VM机制将数据分页存放，由Redis将访问量较少的页即冷数据swap到磁盘上，访问多的页面由磁盘自动换出到内存中（在后面的文章我会仔细分析Redis的VM机制）
```shell
vm-enabled no
```
22、虚拟内存文件路径，默认值为/tmp/redis.swap，不可多个Redis实例共享
```shell
vm-swap-file /tmp/redis.swap
```
23、将所有大于vm-max-memory的数据存入虚拟内存,无论vm-max-memory设置多小,所有索引数据都是内存存储的(Redis的索引数据 就是keys),也就是说,当vm-max-memory设置为0的时候,其实是所有value都存在于磁盘。默认值为0
```shell
vm-max-memory 0
```
24、Redis swap文件分成了很多的page，一个对象可以保存在多个page上面，但一个page上不能被多个对象共享，vm-page-size是要根据存储的 数据大小来设定的，作者建议如果存储很多小对象，page大小最好设置为32或者64bytes；如果存储很大大对象，则可以使用更大的page，如果不 确定，就使用默认值
```shell
vm-page-size 32
```
25、设置swap文件中的page数量，由于页表（一种表示页面空闲或使用的bitmap）是在放在内存中的，，在磁盘上每8个pages将消耗1byte的内存。
```shell
vm-pages 134217728
```
26、设置访问swap文件的线程数,最好不要超过机器的核数,如果设置为0,那么所有对swap文件的操作都是串行的，可能会造成比较长时间的延迟。默认值为4
```shell
vm-max-threads 4
```
27、设置在向客户端应答时，是否把较小的包合并为一个包发送，默认为开启
```shell
glueoutputbuf yes
```
28、指定在超过一定的数量或者最大的元素超过某一临界值时，采用一种特殊的哈希算法
```shell
hash-max-zipmap-entries 64
hash-max-zipmap-value 512
```
29、指定是否激活重置哈希，默认为开启（后面在介绍Redis的哈希算法时具体介绍）
```shell
activerehashing yes
```
30、指定包含其它的配置文件，可以在同一主机上多个Redis实例之间使用同一份配置文件，而同时各个实例又拥有自己的特定配置文件
```shell
include /path/to/local.conf
```
参考网址：
Redis 教程： https://www.runoob.com/redis/redis-tutorial.html
Redis 5.0.3 编译安装，并搭建 cluster 的过程记录： https://www.liangzl.com/get-article-detail-114377.html

### Redis 应用场景

https://blog.csdn.net/Vera1114/article/details/80315577

 国内外三个不同领域巨头分享的Redis实战经验及使用场景（转）：

https://www.cnblogs.com/ajianbeyourself/p/4475183.html

#### 消息订阅

#### 无重复队列

#### 标签实现

https://segmentfault.com/q/1010000000581921/a-1020000005931774

https://blog.csdn.net/vera1114/article/details/80314866

#### 缓存分页列表

https://segmentfault.com/q/1010000004669503/a-1020000004689506

Redis技术分享：

https://blog.csdn.net/qq_28851503/article/details/79705282

Redis应用案例，查找某个值的范围（转）：

https://www.cnblogs.com/ajianbeyourself/p/4475182.html






##### 4.3.3、Python 3 操作 Redis

###### 4.3.3.1、安装 redis-py 库

执行如下语句安装 redis-py 库：

```powershell
pip install -i https://pypi.doubanio.com/simple/ redis
```

验证安装结果是否正确：

```powershell
(PyDatabase) λ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import redis
>>>
```

