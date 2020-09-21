# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 鱼摆摆网_教程.py
# @DATETime   : 2020/4/16 14:58
# @Author     : 笑看风云

import scrapy
import re
from urllib import parse
from scrapy.http import Request
from scrapy_mongodb_for_search.my_tools.common import get_md5, filter_all_html


class www_yubaibai_com_cn_spider(scrapy.Spider):
    name = 'www_yubaibai_com_cn'
    start_urls = ["https://www.yubaibai.com.cn/kaidian/list_3_%d.html" % d for d in range(1, 101)]
    user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
    headers = {
        "Host": 'www.yubaibai.com.cn',
        "User-Agent": user_agent
    }
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'DOWNLOAD_DELAY': 0.1,
    }
    source_dir = "D:/WorkSpace/数据采集/鱼摆摆网/原文/"

    def parse(self, response):
        print("当前抓取的列表页地址为：\t" + response.url)
        con_urls = response.css("div.list ul li span h2 a::attr(href)")
        if con_urls:
            con_urls = con_urls.extract()
            for con_url in con_urls:
                con_url = parse.urljoin(response.url, con_url)
                yield Request(url=con_url, headers=response.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        title_t = response.css("div.listcenter h2::text")
        body_t = response.css("div.cent p")
        if title_t and body_t:
            title = title_t.extract()[0]
            body_arr = body_t.extract()
            body = ""
            for p in body_arr:
                if "<img" not in p:
                    p = filter_all_html(p)  # 由于文章用于翻译，所以需要过滤所有的 HTML 标签
                    p = p.strip()
                    if p:
                        p = p + "\n"
                        body = body + p

            if title and body and len(body) >= 500:
                print("当前抓取的内容页地址为：\t" + response.url)
                file_name = get_md5(response.url) + ".txt"
                file_path = self.source_dir + file_name
                with open(file_path, mode="a+", encoding="UTF-8") as fw:
                    fw.write(response.url + "[ZLSLHX]\n[ZLSLHX]" + title + "[ZLSLHX]\n[ZLSLHX]" + body)


if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'www_yubaibai_com_cn'])
