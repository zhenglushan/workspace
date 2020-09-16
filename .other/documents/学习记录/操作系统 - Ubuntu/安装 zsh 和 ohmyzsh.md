### 安装 zsh

https://www.zsh.org/

```shell
sudo apt install zsh
```

查看安装结果

```shell
zsh --version
```

修改默认的 shell

```shell
chsh -s $(which zsh)
```

### 安装 ohmyzsh

https://ohmyz.sh/

在安装 `ohmyzsh` 之前，需要先修改下 `hosts` 文件的内容：

首先打开 `https://www.ipaddress.com/` 查询 `raw.githubusercontent.com` 的 `ip` 地址为 `199.232.68.133`

然后在终端输入如下命令：

```shell
sudo vim /etc/hosts
```

添加如下内容：

```shell
199.232.68.133   raw.githubusercontent.com
199.232.68.133   user-images.githubusercontent.com
199.232.68.133   avatars2.githubusercontent.com
199.232.68.133   avatars1.githubusercontent.com
```

然后再执行如下安装 `ohmyzsh` 命令：

```shell
# 以下三种方式选择一种即可:
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sh -c "$(fetch -o - https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

就不会出现如下错误信息:

```shell
curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to raw.githubusercontent.com:443
```

出现这个错误信息的原因是由于我们之前用站长工具查询 `raw.githubusercontent.com` 得到的 `IP` 来解析导致的。

附带 `DNS` 查询网址：
http://www.webkaka.com/dns/
https://tools.ipip.net/dns.php

### 修改配置文件

```shell
vim ~/.zshrc
```

添加终端命令别名：

```shell
alias nvcfg="nvim ~/.config/nvim/init.vim"
```

