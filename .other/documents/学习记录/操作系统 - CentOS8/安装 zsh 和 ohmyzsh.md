安装 zsh: https://www.zsh.org/

```shell
yum -y install zsh
```

查看安装结果

```shell
zsh --version
```

修改默认的 shell

```shell
chsh -s $(which zsh)
```

安装 ohmyzsh: https://ohmyz.sh/

```shell
# 以下三种方式选择一种即可:
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sh -c "$(fetch -o - https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

安装时，出现如下错误信息:

```shell
curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to raw.githubusercontent.com:443
```

解决方式如下:

```shell
找不到解决方法。
```



配置文件

```shell
vim ~/.zshrc
```

