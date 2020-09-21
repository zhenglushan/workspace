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
#     fulldomain = 'http://www.nvrenx.com/'
#     name = get_name(fulldomain)
#     table_name = "丰胸" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#
#     start_urls = [
#                      "http://www.nvrenx.com/fxzx/list_12_1.html",
#                      "http://www.nvrenx.com/fengxiongkepu/list_32_1.html",
#                      "http://www.nvrenx.com/yigai/list_34_1.html",
#                      "http://www.nvrenx.com/fxwq/list_14_1.html",
#                      "http://www.nvrenx.com/bjhl/list_13_1.html",
#                      "http://www.nvrenx.com/fxmr/list_15_1.html",
#                      "http://www.nvrenx.com/fxsp/list_17_1.html",
#                      "http://www.nvrenx.com/ydfx/list_21_1.html",
#                      "http://www.nvrenx.com/chfx/list_22_1.html",
#                      "http://www.nvrenx.com/amfx/list_20_1.html",
#                      "http://www.nvrenx.com/zhenjiufengxiong/list_36_1.html",
#                      "http://www.nvrenx.com/fengxiongnayi/list_37_1.html",
#                      "http://www.nvrenx.com/zhongyaofengxiong/list_63_1.html",
#                      "http://www.nvrenx.com/fengxiongmiji/list_61_1.html",
#                      "http://www.nvrenx.com/mxfx/list_27_1.html",
#                      "http://www.nvrenx.com/fxal/list_24_1.html",
#                      "http://www.nvrenx.com/gsxd/list_25_1.html",
#                      "http://www.nvrenx.com/zjjd/list_26_1.html",
#                      "http://www.nvrenx.com/fengxiongjingyou/list_40_1.html",
#                      "http://www.nvrenx.com/fengxiongshuang/list_41_1.html",
#                      "http://www.nvrenx.com/koufu/list_42_1.html",
#                      "http://www.nvrenx.com/longxiongchangshi/list_49_1.html",
#                      "http://www.nvrenx.com/zitizhifangfengxiong/30_1.html",
#                      "http://www.nvrenx.com/jiatilongxiong/list_51_1.html",
#                      "http://www.nvrenx.com/zhushelongxiong/list_52_1.html",
#                      "http://www.nvrenx.com/longxiongdeweihai/list_47_1.html",
#                      "http://www.nvrenx.com/rufangfayu/list_56_1.html",
#                      "http://www.nvrenx.com/rufangbaoyang/list_57_1.html",
#                      "http://www.nvrenx.com/rufangjibing/list_58_1.html",
#                      "http://www.nvrenx.com/muruweiyang/list_59_1.html",
#                  ] + [
#                      "http://www.nvrenx.com/fxzx/list_12_%d.html" % p
#                      for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fengxiongkepu/list_32_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/yigai/list_34_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fxwq/list_14_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/bjhl/list_13_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fxmr/list_15_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fxsp/list_17_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/ydfx/list_21_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/chfx/list_22_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/amfx/list_20_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/zhenjiufengxiong/list_36_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fengxiongnayi/list_37_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/zhongyaofengxiong/list_63_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fengxiongmiji/list_61_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/mxfx/list_27_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fxal/list_24_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/gsxd/list_25_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/zjjd/list_26_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fengxiongjingyou/list_40_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/fengxiongshuang/list_41_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/koufu/list_42_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/longxiongchangshi/list_49_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/zitizhifangfengxiong/30_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/jiatilongxiong/list_51_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/zhushelongxiong/list_52_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/longxiongdeweihai/list_47_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/rufangfayu/list_56_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/rufangbaoyang/list_57_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/rufangjibing/list_58_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.nvrenx.com/muruweiyang/list_59_%d.html" % p for p in range(2, 11)
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
#         con_urls = response.css("div.ls-typetwo-right.fl h3.ls-typetwo-title a.a-hover::attr(href)")
#         if con_urls:
#             con_urls = con_urls.extract()
#             for con_url in con_urls:
#                 # http://www.nvrenx.com/longxiongchangshi/2332.html
#                 # http://www.nvrenx.com/fxsp/122.html
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
#         #     qz_reg = "<div class=[\"\']wrap-list-paging mt-20[\"\']>.*?<li class=[\"\']thisclass[\"\']>\d+</li>"
#         #     hz_reg = "<li><a href=[\"\'](.*?)[\"\']>\d+</a></li>"
#         #     full_reg = qz_reg + ".*?" + hz_reg
#         #     result = re.findall(full_reg, response.text, re.S)
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
#             title = response.css("div.arti div.arti-head h1.arti-title::text")
#             if title:
#                 title = title.extract()[0]
#                 title = filter_title(title)
#
#         body = response.meta['body']
#         tbody = response.css("div.arti div.arti-content")
#         if tbody:
#             tbody = tbody.extract()[0]
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
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     import sys
#     import os
#
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'www_nvrenx_com'])
