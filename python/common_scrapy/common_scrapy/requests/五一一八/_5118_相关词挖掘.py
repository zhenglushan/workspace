# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : relatedKeyword.py
# @DATETime   : 2019/12/13 14:56
# @Author     : 笑看风云

import re
import requests
from urllib import parse
from time import sleep
from scrapy.http import HtmlResponse
from common_scrapy.requests.五一一八._5118_cookie import _5118_cookie

"""
获取 5118 相关关键词
https://www.5118.com/seo/newrelated/关键词
"""

related_url = "https://www.5118.com/seo/newrelated/"

headers = {
    'Host': 'www.5118.com',
    'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
    # Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)
}

cookiestr = _5118_cookie

if __name__ == '__main__':

    word_list = ["网络营销", "网络营销公司", "网络营销课程", "网络营销培训"]
    for word in word_list:
        newrelated_url = related_url + parse.quote(word)
        headers.update({'Cookie': cookiestr})
        resp = requests.get(newrelated_url, headers=headers)
        resp.encoding = 'UTF-8'
        response = HtmlResponse(url=newrelated_url, body=resp.text, encoding=resp.encoding)
        keyword_arr = response.css(
            'div.list-table-content table.list-table tbody.list-body tr.list-row td:first-of-type > a:first-of-type')
        # 输出结果
        print(newrelated_url)
        print(response.text)
        if keyword_arr:
            for rlkw in keyword_arr:
                text = rlkw.extract()
                re_sub = "<[^>]*>"
                text = re.sub(re_sub, '', text)
                print(text)
        sleep(1)
