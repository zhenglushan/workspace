1、一个栏目对应一个分表；首先进入“频道模型”找到“普通文章”，“普通文章”后面有个复制操作，看到了就点击复制，这样就能增加一个单独的表了，也就是分表。

2、arclist 最新、热门、推荐、头条替换成 freelist 列表；

在织梦中 `flag` 字段经常属于查询条件，所以可以创建索引。

索引的创建是在定义表结构的时候设置的，比如 dedecms 的 sql-dftables.txt，如下：

```shell
primary key (`id`),

key `sortrank` (`sortrank`),

key `mainindex` (`arcrank`,`typeid`,`channel`,`flag`,`mid`),

key `lastpost` (`lastpost`,`scores`,`goodpost`,`badpost`,`notpost`)
```

参考文章[重点参考前两篇]:

dedecms数据负载性能优化方案简单几招让你dedecms提速n倍

http://www.adminwu.cn/art/45.html

dedecms负载性能优化实例 三招让你的dedecms快10倍以上

http://www.adminwu.cn/art/46.html

教你用 DEDECMS 快速制作电影站点:

https://www.genban.org/news/dedecms-6082.html

织梦 CMS 怎么利用小说模块搭建小说站和漫画站:

https://www.genban.org/news/dedecms-18819.html

织梦模板dedecms数据库分表储存数据负载性能优化

http://www.dede58.com/a/dedejq/10949.html

织梦dedecms自由列表freelist调用增加排序方式

http://www.dede58.com/a/dedejq/3392.html

dedecms数据负载性能优化方案简单几招让你提速n倍

https://blog.csdn.net/nczb007/article/details/72808581

dede自由列表的＂不使用目录默认主页＂错误修正

https://www.chaofanseo.com/seo-15-1583.html

dedecms 织梦 数据量达到几十万 生成速度很慢

https://blog.csdn.net/qq_40599116/article/details/82862931

mysql数据库中的索引有那些、有什么用

https://www.2cto.com/database/201707/660712.html

mysql 教程

http://www.runoob.com/mysql/mysql-tutorial.html

实战Nginx与PHP（FastCGI）的安装、配置与优化

https://www.cnblogs.com/lidabo/p/4212419.html

php7 + php-fpm + nginx 完整源码编译安装 2018年08月02日 14:00:17

https://blog.csdn.net/ghostyusheng/article/details/81357638

织梦5.7最新字母检索插件

https://download.csdn.net/download/qiwen5de111/4764318

MySQL 分库分表方案，总结的非常好！

https://blog.csdn.net/qq_39940205/article/details/80536666

mysql分库分表实战及php代码操作完整实例

https://blog.csdn.net/nuli888/article/details/52143065

php实现mysql分表

https://blog.csdn.net/m_nanle_xiaobudiu/article/details/81096344