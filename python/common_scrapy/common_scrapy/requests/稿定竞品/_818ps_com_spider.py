# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : _818ps_com_muban.py
# @DATETime   : 2020/3/3 16:12
# @Author     : 笑看风云
# 图怪兽 https://818ps.com/muban/{0}.html

import re
import os
import scrapy
from scrapy.http import Request
from scrapy_mongodb_for_search.my_tools.tools.commons import get_md5


class _818ps_com_spider(scrapy.Spider):
    name = "_818ps_com_spider"
    save_dir = "D:/WorkSpace/数据采集/稿定设计竞品/" + name + "/"
    allowed_domains = ['818ps.com']
    start_urls = ['http://818ps.com/']
    url_temp = "https://818ps.com/pic/{0}.html"
    spider_header = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
    }
    spider_header.update({"Host": "818ps.com"})
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'DOWNLOAD_DELAY': 0,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if (not os.path.exists(self.save_dir)):
            os.makedirs(self.save_dir)

    def make_muban_url(self):
        for i in range(1, 10000000):
            url_source = self.url_temp.format(i)
            yield url_source, i

    def start_requests(self):
        gen_url = self.make_muban_url()
        for url_source, i in gen_url:
            yield Request(url=url_source, headers=self.spider_header)

    def parse(self, response):
        print("当前采集页面:\t" + response.url + "\t" + str(response.status))

        con_texts = response.css("div.keywords-list ul li a::text")
        if con_texts:
            con_text = con_texts.extract()
            for text in con_text:
                text = text.strip()
                file_name = get_md5(text)
                with open(self.save_dir + file_name + ".txt", 'w') as wk:
                    wk.write(text)

        con_texts = response.css("p.intro a::text")
        if con_texts:
            con_text = con_texts.extract()
            for text in con_text:
                text = text.strip()
                file_name = get_md5(text)
                with open(self.save_dir + file_name + ".txt", 'w') as wk:
                    wk.write(text)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "_818ps_com_spider"])  # 要执行的 spider
