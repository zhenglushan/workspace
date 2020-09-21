# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup


html = '''
<div class="pages">
<a href="//www.zx123.cn/zxlc/" rel="nofollow">首页</a><a href="//www.zx123.cn/zxlc/" rel="nofollow">上一页</a><a href="//www.zx123.cn/zxlc/"class='hovers' rel="nofollow">1</a><a href="//www.zx123.cn/zxlc/2.html" rel="nofollow">2</a><a href="//www.zx123.cn/zxlc/3.html" rel="nofollow">3</a><a href="//www.zx123.cn/zxlc/4.html" rel="nofollow">4</a><a href="//www.zx123.cn/zxlc/5.html" rel="nofollow">5</a><a href="//www.zx123.cn/zxlc/2.html" rel="nofollow">下一页</a><a href="//www.zx123.cn/zxlc/122.html" rel="nofollow">尾页</a>&nbsp;页次：<b><font color="red">1</font>/122</b><div style="clear: both;"></div>
'''

soup = BeautifulSoup(html, 'html5lib')
title = soup.select('a.hovers + a')
print(title[0].get('href'))



