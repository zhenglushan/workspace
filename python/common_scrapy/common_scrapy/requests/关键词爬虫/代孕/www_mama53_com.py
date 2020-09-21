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
#     fulldomain = 'http://www.mama53.com/'
#     name = get_name(fulldomain)
#     table_name = "怀孕" + '_' + name  # 保存数据的表名
#     root_domain = get_root_domain(fulldomain)
#
#     start_urls = [
#                      "http://www.mama53.com/myyp/list_40_1.html",
#                      "http://www.mama53.com/cqch/fenmianshike/list_33_1.html",
#                      "http://www.mama53.com/cqch/fenmianzhunbei/list_32_1.html",
#                      "http://www.mama53.com/cqch/chanhouhuifu/list_35_1.html",
#                      "http://www.mama53.com/cqch/fenmianfangshi/list_31_1.html",
#                      "http://www.mama53.com/cqch/zaochannanchan/list_34_1.html",
#                      "http://www.mama53.com/cqch/chanhoujibing/list_36_1.html",
#                      "http://www.mama53.com/cqch/chanhouzhishi/list_37_1.html",
#                      "http://www.mama53.com/hyzq/yunqizhishi/list_14_1.html",
#                      "http://www.mama53.com/hyzq/yunqibaojian/list_25_1.html",
#                      "http://www.mama53.com/hyzq/jibingfangzhi/list_26_1.html",
#                      "http://www.mama53.com/hyzq/liuchanzhuyi/list_27_1.html",
#                      "http://www.mama53.com/hyzq/yunqiantai/list_29_1.html",
#                      "http://www.mama53.com/hyzq/yunqishipu/list_30_1.html",
#                      "http://www.mama53.com/hyqq/ruhehuaiyun/list_39_1.html",
#                      "http://www.mama53.com/hyqq/yunqianzhunbei/list_4_1.html",
#                      "http://www.mama53.com/hyqq/yunqiyinshi/list_24_1.html",
#                      "http://www.mama53.com/hyqq/huaiyunzhengzhuang/list_13_1.html",
#                      "http://www.mama53.com/hyqq/youshengzhishi/list_21_1.html",
#                      "http://www.mama53.com/hyqq/buyunbuyu/list_23_1.html",
#                      "http://www.mama53.com/hyqq/beiyunjiancha/list_22_1.html",
#                  ] + [
#                      "http://www.mama53.com/myyp/list_40_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/fenmianshike/list_33_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/fenmianzhunbei/list_32_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/chanhouhuifu/list_35_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/fenmianfangshi/list_31_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/zaochannanchan/list_34_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/chanhoujibing/list_36_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/cqch/chanhouzhishi/list_37_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyzq/yunqizhishi/list_14_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyzq/yunqibaojian/list_25_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyzq/jibingfangzhi/list_26_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyzq/liuchanzhuyi/list_27_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyzq/yunqiantai/list_29_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyzq/yunqishipu/list_30_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/ruhehuaiyun/list_39_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/yunqianzhunbei/list_4_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/yunqiyinshi/list_24_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/huaiyunzhengzhuang/list_13_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/youshengzhishi/list_21_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/buyunbuyu/list_23_%d.html" % p for p in range(2, 11)
#                  ] + [
#                      "http://www.mama53.com/hyqq/beiyunjiancha/list_22_%d.html" % p for p in range(2, 11)
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
#         con_urls = response.css("dl.aListDl dd.oh p.aList-title a::attr(href)")
#         if con_urls:
#             con_urls = con_urls.extract()
#             for con_url in con_urls:
#                 # con_url = 'http://www.mama53.com/myyp/042XW52019.html'
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
#         #     qz_reg = "<div class=[\"\']dede_pages[\"\']>.*?<li class=[\"\']thisclass[\"\']>\d+</li>"
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
#             title = response.css("div.artTop h1.artTit::text")
#             if title:
#                 title = title.extract()[0]
#                 title = filter_title(title)
#
#         body = response.meta['body']
#         tbody = response.css("div.artText")
#         if tbody:
#             tbody = tbody.extract()[0]
#             tbody = filter_common_html(tbody)  # 过滤常见的 HTML 标签和属性
#             # 其他过滤
#             re_sub = "<p>本文链接.*"
#             tbody = re.sub(re_sub, "", tbody, flags=re.I | re.S)
#             tbody = tbody.replace('</script>', '')
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
#     execute(['scrapy', 'crawl', 'www_mama53_com'])
