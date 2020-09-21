# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : abuyun_for_company.py
# @DATETime   : 2020/3/9 10:53
# @Author     : 笑看风云

import base64

proxy_server = "http://http-pro.abuyun.com:9010/"

proxy_user = "HG852AT514B0W11D"
proxy_pass = "5EE9BE9B8B92882D"

proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
