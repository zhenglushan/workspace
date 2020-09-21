# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : chuangkit_com_mb.py
# @DATETime   : 2020/3/3 16:12
# @Author     : 笑看风云

import os
import scrapy
from scrapy.http import Request
from scrapy_mongodb_for_search.my_tools.tools.commons import get_md5


class www_58pic_com_spider(scrapy.Spider):
    name = "www_58pic_com_spider"
    save_dir = "D:/WorkSpace/数据采集/稿定设计竞品/" + name + "/"
    allowed_domains = ['www.58pic.com']
    url_temp = "https://www.58pic.com/newpic/{0}.html"
    spider_header = {
        'User-Agent': 'AdsBot-Google-Mobile (+http://www.google.com/mobile/adsbot.html) Mozilla (iPhone; U; CPU iPhone OS 3 0 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile Safari'
    }
    spider_header.update({"Host": "www.58pic.com"})

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'REDIRECT_ENABLED ': False,
        # 'DOWNLOAD_DELAY': 0.1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if (not os.path.exists(self.save_dir)):
            os.makedirs(self.save_dir)

    def make_muban_url(self):
        for i in range(35720000, 35730000):
            url_source = self.url_temp.format(i)
            yield url_source, i

    def start_requests(self):
        gen_url = self.make_muban_url()
        for url_source, i in gen_url:
            yield Request(url=url_source, headers=self.spider_header)

    def parse(self, response):
        print("当前采集页面:\t" + response.url + "\t" + str(response.status))
        con_texts = response.css("div.clearfix.mainRight-tagBox a::text")
        if con_texts:
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
    execute(["scrapy", "crawl", "www_58pic_com_spider"])  # 要执行的 spider
