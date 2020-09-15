### 安装 `i3` 桌面

#### 安装 `sddm` 登录器

```shell
sudo pacman -S sddm
sudo systemctl enable sddm
```

#### 安装 `xorg-xinit`  图形界面

```shell
sudo pacman -S xorg-server xorg-xinit
```

#### 安装 `i3wm` 桌面管理器

```shell
sudo pacman -S i3-gaps
```

`i3-gaps` 属于 `i3wm` 的一个分支，提供了更多的特性。

`i3` 配置文件的地址为：`~/.config/i3/config`，可以把 `/etc/i3/config` 复制过来，或者执行如下命令来生成：

```shell
i3-config-wizard
```

#### 安装终端

```shell
sudo pacman -S mate-terminal
```

然后 `reboot` 重启系统。

### 安装 `i3` 美化软件

| 软件名称  | 简介                           |
| --------- | ------------------------------ |
| `compton` | 提供窗口透明支持               |
| `polybar` | 状态条                         |
| `rofi`    | 快捷程序启动，也可以装 `dmunu` |
| `feh`     | 设置墙纸                       |

#### 安装 `compton` 软件

```shell
sudo pacman -S compton
```

#### 安装 `polybar` 软件

```shell
sudo pacman -S polybar
```

#### 安装 `rofi` 软件

```shell
sudo pacman -S rofi
```

#### 安装 `feh` 软件

```shell
sudo pacman -S feh
```

随机切换墙纸：

```shell
feh --randomize --bg-fill ~/Images
```

`i3` 配置随机切换墙纸：

```shell
exec feh --randomize --bg-fill ~/Images
```

#### 安装 `mate-utils` 软件：

```shell
sudo pacman -S mate-utils
```

该软件用于截图。



### 配置 `i3` 美化桌面

```shell
nano ~/.config/i3/config
```

添加如下配置信息：

```shell








```





