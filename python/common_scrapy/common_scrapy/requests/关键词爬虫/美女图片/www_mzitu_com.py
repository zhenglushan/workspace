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
#     fulldomain = 'https://www.mzitu.com/'
#     name = get_name(fulldomain)
#     table_name = "美女图片" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#     host_domain = get_host(fulldomain)
#
#     # 每日更新地址 https://www.mzitu.com/all/
#
#     start_urls = [
#         'https://www.mzitu.com/page/%d/' % pn for pn in range(1, 226)
#     ]
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#     headers = {
#         "Host": host_domain,
#         'Upgrade-Insecure-Requests': '1',
#         "User-Agent": user_agent,
#         # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
#     }
#     custom_settings = {
#         'LOG_LEVEL': 'INFO'
#     }
#
#     def __init__(self):
#         crate_database_table(self.table_name)
#
#     def start_requests(self):
#         '''
#         请求开始的地方，该函数可以处理 start_urls 的值，更方便测试。
#         :return:
#         '''
#         for start_url in self.start_urls:
#             self.headers.update({'Referer': start_url})
#             yield Request(url=start_url, headers=self.headers, callback=self.parse)
#
#     def parse(self, response):
#         print(response.status)
#         con_urls = response.css("ul#pins li span:not(.time) a::attr(href)")
#         if con_urls:
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
#         # if not self.is_test:  # 如果是测试环境我们就不抓取下一页了
#         #     re_sub = "<a href=[\"\'](list_\d+_\d+\.html)[\"\'] class=[\"\']page-en[\"\']>下一页</a>"
#         #     result = re.findall(re_sub, response.text, re.S)
#         #     if result:
#         #         next_page = result[0]
#         #         next_page = parse.urljoin(response.url, next_page)
#         #         print("列表页的下一页地址为： " + next_page)
#         #         yield Request(url=next_page, headers=response.headers, callback=self.parse)
#
#     def parse_detail(self, response):
#         url = response.meta['url']
#
#         title = response.meta['title']
#         if len(title) == 0:
#             title = response.css("h2.main-title::text")
#             if title:
#                 title = title.extract()[0]
#                 title = filter_title(title)
#
#         body = response.meta['body']
#         tbody = response.css("div.main-image p a img")
#         if tbody:
#             tbody = tbody.extract()[0]
#             body = filter_common_html(body)  # 过滤常见的 HTML 标签和属性
#             re_sub = ' alt=[\"\'].*[\"\']'
#             tbody = re.sub(re_sub, '', tbody, flags=re.I | re.S)
#             body = body + tbody
#
#         re_sub = "<a href=[\"\'](" + self.fulldomain + "\d+/\d+)[\"\']><span>下一页&raquo;</span></a>"
#         result = re.findall(re_sub, response.text, flags=re.I | re.S)
#         if result:
#             body = body + '[zlspage]'
#             next_page = result[0]
#             next_page = parse.urljoin(response.url, next_page)
#             print("内容页分页的下一页地址为： " + next_page)
#             yield Request(url=next_page, headers=response.headers,
#                           meta={'title': title, 'body': body, 'url': url},
#                           callback=self.parse_detail)
#         else:
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
#     execute(['scrapy', 'crawl', 'www_mzitu_com'])
