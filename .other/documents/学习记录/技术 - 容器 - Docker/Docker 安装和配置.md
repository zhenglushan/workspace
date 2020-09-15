安装 Docker 依赖包：

 yum install -y yum-utils device-mapper-persistent-data lvm2

安装 Docker 环境：

 yum install docker

运行 Docker 服务：

 service docker start
 service docker restart
 service docker stop
 service docker status

验证 Docker 安装结果：

 docker info

或者

 docker version

例如：

 [root@localhost ~]## docker version
 Client:
 Version:     1.13.1
 API version:   1.26
 Package version: docker-1.13.1-103.git7f2769b.el7.centos.x86_64
 Go version:   go1.10.3
 Git commit:   7f2769b/1.13.1
 Built:      Sun Sep 15 14:06:47 2019
 OS/Arch:     linux/amd64
 ​
 Server:
 Version:     1.13.1
 API version:   1.26 (minimum version 1.12)
 Package version: docker-1.13.1-103.git7f2769b.el7.centos.x86_64
 Go version:   go1.10.3
 Git commit:   7f2769b/1.13.1
 Built:      Sun Sep 15 14:06:47 2019
 OS/Arch:     linux/amd64
 Experimental:   false
 [root@localhost ~]##

安装过程参考官网：https://docs.docker.com/install/linux/docker-ce/centos/

参考资料：

[Docker 百度百科](https://baike.baidu.com/item/Docker/13344470)

[这可能是最为详细的Docker入门吐血总结](https://mp.weixin.qq.com/s/a5fnVpXH1xCtgXHu6jg1LQ)

[Docker 入门教程](http://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html)

[Docker 微服务教程](http://www.ruanyifeng.com/blog/2018/02/docker-wordpress-tutorial.html)

[Docker 核心技术与实现原理](http://dockone.io/article/2941)

[Docker——入门实战](https://blog.csdn.net/bskfnvjtlyzmv867/article/details/81044217)

[《Docker从入门到实践》阅读笔记](https://www.jianshu.com/p/ca2a98e42f4d)

[Docker 中文文档](https://docker_practice.gitee.io/zh-cn/basic_concept/image.html)

京东书籍：

[Kubernetes权威指南：从Docker到Kubernetes实践全接触（第4版）](https://item.jd.com/12601558.html)

图书馆借阅：

[每天5分钟玩转 Kubernetes](http://interweb.xmlib.net/opac/book/3003720936)

[深入浅出 Docker](http://interweb.xmlib.net/opac/book/3003910143)

视频教程列表：

https://blog.csdn.net/u010600274/article/details/100761657