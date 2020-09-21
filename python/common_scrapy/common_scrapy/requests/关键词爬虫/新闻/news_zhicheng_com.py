# # -*- coding:utf-8 -*-
#
#
# import re
# import os
# import time
# import scrapy
# import requests
# from urllib import parse
# from scrapy.http.cookies import CookieJar
# from scrapy.http import Request
# from ScrapyUploadImage.settings import IMAGES_STORE
# from ScrapyUploadImage.items import ScrapyuploadimageItem
# from ScrapyUploadImage.tools.commons import *
# from ScrapyUploadImage.tools.domysql import crate_database_table
#
#
# class ScrapySpider(scrapy.Spider):
#     name = 'news_zhicheng_com'
#     table_name = "新闻" + '_' + name  # 保存数据的表名
#     root_domain = 'zhicheng.com'
#     start_urls = [
#         "http://www.zhicheng.com/index.php?m=seahot&c=index&a=get_more_list&catid=22&page=%d&pagesize=100" % p for p in
#         range(1, 50)
#     ]
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#     headers = {
#         "Host": 'news.zhicheng.com',
#         "User-Agent": user_agent,
#     }
#
#     custom_settings = {
#         'LOG_LEVEL': 'ERROR',
#         'DOWNLOAD_DELAY': 0,
#         'MEDIA_ALLOW_REDIRECTS': True
#     }
#
#     def __init__(self):
#         crate_database_table(self.table_name)
#
#     def start_requests(self):
#         for start in self.start_urls:
#             headers = self.headers
#             headers.update({'Referer': start})
#             yield Request(url=start, headers=headers)
#
#     def parse(self, response):
#         pattern = '"url":"(\\\\/\\\\/news\.zhicheng\.com\\\\/n\\\\/\d+\\\\/\d+\.html)",'
#         con_urls = re.findall(pattern, response.text, flags=re.I | re.S)
#         if con_urls:
#             for con_url in con_urls:
#                 con_url = con_url.replace("\\", '')
#                 con_url = parse.urljoin(response.url, con_url)
#                 url_dir_path = IMAGES_STORE + self.name + "/" + get_md5(con_url) + "/"
#                 exist = os.path.exists(url_dir_path)  # 去重
#                 if not exist:
#                     os.makedirs(url_dir_path, mode=0o777)  # 创建 URL 对应的文件夹
#                     # con_url = 'http://news.zhicheng.com/n/20170217/123875.html'
#                     print("内容页首页的 URL 地址为： " + con_url)
#                     yield Request(url=con_url, headers=response.headers,
#                                   meta={'title': '', 'body': '', 'url': con_url, 'pageid': 2},
#                                   callback=self.parse_detail)
#                 else:
#                     print("URL 地址为： " + con_url + " 的网页重复采集了！")
#
#         # if not self.is_test:  # 如果是测试环境我们就不抓取下一页了
#         #     next_page = response.css("div.pg a.nxt::attr(href)")
#         #     if next_page:
#         #         next_page = next_page.extract()[0]
#         #         next_page = parse.urljoin(response.url, next_page)
#         #         print("列表页的下一页地址为： " + next_page)
#         #         yield Request(url=next_page, headers=response.headers, callback=self.parse)
#
#     def parse_detail(self, response):
#         url = response.meta['url']
#         title = response.meta['title']
#         body = response.meta['body']
#         pageid = response.meta['pageid']
#
#         if response.status == 200:
#
#             if len(title) == 0:
#                 title = response.css("div.ship_wrap h2::text")
#                 if title:
#                     title = title.extract()[0]
#                     title = filter_title(title)
#
#             tbody = response.css("div.wen_article")
#
#             if tbody:
#                 tbody = tbody.extract()[0]
#                 re_sub = ".*日讯</span></span>"
#                 tbody = re.sub(re_sub, "", tbody, flags=re.I | re.S)
#                 re_sub = '<div class="sf_1">.*'
#                 tbody = re.sub(re_sub, "", tbody, flags=re.I | re.S)
#                 tbody = tbody.replace('src="//', 'src="http://')  # 替换图片的 src 和 http
#                 tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
#                 body = body + tbody
#
#                 # 正文存在，才需要继续下一页
#                 next_page = produce_paging_url(url, pageid)
#                 if len(next_page) > 0:
#                     next_page = parse.urljoin(response.url, next_page)
#                     print("内容页分页的下一页地址为： " + next_page)
#                     pageid = pageid + 1
#                     yield Request(url=next_page, headers=response.headers,
#                                   meta={'title': title, 'body': body, 'url': url, 'pageid': pageid},
#                                   callback=self.parse_detail)
#         else:
#             print("内容页的分页结束了！！！")
#
#             if title and body:
#                 print("已完成对 " + url + " 页面的采集！")
#                 title = title.strip()
#                 body = body.strip()
#                 image_url_sources = []
#                 image_url_fulls = []
#                 item = ScrapyuploadimageItem()
#                 item['headers'] = response.headers
#                 item['spider_name'] = self.name
#                 item['table_name'] = self.table_name
#                 item['user_agent'] = self.user_agent
#                 item['title'] = title
#                 item['body'] = body
#                 item['root_domain'] = self.root_domain
#
#                 if len(body) > 0:
#                     re_sub = "src=[\"\'](.*?)[\"\']"
#                     image_temp = re.findall(re_sub, body, flags=re.I | re.S)
#                     if image_temp:
#                         for image in image_temp:
#                             image_url_sources.append(image)
#                             image = parse.urljoin(url, image)
#                             image_url_fulls.append(image)
#
#                 item['url'] = url
#                 item['urlhash'] = get_md5(url)
#                 item['image_url_sources'] = image_url_sources
#                 item['image_url_fulls'] = image_url_fulls
#                 item['is_published'] = False
#                 item['has_image'] = False
#                 yield item
#                 # print(item)
#
#     def close(self, spider, reason):
#         '''
#         爬虫关闭时，清理空文件夹
#         :param spider:
#         :param reason:
#         :return:
#         '''
#         print("开始清理未采集的网址文件夹！")
#         del_nosave_dir(self.table_name, self.name)
#         print("未采集的网址文件夹清理完成！")
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     import sys
#     import os
#
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'news_zhicheng_com'])
