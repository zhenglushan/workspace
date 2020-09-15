```shell
#  创建数据库
drop database if exists `my_cms`;
create database `my_cms` default character set utf8mb4 collate utf8mb4_general_ci;

# 创建 user 表结构
drop table if exists `user`;
create table `user`
(
    `id`                int(10) unsigned    not null auto_increment comment '用户ID',
    `username`          varchar(50)         not null default '' comment '用户名',
    `email`             varchar(50)         not null default '' comment '用户邮箱',
    `email_is_verified` tinyint(1) unsigned not null default 0 comment '邮箱是否校验: 0 未校验 1 已校验',
    `email_verified_at` int(10) unsigned    not null default 0 comment '邮箱校验时间戳',
    `password`          char(32)            not null default '' comment '用户密码, MD5 固定长度 32 位',
    `mobile`            varchar(30)         not null default '' comment '用户手机号',
    `fax`               varchar(30)         not null default '' comment '用户传真号',
    `wechat`            varchar(30)         not null default '' comment '用户微信号',
    `gender`            tinyint(1) unsigned not null default 0 comment '用户性别: 0 男 1 女',
    `address`           varchar(50)         not null default '' comment '用户住址',
    `reg_date`          int(10) unsigned    not null default 0 comment '用户注册时间戳',
    `last_login_date`   int(10) unsigned    not null default 0 comment '用户最后登录时间戳',
    primary key (id)
);

# 创建 category 表结构
drop table if exists `category`;
create table `category`
(
    `id`           smallint(6) unsigned not null auto_increment comment '分类ID',
    `reid`         smallint(6) unsigned not null default 0 comment '父类ID',
    `name`         varchar(250)         not null default '' comment '分类名称',
    `pinyin`       varchar(250)         not null default '' comment '分类拼音',
    `title`        varchar(250)         not null default '' comment '分类标题',
    `keywords`     varchar(250)         not null default '' comment '分类关键词',
    `description`  varchar(250)         not null default '' comment '分类描述',
    `introduction` varchar(250)         not null default '' comment '分类介绍',
    `is_show`      tinyint(1) unsigned  not null default 1 comment '是否展示: 1 展示 0 不展示',
    `litpic`       varchar(100)         not null default '' comment '分类缩略图',
    `backpic`      varchar(100)         not null default '' comment '分类背景图',
    `content`      text comment '分类正文',
    primary key (id) comment '分类主键'
);

# 创建 article 文章表
drop table if exists `article`;
create table `article`
(
    `id`          int(10) unsigned      not null auto_increment comment '文章ID',
    `cate_id`     smallint(6) unsigned  not null default 0 comment '分类ID',
    `title`       varchar(250)          not null default '' comment '文章标题',
    `keywords`    varchar(250)          not null default '' comment '文章关键词',
    `description` varchar(250)          not null default '' comment '文章描述',
    `pubdate`     int(10) unsigned      not null default 0 comment '文章发布时间戳',
    `click`       mediumint(8) unsigned not null default 0 comment '文章点击量',
    `writer`      varchar(50)           not null default '' comment '文章作者',
    `source`      varchar(50)           not null default '' comment '文章来源',
    `is_show`     tinyint(1) unsigned   not null default 1 comment '是否展示: 1 展示 0 不展示',
    `litpic`      varchar(100)          not null default '' comment '文章缩略图',
    `content`     text comment '文章正文',
    primary key (id) comment '文章主键'
);

# 创建 tag 表结构
drop table if exists `tag`;
create table `tag`
(
    `id`           int(10) unsigned not null auto_increment comment '标签ID',
    `name`         varchar(250)     not null default '' comment '标签名称',
    `pinyin`       varchar(250)     not null default '' comment '标签拼音',
    `title`        varchar(250)     not null default '' comment '标签标题',
    `keywords`     varchar(250)     not null default '' comment '标签关键词',
    `description`  varchar(250)     not null default '' comment '标签描述',
    `introduction` varchar(250)     not null default '' comment '标签简介',
    `pubdate`      int(10) unsigned not null default 0 comment '标签发布时间戳',
    `jump_url`     varchar(50)      not null default '' comment '标签跳转地址',
    primary key (id) comment '标签主键',
    key `pinyin` (`pinyin`) comment '标签索引键'
);

# 创建 article 和 category、tag 的中间表
drop table if exists `article_tag_category`;
create table `article_tag_category`
(
    `article_id` int(10) unsigned     not null default 0 comment '文章ID',
    `cate_id`    smallint(5) unsigned not null default 0 comment '分类ID',
    `tag_id`     int(10) unsigned     not null default 0 comment '标签ID'
);

# 创建 topic 表结构
drop table if exists `topic`;
create table `topic`
(
    `id`           int(10) unsigned      not null auto_increment comment '专题ID',
    `aids`         varchar(250)          not null default '' comment '专题相关联的文章ID',
    `name`         varchar(250)          not null default '' comment '专题名称',
    `pinyin`       varchar(250)          not null default '' comment '专题拼音',
    `title`        varchar(250)          not null default '' comment '专题标题',
    `keywords`     varchar(250)          not null default '' comment '专题关键词',
    `description`  varchar(250)          not null default '' comment '专题描述',
    `introduction` varchar(250)          not null default '' comment '专题简介',
    `pubdate`      int(10) unsigned      not null default 0 comment '专题发布时间戳',
    `jump_url`     varchar(50)           not null default '' comment '专题跳转地址',
    `writer`       varchar(50)           not null default '' comment '专题作者',
    `source`       varchar(50)           not null default '' comment '专题来源',
    `is_show`      tinyint(1) unsigned   not null default 1 comment '是否展示: 1 展示 0 不展示',
    `click`        mediumint(8) unsigned not null default 0 comment '专题点击量',
    `litpic`       varchar(100)          not null default '' comment '专题缩略图',
    `content`      text comment '专题正文',
    primary key (id) comment '专题主键',
    key `pinyin` (`pinyin`) comment '专题索引建'
);

# 创建 search 表结构
drop table if exists `search`;
create table `search`
(
    `id`           int(10) unsigned not null auto_increment comment '搜索ID',
    `name`         varchar(250)     not null default '' comment '搜索名称',
    `pinyin`       varchar(250)     not null default '' comment '搜索拼音',
    `title`        varchar(250)     not null default '' comment '搜索标题',
    `keywords`     varchar(250)     not null default '' comment '搜索关键词',
    `description`  varchar(250)     not null default '' comment '搜索描述',
    `introduction` varchar(250)     not null default '' comment '搜索简介',
    `pubdate`      int(10) unsigned not null default 0 comment '搜索发布时间戳',
    `jump_url`     varchar(50)      not null default '' comment '搜索跳转地址',
    primary key (id) comment '搜索主键',
    key `pinyin` (`pinyin`) comment '搜索索引键'
);

# 创建 sysconf 表结构
drop table if exists `sysconf`;
create table `sysconf`
(
    `id`      int(10) unsigned not null auto_increment comment '配置项ID',
    `varname` varchar(50)      not null default '' comment '配置项变量名',
    `value`   varchar(50)      not null default '' comment '配置项变量值',
    `info`    varchar(100)     not null default '' comment '配置项文字说明',
    primary key (id) comment '配置项主键'
);

```

