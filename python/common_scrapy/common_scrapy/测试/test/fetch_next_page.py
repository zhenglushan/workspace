# -*- coding:utf-8 -*-
import re

text = "<div class=\"pagenavi\"><li>首页</li>\
<li class=\"thisclass\">1</li>\
<li><a href='list_1_2.html'>2</a></li>\
<li><a href='list_1_3.html'>3</a></li>\
<li><a href='list_1_4.html'>4</a></li>\
<li class=\"thisclass\">9</li>\
<li><a href='list_1_5.html'>5</a></li>\
<li><a href='list_1_2.html'>下一页</a></li>\
<li><a href='list_1_142.html'>末页</a></li>\
	</div>"

qz_reg = "<div class=[\"\']pagenavi[\"\']>.*?<li class=[\"\']thisclass[\"\']>\d+</li>"
hz_reg = "<li><a href=[\"\'](.*?)[\"\']>\d+</a></li>"
full_reg = qz_reg + ".*?" + hz_reg

result = re.findall(full_reg, text, flags=re.I | re.S)
if result:
    print(result[0])
