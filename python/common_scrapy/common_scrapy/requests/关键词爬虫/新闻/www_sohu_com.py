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
#     fulldomain = 'http://www.sohu.com/'
#     name = get_name(fulldomain)
#     table_name = "新闻" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#     start_urls = [
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=10&page=1&size=50",  # CHANNEL
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=18&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=17&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=29&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=25&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=23&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=44&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=41&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=45&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=42&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=27&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=12&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=28&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=13&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=26&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=994&page=1&size=50",  # CATEGORY
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=998&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1461&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=911&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=934&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=882&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=913&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=881&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=880&page=1&size=50",
#         "http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=936&page=1&size=50",
#         # "http://v2.sohu.com/public-api/feed?scene=TAG&sceneId=67245&page=1&size=50",  # TAG
#         # "http://v2.sohu.com/integration-api/mix/region/139?size=50&adapter=pc&secureScore=50&page=1",  # region
#         # "http://v2.sohu.com/integration-api/mix/region/131?size=50&adapter=pc&secureScore=50&page=1",
#         # "http://v2.sohu.com/integration-api/mix/region/6167?size=50&adapter=pc&secureScore=50&page=1",
#         # "http://v2.sohu.com/integration-api/mix/region/82?size=50&adapter=pc&secureScore=50&page=1"
#     ]
#
#     user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'
#     headers = {
#         "Host": fulldomain,
#         "User-Agent": user_agent
#     }
#     custom_settings = {
#         'LOG_LEVEL': 'ERROR',
#         'DOWNLOAD_DELAY': 0,
#     }
#
#     def __init__(self):
#         crate_database_table(self.table_name)
#
#     def parse(self, response):
#         pattern = '"id":(\d+),"authorId":(\d+),"authorName"'
#         id_aid_arr = re.findall(pattern, response.text, flags=re.I | re.S)
#         if not id_aid_arr:
#             pattern = '"url":"//www.sohu.com/a/(\d+)_(\d+)?'
#             id_aid_arr = re.findall(pattern, response.text, flags=re.I | re.S)
#         if id_aid_arr:
#             for id_aid in id_aid_arr:
#                 con_url = "http://www.sohu.com/a/" + id_aid[0] + "_" + id_aid[1]
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
#         # if not self.is_test:  # 如果是测试环境我们就不抓取下一页了
#         #     next_page = response.css("div.pg a.nxt::attr(href)")
#         #     if next_page:
#         #         next_page = next_page.extract()[0]
#         #         next_page = parse.urljoin(response.url, next_page)
#         #         print("列表页的下一页地址为： " + next_page)
#         #         yield Request(url=next_page, headers=response.headers, callback=self.parse)
#
#     def parse_detail(self, response):
#         url = response.meta['url']
#
#         title = response.meta['title']
#         if len(title) == 0:
#             title = response.css("span.title-info-title::text")
#         if not title:
#             title = response.css("h3.article-title::text")
#         if not title:
#             title = response.css("div.text-title h1::text")
#         if not title:
#             title = response.css("h1::text")
#         if title:
#             title = title.extract()[0]
#             title = filter_title(title)
#
#         body = response.meta['body']
#         tbody = response.css("article#mp-editor.article")
#         if not tbody:
#             tbody = response.css("article.article-text")
#         if tbody:
#             tbody = tbody.extract()[0]
#             tbody = tbody.replace('data-src="//', 'src="http://')  # 替换图片的 src 和 http
#             tbody = tbody.replace('src="//', 'src="http://')  # 替换图片的 src 和 http
#             tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
#             tbody = tbody.replace("<span><i></i>返回搜狐，查看更多</span>", "").replace("<html>", ""). \
#                 replace("</html>", "").replace("<head>", "").replace("</head>", ""). \
#                 replace("<body>", "").replace("</body>", "")
#             p_index = tbody.rindex("<p>")
#             tbody = tbody[0:p_index]  # 使用切片方式把责任编辑部分的内容替换为空
#             tbody = tbody.replace("返回搜狐，查看更多", "")
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
#     execute(['scrapy', 'crawl', 'www_sohu_com'])
