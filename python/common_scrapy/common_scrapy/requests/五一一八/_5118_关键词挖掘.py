# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : longTailKeyword.py
# @DATETime   : 2019/12/13 14:17
# @Author     : 笑看风云

import re
import requests
from urllib import parse
from time import sleep
from scrapy.http import HtmlResponse
from scrapy_mongodb_for_search.spiders._5118_cookie import _5118_cookie

"""
挖掘长尾词
"""
from scrapy_mongodb_for_search.spiders._5118_关键词加密 import GetConvertKeyword

ci_url = "https://ci.5118.com/"

headers = {
    'Host': 'ci.5118.com',
    'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
    # Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
}

cookiestr = _5118_cookie

re_sub = "<[^>]*>"

if __name__ == '__main__':
    word_list = ["网络营销", "网络营销公司", "网络营销课程", "网络营销培训"]
    for word in word_list:
        new_url = ci_url + GetConvertKeyword().reConvertKeyword(word) + "/"
        headers.update({'Cookie': cookiestr})
        resp = requests.get(new_url, headers=headers)
        resp.encoding = 'UTF-8'
        response = HtmlResponse(url=new_url, body=resp.text, encoding=resp.encoding)
        # 打印請求地址
        print(new_url)
        # 匹配出有指数的有多少条
        word_index = response.css('div.search-result em.blue:nth-child(2)')
        word_index = word_index.extract()[0]  # ['<em class="blue">232</em>'] 所以需要取 [0] 操作
        word_index = re.sub(re_sub, '', word_index)
        print("有指数的关键词个数为：{} 个！".format(str(word_index)))
        # 匹配出查询到的长尾关键词
        keyword_arr = response.css('span.hoverToHide')
        # print(resp.text)
        # print(keyword_arr)
        if keyword_arr:
            for rlkw in keyword_arr:
                text = rlkw.extract()
                text = re.sub(re_sub, '', text)
                print(text)
        sleep(1)

        """
        本程序還未處理分頁情況，使用之前需要繼續完善程序：
        https://ci.5118.com/1556d336bf95a5a5/?isPager=true&pageIndex=1&sortfields=&filters=&_=1576152366536
        https://ci.5118.com/1556d336bf95a5a5/?isPager=true&pageIndex=2&sortfields=&filters=&_=1576152366535
        https://ci.5118.com/1556d336bf95a5a5/?isPager=true&pageIndex=3&sortfields=&filters=&_=1576152366534
        """
