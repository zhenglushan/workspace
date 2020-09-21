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
# from ScrapyUploadImage.items import ScrapyuploadimageItem
# from ScrapyUploadImage.tools.commons import *
# from ScrapyUploadImage.tools.domysql import crate_database_table
# from ScrapyUploadImage.tools.do_site_domain import *
#
#
# class AllSpider(CrawlSpider):
#     is_follow = True  # 是否跟踪页面里面的链接,测试时用 False 上线时用 True
#     fulldomain = 'http://www.30quban.com/'
#     name = get_name(fulldomain)
#     table_name = "祛斑" + '_' + name  # 保存数据的表名
#     host = get_host(fulldomain)
#     root_domain = get_root_domain(fulldomain)
#
#     start_urls = [
#         'http://www.30quban.com/',
#         "http://www.30quban.com/wenzhang/",
#     ]
#
#     rules = [
#         Rule(
#             LinkExtractor(allow=("/[a-z]+/$", "/list-\d+.html$", "/wenzhang/?paged=\d+")),
#             process_request='process_request', follow=is_follow),
#
#         Rule(
#             LinkExtractor(allow=("www.30quban.com.*/\d+.html$", "www.30quban.com.*/?p=\d+$")),
#             process_links='process_links',
#             process_request='process_request',
#             callback='parse_detail', follow=is_follow),
#     ]
#     # 参考 https://blog.csdn.net/lingfeng5/article/details/80614567
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#
#     headers = {
#         "Host": host,
#         "User-Agent": user_agent
#     }
#
#     custom_settings = {
#         'LOG_LEVEL': 'ERROR'
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
#         crate_database_table(self.table_name)
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
#
#         # 修改 meta
#         request.meta['c_title'] = ''
#         request.meta['c_body'] = ''
#         request.meta['c_url'] = request.url
#         request.meta['pageid'] = 2
#
#         return request
#
#     def parse_detail(self, response):
#         url = response.meta['c_url']
#         title = response.meta['c_title']
#         body = response.meta['c_body']
#         pageid = response.meta['pageid']
#
#         if len(title) == 0:
#             title = response.css("div.wrapper h1 a::text")
#             if not title:
#                 title = response.css("header.entry-header h1.entry-title::text")
#             if title:
#                 title = title.extract()[0]
#                 title = filter_title(title)
#
#         teamp_body = response.css("div.wrapper div.detail-panel")
#         if not teamp_body:
#             teamp_body = response.css("div.entry-content")
#         if teamp_body:
#             teamp_body = teamp_body.extract()
#             teamp_body = "".join(teamp_body)
#
#         if teamp_body:
#             re_sub = "<p>本文链接.*"
#             teamp_body = re.sub(re_sub, "", teamp_body, flags=re.I | re.S)
#             re_sub = "<span[^>]*>"
#             teamp_body = re.sub(re_sub, "", teamp_body, flags=re.I | re.S)
#             teamp_body = teamp_body.replace('</span>', '')
#
#             teamp_body = filter_common_html(teamp_body)  # 过滤常见的 HTML 标签和属性
#
#             body = body + teamp_body
#
#         if len(title) > 0 and len(body) > 0:
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
#         else:
#             print("网址: " + url + " 的采集有问题哦！")
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
#     execute(['scrapy', 'crawl', 'www_30quban_com'])
