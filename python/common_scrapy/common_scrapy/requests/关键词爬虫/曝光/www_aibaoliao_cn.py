# # -*- coding:utf-8 -*-
#
#
# import re
# import os
# import scrapy
# from urllib import parse
# from scrapy.http import Request
# from ScrapyUploadImage.settings import IMAGES_STORE
# from ScrapyUploadImage.items import ScrapyuploadimageItem
# from ScrapyUploadImage.tools.commons import *
# from ScrapyUploadImage.tools.domysql import crate_database_table
# from ScrapyUploadImage.tools.do_site_domain import *
#
#
# class ScrapySpider(scrapy.Spider):
#     is_test = False  # 设置是否是测试环境,测试时设置为 True 上线时设置为 False
#     fulldomain = 'http://www.aibaoliao.cn/'
#     name = get_name(fulldomain)
#     table_name = "曝光" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#
#     list_1 = ["http://www.aibaoliao.cn/index-%d.htm" % pn for pn in range(1, 100)]
#     list_2 = ["http://www.aibaoliao.cn/forum-2-%d.htm?orderby=lastpid" % pn for pn in range(1, 100)]
#     list_3 = ["http://www.aibaoliao.cn/forum-4-%d.htm?orderby=lastpid" % pn for pn in range(1, 100)]
#     start_urls = list_1 + list_2 + list_3
#     # start_urls = list_3
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#     headers = {
#         "Host": fulldomain,
#         "User-Agent": user_agent
#     }
#     custom_settings = {
#         'LOG_LEVEL': 'ERROR'
#     }
#
#     def __init__(self):
#         crate_database_table(self.table_name)
#
#     def parse(self, response):
#         con_urls = response.css("div.media-body div.subject.break-all a::attr(href)")
#         if con_urls:
#             # con_urls = ['http://www.aibaoliao.cn/thread-3190486926.htm',
#             #             'http://www.aibaoliao.cn/thread-3190486929.htm']
#             con_urls = con_urls.extract()
#             for con_url in con_urls:
#                 con_url = parse.urljoin(response.url, con_url)
#                 url_dir_path = IMAGES_STORE + self.name + "/" + get_md5(con_url) + "/"
#                 exist = os.path.exists(url_dir_path)  # 去重
#                 if not exist:
#                     os.makedirs(url_dir_path, mode=0o777)  # 创建 URL 对应的文件夹
#                     print("内容页首页的 URL 地址为： " + con_url)
#                     yield Request(url=con_url, headers=response.headers,
#                                   meta={'title': '', 'body': '', 'url': con_url},
#                                   callback=self.parse_detail)
#                 else:
#                     print("URL 地址为： " + con_url + " 的网页重复采集了！")
#
#     def parse_detail(self, response):
#         url = response.meta['url']
#
#         title = response.meta['title']
#         if len(title) == 0:
#             title = response.css("div.media-body h4.break-all::text")
#             if title:
#                 title = title.extract()[0]
#                 title = filter_title(title)
#
#         body = response.meta['body']
#         tbody = response.css("div.message.break-all")
#         if tbody:
#             tbody = tbody.extract()[0]
#             re_sub = '(<br[^>]*>){2,}'
#             tbody = re.sub(re_sub, "<p>", tbody, flags=re.I | re.S)
#             re_sub = '(<br[^>]*>)+'
#             tbody = re.sub(re_sub, "<p>", tbody, flags=re.I | re.S)
#             tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
#             body = body + tbody
#
#         if title and body:
#             print("已完成对 " + url + " 页面的采集！")
#             title = title.strip()
#             body = body.strip()
#             image_url_sources = []
#             image_url_fulls = []
#             item = ScrapyuploadimageItem()
#             item['headers'] = response.headers
#             item['spider_name'] = self.name
#             item['table_name'] = self.table_name
#             item['user_agent'] = self.user_agent
#             item['title'] = title
#             item['body'] = body
#             item['root_domain'] = self.root_domain
#
#             if len(body) > 0:
#                 re_sub = "src=[\"\'](.*?)[\"\']"
#                 image_temp = re.findall(re_sub, body, flags=re.I | re.S)
#                 if image_temp:
#                     for image in image_temp:
#                         image_url_sources.append(image)
#                         image = parse.urljoin(url, image)
#                         image_url_fulls.append(image)
#
#             item['url'] = url
#             item['urlhash'] = get_md5(url)
#             item['image_url_sources'] = image_url_sources
#             item['image_url_fulls'] = image_url_fulls
#             item['is_published'] = False
#             item['has_image'] = False
#             yield item
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
#     execute(['scrapy', 'crawl', 'www_aibaoliao_cn'])
