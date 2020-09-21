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
#     fulldomain = 'http://www.zx123.cn/'
#     name = get_name(fulldomain)
#     table_name = "装修" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#     # allowed_domains = [get_host(fulldomain)]
#     start_urls = [
#                      "http://www.zx123.cn/fwzx/",
#                      "http://www.zx123.cn/jjfs/",
#                      "http://www.zx123.cn/zxfg/",
#                      "http://www.zx123.cn/zxgl/",
#                      "http://www.zx123.cn/jjzx/",
#                      "http://www.zx123.cn/zxlc/",
#                  ] + [
#                      'http://www.zx123.cn/fwzx/%d.html' % p for p in range(2, 11)
#                  ] + [
#                      'http://www.zx123.cn/jjfs/%d.html' % p for p in range(2, 11)
#                  ] + [
#                      'http://www.zx123.cn/zxfg/%d.html' % p for p in range(2, 11)
#                  ] + [
#                      'http://www.zx123.cn/zxgl/%d.html' % p for p in range(2, 11)
#                  ] + [
#                      'http://www.zx123.cn/jjzx/%d.html' % p for p in range(2, 11)
#                  ] + [
#                      'http://www.zx123.cn/zxlc/%d.html' % p for p in range(2, 11)
#                  ]
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
#         con_urls = response.css("div.tagstt_item div.atitle h2 a::attr(href)")
#         if not con_urls:
#             con_urls = response.css("div.bkleftlist div.bktitle strong a::attr(href)")
#         if con_urls:
#             con_urls = con_urls.extract()
#             for con_url in con_urls:
#                 # con_url = 'http://www.zx123.cn/2012/0719/50659.html'
#                 con_url = parse.urljoin(response.url, con_url)
#                 url_dir_path = IMAGES_STORE + self.name + "/" + get_md5(con_url) + "/"
#                 exist = os.path.exists(url_dir_path)  # 去重
#                 if not exist:
#                     os.makedirs(url_dir_path, mode=0o777)  # 创建 URL 对应的文件夹
#                     print("内容页首页的 URL 地址为： " + con_url)
#                     yield Request(url=con_url, headers=response.headers,
#                                   meta={'title': '', 'body': '', 'url': con_url, 'pageid': 2},
#                                   callback=self.parse_detail)
#                 else:
#                     print("URL 地址为： " + con_url + " 的网页重复采集了！")
#
#         # if not self.is_test:  # 如果是测试环境我们就不抓取下一页了
#         #     result = response.css('a.hovers + a::attr(href)')
#         #     if result:
#         #         next_page = result.extract()[0]
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
#             if len(title) == 0:
#                 title = response.css("div.text_title h1::text")
#                 if title:
#                     title = title.extract()[0]
#                     title = filter_title(title)
#
#             tbody = response.css("div.text_conter.jinxuanxiang p")
#             if not tbody:
#                 tbody = response.css("div.left div.article p")
#             if tbody:
#                 tbody = tbody.extract()
#                 tbody = ''.join(tbody)
#
#                 tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
#                 tbody = tbody.replace('：<span>zxt100520</span>', '，')
#                 tbody = tbody.replace('装修123网站', '').replace('装修123网', '').replace('装修123', '')
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
#             if len(title) > 0 and len(body) > 0:
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
#     execute(['scrapy', 'crawl', 'www_zx123_cn'])
