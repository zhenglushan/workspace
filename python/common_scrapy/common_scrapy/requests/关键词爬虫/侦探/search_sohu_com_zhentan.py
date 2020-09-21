# -*- coding:utf-8 -*-

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
    name = 'search_sohu_com_zhentan'
    table_name = "侦探" + '_' + name  # 保存数据的表名
    root_domain = 'sohu.com'

    start_urls = [
                     'http://search.sohu.com/search/meta?keyword=私家侦探&terminalType=pc&spm-pre=smpc.csrpage.0.0.15615184009643jp4p2G&SUV=190625141446T0OJ&from=%d&size=10&searchType=news&queryType=outside&queryId=15615184001075Y2K015&pvId=15615184009643jp4p2G&refer=' % (
                             p * 10) for p in range(0, 50)
                 ] + [
                     'http://search.sohu.com/search/meta?keyword=私人侦探&terminalType=pc&spm-pre=smpc.csrpage.0.0.15615184009643jp4p2G&SUV=190625141446T0OJ&from=%d&size=10&searchType=news&queryType=outside&queryId=15615184001075Y2K015&pvId=15615184009643jp4p2G&refer=' % (
                             p * 10) for p in range(0, 50)
                 ]

    user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
    headers = {
        "Host": 'www.sohu.com',
        "User-Agent": user_agent
    }
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'DOWNLOAD_DELAY': 0,
    }

    def __init__(self):
        crate_database_table(self.table_name)

    def parse(self, response):
        pattern = '"url":"(.*?)","pv"'
        urls = re.findall(pattern, response.text, flags=re.I | re.S)
        if urls:
            for url in urls:
                con_url = url.strip()
                con_url = parse.urljoin(response.url, con_url)
                url_dir_path = IMAGES_STORE + self.name + "/" + get_md5(con_url) + "/"
                exist = os.path.exists(url_dir_path)  # 去重
                if not exist:
                    os.makedirs(url_dir_path, mode=0o777)  # 创建 URL 对应的文件夹
                    print("内容页首页的 URL 地址为： " + con_url)
                    yield Request(url=con_url, headers=response.headers,
                                  meta={'title': '', 'body': '', 'url': con_url},
                                  callback=self.parse_detail)
                else:
                    print("URL 地址为： " + con_url + " 的网页重复采集了！")

    def parse_detail(self, response):
        url = response.meta['url']

        title = response.meta['title']
        if len(title) == 0:
            title = response.css("span.title-info-title::text")
        if not title:
            title = response.css("h3.article-title::text")
        if not title:
            title = response.css("div.text-title h1::text")
        if not title:
            title = response.css("h1::text")
        if title:
            title = title.extract()[0]
            title = filter_title(title)

        body = response.meta['body']
        tbody = response.css("article#mp-editor.article")
        if not tbody:
            tbody = response.css("article.article-text")
        if tbody:
            tbody = tbody.extract()[0]
            tbody = tbody.replace('data-src="//', 'src="http://')  # 替换图片的 src 和 http
            tbody = tbody.replace('src="//', 'src="http://')  # 替换图片的 src 和 http
            tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
            tbody = tbody.replace("<span><i></i>返回搜狐，查看更多</span>", "").replace("<html>", ""). \
                replace("</html>", "").replace("<head>", "").replace("</head>", ""). \
                replace("<body>", "").replace("</body>", "")
            p_index = tbody.rindex("<p>")
            tbody = tbody[0:p_index]  # 使用切片方式把责任编辑部分的内容替换为空
            tbody = tbody.replace("返回搜狐，查看更多", "")
            tbody = tbody.replace('</videoinfo></p>', '')
            body = body + tbody

        if title and body:
            print("已完成对 " + url + " 页面的采集！")
            title = title.strip()
            body = body.strip()
            image_url_sources = []
            image_url_fulls = []
            item = ScrapyMongodbForSearchItem()
            item['headers'] = response.headers
            item['spider_name'] = self.name
            item['table_name'] = self.table_name
            item['user_agent'] = self.user_agent
            item['title'] = title
            item['body'] = body
            item['root_domain'] = self.root_domain

            if len(body) > 0:
                re_sub = "src=[\"\'](.*?)[\"\']"
                image_temp = re.findall(re_sub, body, flags=re.I | re.S)
                if image_temp:
                    for image in image_temp:
                        image_url_sources.append(image)
                        image = parse.urljoin(url, image)
                        image_url_fulls.append(image)

            item['url'] = url
            item['urlhash'] = get_md5(url)
            item['image_url_sources'] = image_url_sources
            item['image_url_fulls'] = image_url_fulls
            item['is_published'] = False
            item['has_image'] = False
            yield item

    def close(self, spider, reason):
        '''
        爬虫关闭时，清理空文件夹
        :param spider:
        :param reason:
        :return:
        '''
        print("开始清理未采集的网址文件夹！")
        del_nosave_dir(self.table_name, self.name)
        print("未采集的网址文件夹清理完成！")

if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'search_sohu_com_zhentan'])
