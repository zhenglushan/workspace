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
# from ScrapyUploadImage.tools.proxy.abuyun.requests_proxy import proxy_requests
#
#
# def get_cookie():
#     '''
#     参考链接:
#     https://blog.csdn.net/weixin_43116910/article/details/83514670
#     :return:
#     '''
#     user_agent = get_user_agent()
#     # 获取 cookie
#     cookie_header = {
#         "Host": "www.sogou.com",
#         "Referer": "https://www.sogou.com/"
#     }
#     cookie_header.update({'User-Agent': user_agent})
#
#     resp = proxy_requests(cookie_header, "https://www.sogou.com/web?query=" + str(random.randint(1, 100000000)))
#     cookies = resp.cookies
#     # print(cookies._cookies)
#     # SNUID = cookies._cookies['.sogou.com']['/']['SNUID'].value
#     # IPLOC = cookies._cookies['.sogou.com']['/']['IPLOC'].value
#     # SUID = cookies._cookies['.sogou.com']['/']['SUID'].value
#     # ld = cookies._cookies['.sogou.com']['/']['ld'].value
#     _sogou_com_cookie = cookies._cookies['.sogou.com']['/']
#     if 'SNUID' in _sogou_com_cookie:
#         SNUID = _sogou_com_cookie['SNUID'].value
#         SNUID_expires = _sogou_com_cookie['SNUID'].expires
#     else:
#         SNUID = ''
#         SNUID_expires = 0
#     # 把 RequestCookieJar 转换成字典格式并添加新的 Cookie 键值对
#     cookies_dict = requests.utils.dict_from_cookiejar(cookies)
#     cookies_dict['com_sohu_websearch_ITEM_PER_PAGE'] = '100'
#     # print(cookies_dict)
#     return cookies_dict, user_agent, SNUID, SNUID_expires
#
#
# def get_user_agent():
#     '''
#     构造不是爬虫也不是浏览器的 UA
#     '''
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) {0}/{1} {2}/{3}.{4}"
#
#     a_z = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
#            "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
#            "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
#
#     random.shuffle(a_z)
#     rand_a_z_1 = random.sample(a_z, random.randint(3, 10))
#     random.shuffle(a_z)
#     rand_a_z_2 = random.sample(a_z, random.randint(3, 10))
#
#     user_agent = user_agent.format("".join(rand_a_z_1), random.randint(1, 1000000), "".join(rand_a_z_2),
#                                    random.randint(1, 1000000), random.randint(1, 1000000))
#     return user_agent
#
#
# class ScrapySpider(scrapy.Spider):
#     index = 0
#     fulldomain = 'https://www.sogou.com/'
#     name = "sogou_search_result"
#     root_domain = get_root_domain(fulldomain)
#     headers = {
#         "Host": get_host(fulldomain)
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
#             for k, line in enumerate(lines):
#                 line = line.replace('-', '').strip()
#                 if len(line) > 0:
#                     query_path = "https://www.sogou.com/web?query=" + parse.quote(line)
#                     headers = self.headers
#                     headers.update({'Referer': query_path})
#                     try:
#                         SNUID_expires = 0
#                         if not SNUID_expires:
#                             cookies_dict, user_agent, SNUID, SNUID_expires = get_cookie()
#                             cookie = cookies_dict
#                         else:
#                             timestamp = int(time.time())
#                             if timestamp > SNUID_expires:
#                                 cookies_dict, user_agent, SNUID, SNUID_expires = get_cookie()
#                                 if SNUID:
#                                     cookie = cookies_dict
#                         headers.update({'User-Agent': user_agent})
#                         yield Request(url=query_path, meta={'keyword': line}, headers=headers, cookies=cookie)
#                     except:
#                         print("很抱歉，搜狗搜索出现问题了，请略过！！！")
#         wordfile.close()
#
#     def parse(self, response):
#         keyword = response.meta['keyword']
#         try:
#             if "快照</a>" in response.text:
#                 print(keyword + " 请求长度为：" + str(len(response.text)) + "   第 " + str(self.index) + " 次请求 √√√√√√√√√√")
#             else:
#                 print(keyword + " 第 " + str(self.index) + " 次请求有问题哦 ××××××××××")
#                 print("搜狗出现验证码咯！！！请略过！！！")
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
#     execute(['scrapy', 'crawl', 'sogou_search_result'])
