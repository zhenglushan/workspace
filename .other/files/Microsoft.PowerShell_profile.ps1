<# 带参数的命令映射 #>

# 打开 NeoVim 配置文件
function fun_nvim_config {
	nvim $env:USERPROFILE\.SpaceVim.d\init.toml
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

# 打开 PowerShell 配置文件
function fun_subl_pwcfg {
	subl $env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
}
Set-Alias sublpwcfg fun_subl_pwcfg

# 打开 Cmder 历史命令文件
function fun_subl_cmder {
	subl C:\Cmder\config\.history
}
Set-Alias sublcmder fun_subl_cmder

# 映射 vim 到 nvim 命令
Set-Alias vim nvim
