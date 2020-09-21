# # -*- coding:utf-8 -*-
#
#
# import re
# import os
# from urllib import parse
# from scrapy.http import Request
# from scrapy.linkextractors import LinkExtractor
# from scrapy.link import Link
# from scrapy.spiders import CrawlSpider, Rule
# from ScrapyUploadImage.settings import IMAGES_STORE
# from ScrapyUploadImage.tools.commons import *
# from ScrapyUploadImage.tools.do_site_domain import *
#
#
# class AllSpider(CrawlSpider):
#     is_follow = True  # 是否跟踪页面里面的链接,测试时用 False 上线时用 True
#     fulldomain = 'https://818ps.com/'
#     name = get_name(fulldomain)
#     table_name = "竞品" + '_' + name  # 保存数据的表名
#     host = get_host(fulldomain)
#     root_domain = get_root_domain(fulldomain)
#
#     start_urls = [
#         fulldomain
#     ]
#
#     rules = [
#         Rule(
#             LinkExtractor(
#                 allow=("/detail/[0-9]+.html")),
#             process_links='process_links',
#             process_request='process_request',
#             callback='parse_detail',
#             follow=is_follow),
#         Rule(
#             LinkExtractor(
#                 allow=("/color/search", "/search.html$", "/search/[0-9a-zA-Z_\-]+.html$",
#                        "/muban/[0-9a-zA-Z_\-]+.html$", "/search/[0-9a-zA-Z_\-]+/[0-9]+.html$",
#                        "/muban/[0-9a-zA-Z_\-]+/[0-9]+.html$")),
#             process_request='process_request',
#             follow=is_follow),
#     ]
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#
#     headers = {
#         "Host": host,
#         "User-Agent": user_agent
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
#     def __init__(self, *args, **kwargs):
#         '''
#         如果没有该函数会出现如下错误:
#         AttributeError: 'CqhwqdcSpider' object has no attribute '_rules'
#         :param args:
#         :param kwargs:
#         '''
#         CrawlSpider.__init__(self, *args, **kwargs)
#         # super(CqhwqdcSpider,self).__init__(*args, **kwargs)
#         # crate_database_table(self.table_name)
#
#     def process_links(self, links):
#         '''
#         https://www.cnblogs.com/3wtoucan/p/6042444.html
#         该方法在 crawlspider 中的 _requests_to_follow 方法中被调用，
#         它接收一个元素为 Link 的列表作为参数，返回值也是一个元素为 Link 的列表。
#         可以用该方法对采集的 Link 对象进行修改，比如修改 Link.url。
#         这里的如果你的目标 url 是相对的链接，那么 Scrapy 会将其扩展成绝对的。
#         过滤重复网址
#         :param link_arr:
#         :return:
#         '''
#         new_links = []
#         for link in links:
#             url = link.url
#             url_dir_path = IMAGES_STORE + self.name + "/" + get_md5(url) + "/"
#             exist = os.path.exists(url_dir_path)  # 去重
#             if not exist:
#                 os.makedirs(url_dir_path, mode=0o777)  # 创建 URL 对应的文件夹
#                 print("内容页首页的 URL 地址为： " + url)
#                 new_links.append(link)
#             else:
#                 links.remove(link)
#                 print("URL 地址为： " + url + " 的网页重复采集了！")
#         return new_links
#
#     def process_request(self, request):
#         '''
#         修改请求的 Referer 和 User-Agent 的请求头
#         :param request:
#         :return:
#         '''
#         # 修改 headers
#         request.headers['User-Agent'] = baidu_user_agent
#         request.headers['Referer'] = request.url
#         print("正在爬行的页面地址为：" + request.url)
#         return request
#
#     def parse_detail(self, response):
#         print("当前采集的页面为：" + response.url)
#         keywords = []
#         keyword_path = IMAGES_STORE + self.name + "/" + get_md5(response.url) + "/" + "keywords.txt"
#         keywords_1 = response.css("div.keywords-list ul li a::text")
#         keywords_2 = response.css("p.intro a::text")
#
#         if keywords_1:
#             keywords_1 = keywords_1.extract()
#             keywords = keywords + keywords_1
#
#         if keywords_2:
#             keywords_2 = keywords_2.extract()
#             keywords = keywords + keywords_2
#
#         if keywords:
#             keywords = "\n".join(keywords)
#             keywords = response.url + "\n" + keywords
#             with open(keyword_path, 'w') as kf:
#                 kf.write(keywords)
#
#     def close(self, spider, reason):
#         '''
#         爬虫关闭时，清理空文件夹
#         :param spider:
#         :param reason:
#         :return:
#         '''
#         # print("开始清理未采集的网址文件夹！")
#         # del_nosave_dir(self.table_name, self.name)
#         # print("未采集的网址文件夹清理完成！")
#         print("采集完成了！！！")
#
#
# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#     import sys
#     import os
#
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', '818ps_com'])
