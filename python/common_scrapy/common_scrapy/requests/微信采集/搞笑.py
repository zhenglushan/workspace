# -*- coding:utf-8 -*-
# @Email	  : 276517382@qq.com
# @FileName   : 搞笑.py
# @DATETime   : 2020/4/20 11:34
# @Author     : 笑看风云

import re, json
import os
import scrapy
from urllib import parse
from scrapy.http import Request
from scrapy_mongodb_for_search.settings import IMAGES_STORE
from scrapy_mongodb_for_search.items import ScrapyMongodbForSearchItem
from scrapy_mongodb_for_search.my_tools.tools.commons import *
from scrapy_mongodb_for_search.my_tools.tools.domysql import crate_database_table
from scrapy_mongodb_for_search.my_tools.tools.do_site_domain import *


class ScrapySpider(scrapy.Spider):
    name = 'weixin_gaoxiao'
    start_urls = [
        "https://weixin.sogou.com/pcindex/pc/pc_1/pc_1.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/1.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/2.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/3.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/4.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/5.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/6.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/7.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/8.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/9.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/10.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/11.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/12.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/13.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/14.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/15.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/16.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/17.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/18.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/19.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/20.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/21.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/22.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/23.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/24.html",
        "https://weixin.sogou.com/pcindex/pc/pc_1/25.html",
    ]

    user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
    headers = {
        "Host": 'mp.weixin.qq.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
    }
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'DOWNLOAD_DELAY': 2,
    }

    all_time_start = "全部采集的开始时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"

    def parse(self, response):
        urls = response.css("div.txt-box h3 a::attr(href)")
        if urls:
            urls = urls.extract()
            for url in urls:
                con_url = url.strip()
                self.headers.update({"Referer": response.url})
                yield Request(url=con_url, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        # print(response.url)
        title = response.css("h2#activity-name.rich_media_title::text")
        if title:
            title = title.extract_first()
            title = title.strip()
            print(title)
        else:
            # print("页面显示不存在了！")
            pass

    def close(spider, reason):
        all_time_end = "全部采集的结束时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
        print(spider.all_time_start)
        print(all_time_end)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'weixin_gaoxiao'])
