" 普通设置 {{{
	set nu " 显示行号
	set cursorline " 突出显示当前行
	set showmatch " 显示括号匹配
	set tabstop=4 " 设置 Tab 长度为 4 个空格
	set guifont=Powerline_Consolas:h14:cDEFAULT
	set shiftwidth=4 " 设置自动缩进长度为 4 个空格
	set autoindent " 继承前一行的缩进方式，用于多行注释
	set laststatus=2 " 总是显示状态栏
	set ruler " 显示光标当前位置
" }}}
" ========================= 分隔符 =========================
" 插件管理 {{{
call plug#begin("~/NeoVim/plugged")
	" 代码补全插件 {{{
		Plug 'neoclide/coc.nvim', {'branch': 'release'}
	" }}}
	" 目录树插件 {{{
		Plug 'preservim/nerdtree'
	" }}}
	" 状态栏插件 {{{
		Plug 'vim-airline/vim-airline'
		Plug 'vim-airline/vim-airline-themes'
	" }}}
		Plug 'jvanja/vim-bootstrap4-snippets'	



call plug#end()
" ========================= 分隔符 =========================
" }}}
" 插件配置 {{{
	" NERDTree 配置 {{{
	
	" }}}
	" vim-airline 配置 {{{
		" 更多主题 plugged/vim-airline-themes/autoload/airline/themes
		
		" 显示顶部状态栏， 打开后，tabline和tmuxline都可以得到增强
		set encoding=utf-8
		set langmenu=zh_CN.UTF-8

		" 显示颜色
		set t_Co=256 " 终端开启256色支持
		set laststatus=2  " 底部状态栏管理: 1 关闭, 2 开启

		" 自定义主题
		let g:airline_theme='onedark'

		" 安装字体后必须设置，除非安装相关字体，否则设置为 1 时，会出现乱码
		" 如果不是特别重要，可以设置为 0
		" 如果确定要设置为 1 则把 guifont 设置为 Powerline_Consolas 即可解决
		" 可能需要安装 Powerline 相关字体
		" 
		"
		let g:airline_powerline_fonts = 1

		" 开启tabline
		let g:airline#extensions#tabline#enabled = 1

		" tabline 中当前 buffer 两端的分隔字符
		let g:airline#extensions#tabline#left_sep = ' '

		" tabline 中未激活 buffer 两端的分隔字符
		let g:airline#extensions#tabline#left_alt_sep = '|'

		" tabline 中 buffer 显示编号
		let g:airline#extensions#tabline#buffer_nr_show = 1

		" 映射切换 buffer 的键位
		let g:airline_detect_modified=1
		let g:airline_detect_paste=1

	" }}}
	" vim-aireline-themes 配置 {{{
	
	" }}}
" }}}
