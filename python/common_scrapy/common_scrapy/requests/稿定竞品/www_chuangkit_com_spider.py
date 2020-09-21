# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : chuangkit_com_mb.py
# @DATETime   : 2020/3/3 16:12
# @Author     : 笑看风云
# 创客贴 https://www.chuangkit.com/mb.html

"""
分析代码
打开 https://www.chuangkit.com/mb.html 发现源码是 JS 代码，因此可知道是通过 JS 方式加载的，
找到 XHR 选项卡中的 getMap.do?_dataType=json 发现里面正式加载数据的请求地址
"""

import re
import os
from urllib import parse
import scrapy
from scrapy.http import Request
from scrapy_mongodb_for_search.my_tools.tools.commons import get_md5


class www_chuangkit_com_spider(scrapy.Spider):
    name = "www_chuangkit_com_spider"
    save_dir = "D:/WorkSpace/数据采集/稿定设计竞品/" + name + "/"
    allowed_domains = ['www.chuangkit.com']
    url_temp = "https://www.chuangkit.com/muban/td-id{0}.html"
    spider_header = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
    }
    spider_header.update({"Host": "www.chuangkit.com"})

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'DOWNLOAD_DELAY': 0.1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if (not os.path.exists(self.save_dir)):
            os.makedirs(self.save_dir)

    def make_muban_url(self):
        for i in range(1, 1000000):
            url_source = self.url_temp.format(i)
            yield url_source, i

    def start_requests(self):
        gen_url = self.make_muban_url()
        for url_source, i in gen_url:
            yield Request(url=url_source, headers=self.spider_header)

    def parse(self, response):
        con_texts = response.css("span.template-tags-item a.single-tag::text")
        if con_texts:
            print("当前采集页面:\t" + response.url)
            con_text = con_texts.extract()
            for text in con_text:
                file_name = get_md5(text)
                with open(self.save_dir + file_name + ".txt", 'w') as wk:
                    wk.write(text)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "www_chuangkit_com_spider"])  # 要执行的 spider
