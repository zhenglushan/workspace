在终端输入：

```shell
$PROFILE
```

显示如下结果：

```shell
C:\Users\Administrator\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

这个就是 `PowerShell` 的配置文件的位置，因此我们需要分别创建目录和文件 `WindowsPowerShell` 和 `Microsoft.PowerShell_profile.ps1` 。

我们在配置文件中加入如下信息：

```shell
<# 带参数的命令映射 #>

# 打开 NeoVim 配置文件
function fun_nvim_config {
	nvim $env:USERPROFILE\AppData\Local\nvim\init.vim
}
Set-Alias nvc fun_nvim_config

# 切换到 NeoVim 子配置文件目录
function fun_nvc_dir {
	cd $env:USERPROFILE\AppData\Local\nvim\vim-config\
}
Set-Alias nvcdir fun_nvc_dir

# 打开 hosts 文件
function fun_subl_hosts {
	subl $env:SYSTEMROOT\System32\drivers\etc\hosts
}
Set-Alias sublhosts fun_subl_hosts

# 映射 vim 到 nvim 命令
Set-Alias vim nvim

```



编辑完成之后，启动提示如下错误信息：

```shell
. : 无法加载文件 C:\Users\Administrator\Documents\WindowsPowerShell\Microsoft.PowerSh
ell_profile.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅 https:/go.microsoft
.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
```

执行如下命令：

```shell
PS C:\Users\Administrator>> Set-ExecutionPolicy RemoteSigned

执行策略更改
执行策略可帮助你防止执行不信任的脚本。更改执行策略可能会产生安全风险，如
https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies
帮助主题所述。是否要更改执行策略?
[Y] 是(Y)  [A] 全是(A)  [N] 否(N)  [L] 全否(L)  [S] 暂停(S)  [?] 帮助
(默认值为“N”):A
PS C:\Users\Administrator>>
```

然后重启 `PowerShell` 终端即可。

