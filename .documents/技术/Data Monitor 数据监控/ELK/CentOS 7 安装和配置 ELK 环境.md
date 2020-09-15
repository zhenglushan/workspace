CentOS 系统版本： CentOS Linux release 7.6.1810 (Core)

[由于是外网，下载时，建议使用迅雷工具下载。] [ ELK-7.3安装部署 https://www.chengbinbin.cn/archives/2019080808080088 ]

Elastic 下载中心：https://elasticsearch.cn/download/

创建用户组和用户： [root@localhost ~]# groupadd es_group [root@localhost ~]# useradd es_shanhai -g es_group -p a5s7sh4u

创建 java 和 elk 目录： [root@localhost ~]# mkdir -p /ext/java/ [root@localhost ~]# mkdir -p /ext/elk/

1、安装和配置 java 环境 上传 java 的 tar 包到 /ext/java/ 目录下，并解压缩： [root@localhost ~]# cd /ext/java/ [root@localhost java]# tar -zxvf jdk-13_linux-x64_bin.tar.gz

配置 java 环境变量并生效： [root@localhost java]# gedit /etc/profile 增加如下内容：

# java environment

export JAVA_HOME=/ext/java/jdk-13 export PATH=PATH export CLASSPATH=.:JAVA_HOME/lib/tools.jar:CLASSPATH 使配置生效： [root@localhost java]# source /etc/profile 验证： [root@localhost java]# java -version java version "13" 2019-09-17 Java(TM) SE Runtime Environment (build 13+33) Java HotSpot(TM) 64-Bit Server VM (build 13+33, mixed mode, sharing) [root@localhost java]#

2、安装和配置 elasticsearch 创建 elasticsearch 文件夹： [root@localhost ~]# mkdir /ext/elk/elasticsearch/

上传tar包并解压 wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.2-linux-x86_64.tar.gz [root@localhost elasticsearch]# tar -zxvf elasticsearch-7.3.2-linux-x86_64.tar.gz

开始 elasticsearch 的配置： [root@localhost elasticsearch]# cd /ext/elk/elasticsearch/elasticsearch-7.3.2/config/ 配置 elasticsearch.yml 文件：(单机情况，配置如下四项即可) #----------------------------------------------------------# cluster.name: elasticsearch # 配置集群名称，要小写，必需 node.name: es001 # 配置节点名称，必需 network.host: 0.0.0.0 # 配置该项，使外界可访问 ES 服务，必需，记得开放端口 http.port: 9200 # 配置对外服务的端口号，默认是9200，必需 cluster.initial_master_nodes: ["es001"] # 初始化主节点的节点名称，必需 bootstrap.memory_lock: false # 使用交换分区 #----------------------------------------------------------# 配置文件 elasticsearch.yml 详解：https://www.cnblogs.com/chuijingjing/p/10023783.html

修改系统的 sysctl.conf 配置文件： [root@localhost config]# gedit /etc/sysctl.conf 在文件最后增加如下配置项： vm.max_map_count=655360 fs.file-max=655360 验证修改是否成功： [root@localhost config]# sysctl -p 显示新增的配置项，说明修改成功： vm.max_map_count = 655360 # 调整虚拟内存 fs.file-max = 655360 # 调整最大并发连接数

修改文件限制相关参数的配置文件 limits.conf： [root@localhost config]# gedit /etc/security/limits.conf 增加如下内容：

- hard nofile 65536
- soft nofile 65536
- soft nproc 65536
- hard nproc 65536
- soft memlock unlimited
- hard memlock unlimited

修改进程数配置文件 20-nproc.conf： [root@localhost config]# gedit /etc/security/limits.d/20-nproc.conf 里面的内容为：

- soft nproc 4096 root soft nproc unlimited 不需要调整了。

由于 elasticsearch 不能使用 root 账号启动，所以需要把 elasticsearch 授权给 es_shanhai： chown -R es_shanhai:es_group /ext/elk/elasticsearch/elasticsearch-7.3.2

切换到 es_shanhai 并启动 elasticsearch： [root@localhost elasticsearch-7.3.2]# su es_shanhai [es_shanhai@localhost elasticsearch-7.3.2] ./elasticsearch

端口开放和生效： [root@localhost ~]# firewall-cmd --add-port=9200/tcp --permanent [root@localhost ~]# firewall-cmd --add-port=9300/tcp --permanent [root@localhost ~]# firewall-cmd --reload

在宿主机和虚拟机访问 http://192.168.242.131:9200/ 查看结果

创建软连接： ln -s /ext/elk/elasticsearch/elasticsearch-7.3.2/bin/elasticsearch /usr/bin/elasticsearch 删除软连接： rm -rf /usr/bin/elasticsearch

ELK搭建————elasticsearch7.3.0安装： https://blog.csdn.net/liuwenbiao1203/article/details/100539826 ElasticSearch系列（三）： https://blog.csdn.net/zhanyu1/article/details/88927194 elasticsearch 启动报错 ERROR: [1] bootstrap checks failed: https://blog.csdn.net/qq_36608921/article/details/92803959 ELK搭建过程中出现的问题与解决方法汇总： https://www.cnblogs.com/hellxz/p/11057234.html

3、安装和配置 logstash

创建 logstash 文件夹： [root@localhost elk]# mkdir /ext/elk/logstash/

上传并解压 tar 压缩包： wget https://artifacts.elastic.co/downloads/logstash/logstash-7.3.2.tar.gz tar -zxvf logstash-7.3.2.tar.gz

测试 logstash 启动是否正常： [root@localhost ~]# cd /ext/elk/logstash/logstash-7.3.2/bin/ [root@localhost bin]# ./logstash -e 'input{ stdin{ } } output { stdout { } }' 结果如下： ……Successfully started Logstash API endpoint {:port=>9600} 看到 Successfully started Logstash API endpoint {:port=>9600} 说明启动成功。 在 logstash 启动成功之后的光标处输入 Hello World，结果如下： Hello World /ext/elk/logstash/logstash-7.3.2/vendor/bundle/jruby/2.5.0/gems/awesome_print-1.7.0/lib/awesome_print/formatters/base_formatter.rb:31: warning: constant ::Fixnum is deprecated { "message" => "Hello World", "@timestamp" => 2019-09-19T05:48:05.416Z, "host" => "localhost", "@version" => "1" }

创建软连接： ln -s /ext/elk/logstash/logstash-7.3.2/bin/logstash /usr/bin/logstash

创建 logstash.conf 配置文件： 在 /ext/elk/logstash/logstash-7.3.2/bin/ 目录下创建 logstash.conf 配置文件，内容如下： input{ stdin{ } } output{ stdout{ codec => rubydebug{ } } } 在终端输入 logstash -f /ext/elk/logstash/logstash-7.3.2/bin/logstash.conf 进行启动，输入 Hello World 结果与上面一样。 到这里说明 Logstash 的安装和配置没有问题。

参考： logstash配置文件 https://www.cnblogs.com/xiaobaozi-95/p/9214307.html 一文快速上手Logstash https://cloud.tencent.com/developer/article/1353068 LogStash日志分析系统 https://www.cnblogs.com/xiaocen/p/3717849.html

4、安装和配置 kibana

创建 kibana 文件夹： [root@localhost ~]# mkdir /ext/elk/kibana/

上传并解压 tar 压缩包： wget https://artifacts.elastic.co/downloads/kibana/kibana-7.3.2-linux-x86_64.tar.gz [root@localhost kibana]# tar -zxvf kibana-7.3.2-linux-x86_64.tar.gz

修改 kibana.yml 配置文件： [root@localhost kibana]# cd kibana-7.3.2-linux-x86_64/config/ [root@localhost config]# gedit kibana.yml 修改内容如下：

# 启动 kibana 的远程访问

server.host: "0.0.0.0"

# 配置 es 访问地址

elasticsearch.hosts: ["http://192.168.242.131:9200/"]

# 汉化界面

i18n.locale: "zh-CN"

授权可访问的用户组： 由于 kibana 与 elasticsearch 一样，不能使用 root 账号启动，所以需要把 kibana 授权给 es_shanhai： chown -R es_shanhai:es_group /ext/elk/kibana/kibana-7.3.2-linux-x86_64

启动 kibana 服务： cd /ext/elk/kibana/kibana-7.3.2-linux-x86_64/bin [root@localhost bin]# su es_shanhai [es_shanhai@localhost bin]$ ./kibana 启动结果如下： log [07:46:16.616] [info](#) Server running at http://0.0.0.0:5601 log [07:46:16.624] [info](#)[Kibana](#) http server running log [07:46:17.164] [info](#)[plugin:spaces@7.3.2] Status changed from yellow to green - Ready 说明启动成功，且本地访问地址为 http://0.0.0.0:5601 为了使外网可以访问，我们把 5601 端口开放。

端口开放和生效： [root@localhost ~]# firewall-cmd --add-port=5601/tcp --permanent [root@localhost ~]# firewall-cmd --reload

在宿主机和虚拟机访问 http://192.168.242.131:5601/ 查看结果

Kibana（一张图片胜过千万行日志） https://www.cnblogs.com/cjsblog/p/9476813.html

Kibana快速介绍： https://www.jianshu.com/p/8001ac47c378

\#----------------------------------------------------------# Elasticsearch 配置文件 elasticsearch.yml 的配置项说明： #----------------------------------------------------------# #ES集群名称，同一个集群内的所有节点集群名称必须保持一致 cluster.name: ES-Cluster

\#ES集群内的节点名称，同一个集群内的节点名称要具备唯一性 node.name: ES-master-192.168.0.201

\#允许节点是否可以成为一个master节点，ES是默认集群中的第一台机器成为master，如果这台机器停止就会重新选举 node.master: true

\#允许该节点存储索引数据（默认开启） node.data: false

\#path可以指定多个存储位置 path.data: /ext/elasticsearch/data

\#elasticsearch专门的日志存储位置，生产环境中建议elasticsearch配置文件与elasticsearch日志分开存储 path.logs: /ext/elasticsearch/logs

\#在ES运行起来后锁定ES所能使用的堆内存大小，锁定内存大小一般为可用内存的一半左右；锁定内存后就不会使用交换分区 #如果不打开此项，当系统物理内存空间不足，ES将使用交换分区，ES如果使用交换分区，那么ES的性能将会变得很差 bootstrap.memory_lock: true

\#es绑定地址，支持IPv4及IPv6，默认绑定127.0.0.1；es的HTTP端口和集群通信端口就会监听在此地址上 network.host: 192.168.0.201

\#是否启用tcp无延迟，true为启用tcp不延迟，默认为false启用tcp延迟 network.tcp.no_delay: true

\#是否启用TCP保持活动状态，默认为true network.tcp.keep_alive: true

\#是否应该重复使用地址。默认true，在Windows机器上默认为false network.tcp.reuse_address: true

\#tcp发送缓冲区大小，默认不设置 network.tcp.send_buffer_size: 128mb

\#tcp接收缓冲区大小，默认不设置 network.tcp.receive_buffer_size: 128mb

\#设置集群节点通信的TCP端口，默认就是9300 transport.tcp.port: 9300

\#设置是否压缩TCP传输时的数据，默认为false transport.tcp.compress: true

\#设置http请求内容的最大容量，默认是100mb http.max_content_length: 200mb

\#是否开启跨域访问 http.cors.enabled: true

\#开启跨域访问后的地址限制，表示无限制 http.cors.allow-origin: ""

\#定义ES对外调用的http端口，默认是9200 http.port: 9200

\#Elasticsearch7新增参数，写入候选主节点的设备地址，来开启服务时就可以被选为主节点,由discovery.zen.ping.unicast.hosts:参数改变而来 discovery.seed_hosts: ["192.168.0.201:9300"]

\#Elasticsearch7新增参数，写入候选主节点的设备地址，来开启服务时就可以被选为主节点 cluster.initial_master_nodes: ["192.168.0.201:9300"]

\#Elasticsearch7新增参数，设置每个节点在选中的主节点的检查之间等待的时间。默认为1秒 cluster.fault_detection.leader_check.interval: 15s

\#Elasticsearch7新增参数，启动后30秒内，如果集群未形成，那么将会记录一条警告信息，警告信息未master not fount开始，默认为10秒 discovery.cluster_formation_warning_timeout: 30s

\#Elasticsearch7新增参数，节点发送请求加入集群后，在认为请求失败后，再次发送请求的等待时间，默认为60秒 cluster.join.timeout: 120s

\#Elasticsearch7新增参数，设置主节点等待每个集群状态完全更新后发布到所有节点的时间，默认为30秒 cluster.publish.timeout: 90s

\#集群内同时启动的数据任务个数，默认是2个 cluster.routing.allocation.cluster_concurrent_rebalance: 32

\#添加或删除节点及负载均衡时并发恢复的线程个数，默认4个 cluster.routing.allocation.node_concurrent_recoveries: 32

\#初始化数据恢复时，并发恢复线程的个数，默认4个 cluster.routing.allocation.node_initial_primaries_recoveries: 32 #----------------------------------------------------------#