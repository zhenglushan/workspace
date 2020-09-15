# Git 常见操作

## 平台到本地

过程如下：

```shell
mkdir dirname
cd dirname
git init
git pull http………….git
```

比如：

```shell
mkdir Python-100-Days
cd Python-100-Days
git init
git pull https://github.com/jackfrued/Python-100-Days.git
```

## 本地到平台

### 1、平台创建仓库

首先在平台创建一个私有或者公有项目；

### 2、本地提交项目

步骤如下：

```shell
git init
git add *
git commit -m "项目评论信息"
git remote add origin http……………………/平台创建的仓库名称.git
git push -u origin master
```

举例如下：

```shell
git init
git add *
git commit -m "提交到 Gitee 平台托管"
git remote add origin https://gitee.com/zhenglushan/data_collection.git
git push -u origin master
```



## 常见错误

### nothing added to commit but untracked files present

如果操作时出现 nothing added to commit but untracked files present 错误，说明没有进行 add 操作，我们需要进行 add 操作，参考代码如下：

```shell
git add *
```

需要执行 git add * 添加要提交的文档，可使用 * 模糊匹配。

