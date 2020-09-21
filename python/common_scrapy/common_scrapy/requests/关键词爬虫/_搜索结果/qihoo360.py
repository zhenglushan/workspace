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
# from ScrapyUploadImage.tools.do_site_domain import *
#
#
# class ScrapySpider(scrapy.Spider):
#     index = 0
#     fulldomain = 'https://www.baidu.com/'
#     name = "qihoo360_search_result"
#     root_domain = get_root_domain(fulldomain)
#     query_path = "http://www.baidu.com/s?wd={keyword}&pn={pageno}&rn=50"
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#     headers = {
#         "Host": get_host(fulldomain),
#         "User-Agent": user_agent,
#     }
#
#     custom_settings = {
#         'LOG_LEVEL': 'ERROR',
#         'DOWNLOADER_MIDDLEWARES': {
#             'ScrapyUploadImage.middlewares.ABuYunProxyMiddleware': 1,
#         },
#         """ 启用限速设置 """
#         'AUTOTHROTTLE_ENABLED': True,
#         'AUTOTHROTTLE_START_DELAY': '0.2',  # 初始下载延迟
#         'DOWNLOAD_DELAY': '0.2',  # 每次请求间隔时间
#     }
#
#     def start_requests(self):
#         wordfile = open('D:/siru.txt', 'r', encoding='UTF-8')
#         while True:
#             lines = wordfile.readlines(10000)  # 每次读取 10000 行关键词
#             if not lines:
#                 break
#             for line in lines:
#                 line = line.replace('-', '').strip()
#                 if len(line) > 0:
#                     query_path_p_0 = self.query_path.replace("{keyword}", parse.quote(line)).replace("{pageno}", "0")
#                     query_path_p_1 = self.query_path.replace("{keyword}", parse.quote(line)).replace("{pageno}", "1")
#                     headers = self.headers
#                     headers.update({'Referer': query_path_p_0})
#                     yield Request(url=query_path_p_0, meta={'next_page': query_path_p_1, 'keyword': line},
#                                   headers=headers)
#         wordfile.close()
#
#     def parse(self, response):
#         keyword = response.meta['keyword']
#         try:
#             if "百度快照" in response.text:
#                 print(keyword + " 请求长度为：" + str(len(response.text)) + "   第 " + str(self.index) + " 次请求 √√√√√√√√√√")
#             else:
#                 print(keyword + " 第 " + str(self.index) + " 次请求有问题哦 ××××××××××")
#         except Exception as e:
#             print(keyword + " 第 " + str(self.index) + " 次请求有异常哦 ??????????")
#         self.index = self.index + 1
#
#     def parse_detail(self, response):
#         pass
#
#     def close(self, spider, reason):
#         '''
#         爬虫关闭时，清理空文件夹
#         :param spider:
#         :param reason:
#         :return:
#         '''
#         print("开始清理未采集的网址文件夹！")
#         # del_nosave_dir(self.table_name, self.name)
#         print("未采集的网址文件夹清理完成！")
#
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     import sys
#     import os
#
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'qihoo360_search_result'])
