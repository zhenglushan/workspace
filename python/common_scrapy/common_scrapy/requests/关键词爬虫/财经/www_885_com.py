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
#     is_test = False  # 设置是否是测试环境,测试时设置为 True 上线时设置为 False
#
#     fulldomain = 'http://www.885.com/'
#     name = get_name(fulldomain)
#     table_name = "财经" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#
#     start_urls = [
#         "http://www.885.com/caijing/gushi/",
#         'http://www.885.com/caijing/yuanyou/',
#         'http://www.885.com/caijing/waihui/',
#         'http://www.885.com/caijing/guijinshu/',
#         'http://www.885.com/caijing/guoji/',
#         'http://www.885.com/caijing/licai/',
#         'http://www.885.com/caijing/xiaofei/',
#         'http://www.885.com/caijing/qiye/',
#         'http://www.885.com/dujia/',
#         'http://www.885.com/xuetang/gprm/',
#         'http://www.885.com/xuetang/cgjq/',
#         'http://www.885.com/xuetang/tzrm/',
#         'http://www.885.com/xuetang/tzjq/',
#         'http://www.885.com/xuetang/gmxd/',
#         # http://www.885.com/wanghongarticle/ 以及如下分页未采集
#         # http://www.885.com/portal/onlinestar/ajax_get_arclist_more?page=2&num=15
#     ]
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#     headers = {
#         "Host": get_host(fulldomain),
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
#             yield Request(url=start, meta={'term_id': 0}, headers=headers)
#
#     def parse(self, response):
#         # 临时变量
#         last_id = 0
#         term_id = response.meta['term_id']
#         con_urls = []
#         con_urls = response.css('div.list-text.shli a.surl.stitle::attr(href)')
#         if not con_urls:
#             pattern = '"id":"(\d+)","term_id":"\d+","post_author"'
#             id_arr = re.findall(pattern, response.text, flags=re.I | re.S)
#             if id_arr:
#                 for id in id_arr:
#                     con_url = "/a/" + str(id) + ".html"
#                     con_urls.append(con_url)
#         else:
#             con_urls = con_urls.extract()
#
#         # 计算 last_id 的值
#         if len(con_urls) > 0:
#             con_urls.sort(reverse=True)
#             last_id = int(con_urls[-1].replace('/a/', '').replace('.html', ''))
#
#         # 计算 term_id 的值
#         if term_id == 0:
#             pattern = 'var term_id = (\d+);'
#             term_id = re.findall(pattern, response.text, flags=re.I | re.S)
#             if term_id:
#                 term_id = term_id[0]
#             else:
#                 print("term_id 不存在")
#
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
#         #     next_page = "http://www.885.com/portal/list/ajax_get_list_more?term_id=" + str(term_id) + "&last_id=" + str(
#         #         last_id) + "&limit=1000"
#         #     print("列表页的下一页地址为： " + next_page)
#         #     yield Request(url=next_page, meta={'term_id': term_id}, headers=response.headers, callback=self.parse)
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
#                 title = response.css("div.usu-con.oh h1::text")
#                 if title:
#                     title = title.extract()[0]
#                     title = filter_title(title)
#
#             tbody = response.css("div.usu-con.oh div.pr.content.mt10")
#
#             if tbody:
#                 tbody = tbody.extract()[0]
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
#     execute(['scrapy', 'crawl', 'www_885_com'])
