# # -*- coding:utf-8 -*-
#
#
# import re
# import os
# import scrapy
# from urllib import parse
# from scrapy.http import Request
# from scrapy_mongodb_for_search.settings import IMAGES_STORE
# from scrapy_mongodb_for_search.items import ScrapyuploadimageItem
# from scrapy_mongodb_for_search.tools.commons import *
# from scrapy_mongodb_for_search.tools.domysql import crate_database_table
# from scrapy_mongodb_for_search.tools.do_site_domain import *
# from scrapy_mongodb_for_search.settings import MYSQL_CHARSET, MYSQL_DBNAME_SEARCH, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER
# from scrapy_mongodb_for_search.spiders_requests.search_result._0_search_result_config import keyword_list
# from scrapy_mongodb_for_search.spiders_requests.search_result.baidu.baidu_crawl_contents import BaiduCrawlContents
# from scrapy_mongodb_for_search.spiders_requests.search_result.sogou.sogou_crawl_contents import SogouCrawlContents
# from scrapy_mongodb_for_search.spiders_requests.search_result.qihoo360.qihoo360_crawl_contents import QiHoo360CrawlContents
#
# class ScrapySpider(scrapy.Spider):
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
#         while True:
#             for keyword in keyword_list:
#                 keyword = keyword.strip()
#                 table_name = keyword + '_' + 'contents'
#                 results = self.do_select(table_name,500)
#                 if results:
#                     for result in results:
#                         id = result[0]
#                         word = result[1]
#
#
#                         self.get_and_update(id, word)
#
#
#
#                     print(keyword + " 的所有记录都已经更新完成了。")
#                     keyword_list.remove(keyword)
#             if len(keyword_list) == 0:
#                 break
#
#     def get_and_update(self, id, word):
#         '''
#         包括获取数据和更新数据
#         :param word:
#         :return:
#         '''
#         title_all, body_all = self.get_title_body(word)
#         if title_all and body_all:
#             update_result = self.do_update(id, title_all, body_all)
#             if update_result:
#                 print("表名为 " + self.table_name + " 中 → ID 为 " + str(id) + " 更新成功咯。")
#             else:
#                 print("表名为 " + self.table_name + " 中 → ID 为 " + str(id) + " 更新失败呀！")
#
#     def get_title_body(self, word):
#         title_all, body_all = BaiduCrawlContents().get_title_body(word)
#         if title_all and body_all:
#             print("百度成功采集！")
#         else:
#             title_all, body_all = SogouCrawlContents().get_title_body(word)
#             if title_all and body_all:
#                 print("搜狗成功采集！")
#             else:
#                 title_all, body_all = QiHoo360CrawlContents().get_title_body(word)
#                 if title_all and body_all:
#                     print("奇虎 360 成功采集！")
#
#         return title_all, body_all
#
#     def get_mysql_connection(self):
#         '''
#         获取数据库连接
#         :return:
#         '''
#         conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
#                                db=MYSQL_DBNAME_SEARCH)
#         cursor = conn.cursor()
#         return conn, cursor
#
#     def do_select(self, table_name,num):
#         print("正在读取 " + str(num) + " 个 " + table_name + " 的关键词！")
#         try:
#             conn, cursor = self.get_mysql_connection()
#             # 执行具体的 insert 操作语句
#             select_sql = "SELECT id,word FROM `{0}` WHERE is_crawl=0 LIMIT {1};".format(table_name, num)
#             cursor.execute(select_sql)
#             results = cursor.fetchall()
#         except:
#             return ()  # 如果没有则返回空元祖
#         else:
#             return results
#
#     def do_update(self, id, titles, jianjies):
#         conn, cursor = self.get_mysql_connection()
#         try:
#             if titles and jianjies:
#                 update_sql = "UPDATE `{0}` SET titles=%s, jianjies=%s, is_crawl=1 WHERE id=%s;".format(self.table_name)
#             else:
#                 update_sql = "UPDATE `{0}` SET titles=%s, jianjies=%s, is_crawl=1, is_published=1 WHERE id=%s;".format(
#                     self.table_name)
#             cursor.execute(update_sql, (MySQLdb.escape_string(titles), MySQLdb.escape_string(jianjies), id))
#             conn.commit()
#         except:
#             cursor.close()
#             conn.close()
#             return False
#         else:
#             cursor.close()
#             conn.close()
#             return True
#
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
