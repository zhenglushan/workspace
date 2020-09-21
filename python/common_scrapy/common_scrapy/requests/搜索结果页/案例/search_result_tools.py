# -*- coding:utf-8 -*-

import re
from random import choice


def raplace_domains(str):
    '''
    把正文中包含的网址都替换为空
    '''
    fix_str = "jpg|jpeg|png|gif|bmp|psd|tiff|tga|eps|JPG|JPEG|PNG|GIF|BMP|PSD|TIFF|TGA|EPS"
    re_sub = "(http:\/\/|https:\/\/){0,1}(www.){0,1}[0-9a-zA-Z\-]+\.((?!" + fix_str + ")[a-zA-Z\.])+[\/]{0,1}"
    str = re.sub(re_sub, "", str, flags=re.S)
    return str


def replace_qihoo360(str):
    # 字符串替换
    str = str.replace("【", "").replace("】", "").replace("_", "").replace("-", "").replace("|", "")
    str = str.replace("...", "").replace("\r", '').replace("\n", '').replace("\t", '').replace(' ', '')
    str = str.replace('&nbsp;', '').replace("发贴时间：", '').replace("[图文]", '').replace("  ", " ").strip()

    # 正则替换
    re_sub = "</?[^>]*>"
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    re_sub = "[ ]+"
    str = re.sub(re_sub, " ", str, flags=re.S | re.I)
    re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日-'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    str = str.replace('...', choice(['。', '？', '！']))
    re_sub = '\d{1,4}-\d{1,2}-\d{1,2}'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)

    str = str.strip()
    return str
