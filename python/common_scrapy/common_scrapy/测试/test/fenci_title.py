# -*- coding:utf-8 -*-

import re
import jieba
import jieba.analyse
import jieba.posseg as pseg
from ScrapyUploadImage.tools.commons import is_number

# title = '人体艺术模特潘娇娇大胆沐浴照'
#
# # allow_POS = "('n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng')"
# allow_POS = "('n', 'nr', 'ns', 'v', 'a')"
# result = jieba.cut(title)
# for item in result:
#     print(item)


content = '书写时代伟大传奇 习近平这些话暖心更提气不可阻挡的前进步伐  成就中国更加美好的明天我为祖国祝福 为创造更加美好的明天而奋斗盘点阅兵空中的"明星战机"  12亿人次流量咋实现的?战旗美如画 天地英雄气凛然 国庆专题空中受阅梯队“三剑客”齐聚飞越天安门'

result = jieba.cut(content)

for item in result:
    item = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", item)
    if len(item) > 0:
        print("----------------" + item + "----------------")
