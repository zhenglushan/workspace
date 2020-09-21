# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 引号转成实体.py
# @DATETime   : 2020/5/19 10:36
# @Author     : 笑看风云
import html

s = html.escape("Hlelo ' \" fwfe’ “")
print(s)
