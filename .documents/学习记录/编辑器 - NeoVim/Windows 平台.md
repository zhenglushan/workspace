# 软件安装

## 安装 `NeoVim`

打开 `https://github.com/neovim/neovim/releases` 进行下载。
用户手册 `https://neovim.io/doc/user/`
配置文件地址 `https://github.com/neovim/neovim/wiki/Installing-Neovim` 查找 `%userprofile%\AppData\Local\nvim\init.vim` 即可看到，配置文件对应的地址为 `C:\Users\Administrator\AppData\Local\nvim\init.vim` 文件。

## 安装 `vim-plug` 插件管理器

打开 `https://github.com/junegunn/vim-plug` 查看安装方式，在 `Windows(PowerShell)` 平台的安装代码如下：

```shell
iwr -useb https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim |`
    ni "$env:LOCALAPPDATA/nvim-data/site/autoload/plug.vim" -Force
```

安装后的最终地址为：`C:\Users\Administrator\AppData\Local\nvim-data\site\autoload\plug.vim` 文件。

## 启动 `vim-plug` 插件管理器

打开 `init.vim` 配置文件，添加如下代码：

```shell
" 插件管理 {{{
    call plug#begin("~/NeoVim/plugged")
    call plug#end()
" }}}
```

即可启用 `vim-plug` 插件管理器。

## 为 `Win10` 打造类 `Linux` 终端

我们通过配置 `Git Bash` 来实现类 `Linux` 终端。

### 快捷键配置

1、`Git Bash` → 打开文件位置 → 右键属性：
→ 快捷方式 → 快捷键 → Ctrl + Alt + T
→ 快捷方式 → 高级 → √ 用管理员身份运行
2、解决快捷键延迟问题
服务 → 以管理员身份运行 → `SysMain`(或旧名 `superFetch`) → 属性：
→ 服务状态: 已停止 → 启动类型: 禁用
→ 恢复 → 第一次失败和第二次失败 → 无操作
→ 重启系统

### 修改命令提示符

`https://juejin.im/post/6844903700775845895`





# 安装插件

## 安装 `coc.nvim` 代码补全插件

`coc.nvim` 插件地址 `https://github.com/neoclide/coc.nvim`
该插件安装的步骤如下：
1、安装 `nodejs (https://nodejs.org/en/download/)` ≥ 10.12 版本
2、在 `vim-plug` 添加如下代码：
```shell
Plug 'neoclide/coc.nvim', {'branch': 'release'}
```
然后启动 `NeoVim` 执行如下命令：
```shell
:PlugInstall
```
即可进行 `coc.nvim` 插件的安装。

### 配置 `前端` 代码补全插件
这里是指包括 `HTML`、`CSS` 和 `JavaScript`、`TypeScript` 四个方面的代码补全：


### 配置 `PHP` 代码补全插件

#### 配置 `Laravel` 代码补全插件

### 配置 `Python` 代码补全插件
### 配置 `Java` 代码补全插件
### 配置 `Go` 代码补全插件
### 配置 `C` 和 `C++` 代码补全插件
### 配置 `C#` 代码补全插件

## 安装 `NERDTree` 目录树插件

该插件的地址为 `https://github.com/preservim/nerdtree`
安装方式 `Plug 'preservim/nerdtree'`
打开命令 `:NERDTree`
常用配置如下：

```shell
map <C-n> :NERDTreeToggle<CR>
let g:NERDTreeDirArrowExpandable = '▸'
let g:NERDTreeDirArrowCollapsible = '▾'
```



## 安装 `vim-airline` 状态栏插件

## 安装 `fzf` 文件查找插件

## 安装 `ctags` 代码跳转插件

插件地址 `https://github.com/universal-ctags/ctags`






