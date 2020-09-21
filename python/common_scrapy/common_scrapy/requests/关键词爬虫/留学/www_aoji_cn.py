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
# # 采集速度太慢
# class ScrapySpider(scrapy.Spider):
#     is_test = False  # 设置是否是测试环境,测试时设置为 True 上线时设置为 False
#     fulldomain = 'http://www.aoji.cn/'
#     name = get_name(fulldomain)
#     table_name = "留学" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#     host = get_host(fulldomain)
#
#     headers = {
#         "Host": fulldomain,
#         "User-Agent": baidu_user_agent
#     }
#
#     start_urls = [
#                      "http://www.aoji.cn/news/list/0-0-0-1.html",
#                      "http://www.aoji.cn/blog/list/0-0-0-0-1.html",
#                      "http://www.aoji.cn/news/",
#                  ] + [
#                      "http://www.aoji.cn/news/list/0-0-0-%d.html" % p for p in range(1, 11)
#                  ] + [
#                      "http://www.aoji.cn/blog/list/0-0-0-0-%d.html" % p for p in range(1, 11)
#                  ] + [
#                      "http://www.aoji.cn/news/%d.html" % p for p in range(1, 11)
#                  ]
#
#     user_agent = baidu_user_agent
#     custom_settings = {
#         'LOG_LEVEL': 'ERROR'
#     }
#
#     def __init__(self):
#         crate_database_table(self.table_name)
#
#     def parse(self, response):
#         con_urls = response.css("div.bowen div.bowen_on.xinwens h4 a::attr(href)")
#         if not con_urls:
#             con_urls = response.css("div.nnews_nr ul li a.nnews_nr_list.nnews_nr_list2::attr(href)")
#         if not con_urls:
#             con_urls = response.css("ul.list_4 li a::attr(href)")
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
#                                   meta={'title': '', 'body': '', 'url': con_url, 'pageid': 2},
#                                   callback=self.parse_detail)
#                 else:
#                     print("URL 地址为： " + con_url + " 的网页重复采集了！")
#
#         if not self.is_test:  # 如果是测试环境我们就不抓取下一页了
#             next_page = ''
#             qz_reg = "<div id=[\"\']pages[\"\'] class=[\"\']pager[\"\']>.*?<span>\d+</span>"
#             hz_reg = "<a href=[\"\'](.*?)[\"\']>\d+</a>"
#             full_reg = qz_reg + ".*?" + hz_reg
#             result = re.findall(full_reg, response.text, flags=re.I | re.S)
#             if result:
#                 next_page = result[0]
#                 next_page = next_page.strip()
#                 next_page = parse.urljoin(response.url, next_page)
#             else:
#                 np = response.css('div.page.fl.mr5 a.next_page')
#                 if np:
#                     np = np.extract()[0]
#                     np = np.strip()
#                     next_page = parse.urljoin(response.url, np)
#             if len(next_page) > 0:
#                 print("列表页的下一页地址为： " + next_page)
#                 yield Request(url=next_page, headers=response.headers, callback=self.parse)
#
#     def parse_detail(self, response):
#         url = response.meta['url']
#         title = response.meta['title']
#         body = response.meta['body']
#         pageid = response.meta['pageid']
#
#         if response.status == 200:
#             if len(title) == 0:
#                 title = response.css("div.success-table div.table-title::text")
#                 if not title:
#                     title = response.css("div.sub-list h1::text")
#                 if title:
#                     title = title.extract()[0]
#                     title = filter_title(title)
#
#             tbody = response.css("div.success-table div.cont")
#             if not tbody:
#                 tbody = response.css("div#aoji-article-main.aoji-article-main")
#             if tbody:
#                 tbody = tbody.extract()[0]
#                 tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
#                 tbody = tbody.replace('<p><br/></p>', '')
#                 str_arr = ['<section>', '</section>', '<span>', '</span>']
#                 tbody = more_to_one(str_arr, tbody)
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
#                 # 提取图片 开始
#                 re_sub = "src=[\"\'](.*?)[\"\']"
#                 image_temp = re.findall(re_sub, body, flags=re.I | re.S)
#                 if image_temp:
#                     for image in image_temp:
#                         image_url_sources.append(image)
#                         image = parse.urljoin(url, image)
#                         image_url_fulls.append(image)
#                 # 提取图片 结束
#
#                 item['url'] = url
#                 item['urlhash'] = get_md5(url)
#                 item['image_url_sources'] = image_url_sources
#                 item['image_url_fulls'] = image_url_fulls
#                 item['is_published'] = False
#                 item['has_image'] = False
#                 yield item
#             else:
#                 print("网址: " + url + " 的采集有问题哦！")
#
#     # 已实现内容页分页的代码 ScrapyUploadImage.spiders.美女图片.www_mm131_com.MM131Spider
#     # 分页网址： http://fitness.39.net/jfsp/0812/8/735994.html
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
#     execute(['scrapy', 'crawl', 'www_aoji_cn'])
