# -*- coding:utf-8 -*-


import re
import os
import struct
import requests
from urllib import parse
from urllib.parse import urlparse
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from scrapy.spiders import CrawlSpider, Rule
from scrapy_mongodb_for_search.settings import IMAGES_STORE
from scrapy_mongodb_for_search.items import ScrapyMongodbForSearchItem
from scrapy_mongodb_for_search.my_tools.tools.commons import *
from scrapy_mongodb_for_search.my_tools.tools.domysql import crate_database_table


class AllSpider(CrawlSpider):
    name = 'p0003_xyz'

    is_follow = True  # 是否跟踪页面里面的链接,测试时用 False 上线时用 True

    start_urls = ['http://p0003.xyz/', 'http://p0003.xyz/?m=vod-type-id-5.html']

    rules = [
        Rule(LinkExtractor(allow="m=vod-type-id-\d+.html$"), process_request='process_request', follow=is_follow),
        # Rule(LinkExtractor(allow="m=vod-type-id-\d+-pg-\d+.html$"), process_request='process_request',
        #      follow=is_follow),
        Rule(
            LinkExtractor(allow="m=vod-detail-id-\d+.html$"), process_links='process_links',
            process_request='process_request', callback='parse_html', follow=is_follow),
    ]

    user_agent = 'Mozilla/5.0+(compatible;+Baiduspider/2.0;++http://www.baidu.com/search/spider.html)'

    headers = {
        "Host": 'http://p0003.xyz/',
        "User-Agent": user_agent
    }

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'DEPTH_LIMIT': 10
    }

    def __init__(self, *args, **kwargs):
        '''
        如果没有该函数会出现如下错误:
        AttributeError: 'XXXSpider' object has no attribute '_rules'
        :param args:
        :param kwargs:
        '''
        CrawlSpider.__init__(self, *args, **kwargs)
        # super(P0003XYZSpider,self).__init__(*args, **kwargs)

    def process_links(self, links):
        '''
        https://www.cnblogs.com/3wtoucan/p/6042444.html
        该方法在 crawlspider 中的 _requests_to_follow 方法中被调用，
        它接收一个元素为 Link 的列表作为参数，返回值也是一个元素为 Link 的列表。
        可以用该方法对采集的 Link 对象进行修改，比如修改 Link.url。
        这里的如果你的目标 url 是相对的链接，那么 Scrapy 会将其扩展成绝对的。
        过滤重复网址
        :param link_arr:
        :return: newlink 保存未采集的 Link 集合并返回
        '''
        newlink = []
        for link in links:
            url = link.url
            url_dir_path = IMAGES_STORE + self.name + "/" + get_md5(url) + "/"
            exist = os.path.exists(url_dir_path)  # 去重
            if not exist:
                newlink.append(link)
                os.makedirs(url_dir_path, mode=0o777)  # 创建 URL 对应的文件夹
                print("内容页首页的 URL 地址为： " + url)
            else:
                # links.remove(link)
                print("URL 地址为： " + url + " 的网页重复采集了！")

        return newlink

    def process_request(self, request):
        '''
        修改请求的 Referer 和 User-Agent 的请求头
        :param request:
        :return:
        '''

        # 修改 headers
        request.headers['User-Agent'] = baidu_user_agent
        request.headers['Referer'] = request.url
        return request

    def parse_html(self, response):
        '''

        :param response:
        :return:
        '''
        save_dir = IMAGES_STORE + self.name + "/" + get_md5(response.url) + "/"
        re_sub = '\?m=vod\-play\-id\-\d+\-src\-\d+\-num\-\d+.html'
        url_arr = re.findall(re_sub, response.text, flags=re.I | re.S)
        if url_arr:
            url = url_arr[0]
            url = parse.urljoin(response.url, url)
            print("播放地址为 : " + url)
            yield Request(url=url, headers=response.headers, callback=self.parse_m3u8, meta={'save_dir': save_dir})

    def parse_m3u8(self, response):
        save_dir = response.meta['save_dir']
        re_sub = 'unescape\([^>].*?\);'
        url_arr = re.findall(re_sub, response.text, flags=re.I | re.S)
        if url_arr:
            url = url_arr[0]
            url_list = url.split('https')
            m3u8_url = 'https' + url_list[2]
            m3u8_url = parse.unquote(m3u8_url)
            m3u8_url = m3u8_url.replace("');", '')
            print("m3u8 地址为 : " + m3u8_url)
            host_parse = urlparse(m3u8_url)
            host = host_parse.hostname
            # 构造 headers
            # myheaders = {
            #     'Host': host,
            #     'User-Agent': baidu_user_agent,
            #     'Referer': m3u8_url
            # }
            yield Request(url=m3u8_url, headers=response.headers, callback=self.parse_m3u8_2,
                          meta={'save_dir': save_dir})

    def parse_m3u8_2(self, response):
        save_dir = response.meta['save_dir']
        m3u8_url = response.url
        m3u8_2 = response.text.split('\n')[2]
        if m3u8_2.startswith('/'):
            m3u8_url_2 = parse.urljoin(response.url, m3u8_2)
        else:
            m3u8_url_2 = m3u8_url.replace('index.m3u8', m3u8_2)
        print('m3u8_url_2 地址为 : ' + m3u8_url_2)
        yield Request(url=m3u8_url_2, headers=response.headers, callback=self.parse_m3u8_3, meta={'save_dir': save_dir})

    def parse_m3u8_3(self, response):
        save_dir = response.meta['save_dir']
        host_parse = urlparse(response.url)
        host = host_parse.hostname
        ts_arr = []
        arr_temp = response.text.split('\n')
        for temp in arr_temp:
            if '.ts' in temp:
                ts_arr.append(temp)
        ts_arr.sort()
        for ts in ts_arr:
            full_ts = parse.urljoin(response.url, ts)
            print('抓取 ' + full_ts + ' 的内容')
            myheaders = {
                'Host': host,
                'User-Agent': baidu_user_agent,
                'Referer': full_ts
            }
            yield Request(url=full_ts, headers=myheaders, callback=self.write_ts_file,
                          meta={'ts': full_ts, 'save_dir': save_dir})

    def write_ts_file(self, response):
        save_dir = response.meta['save_dir']
        full_ts = response.meta['ts']
        file_name = full_ts.split('/')[-1]
        file_name = file_name

        try:
            with open(save_dir + file_name, 'ab') as f:
                f.write(response.body)
            print(file_name + " 成功写入文件中！")
        except:
            print(file_name + " 文件写入失败咯！")


def compose_videos():
    '''
    把视频进行合成
    扫描文件夹参考:
    https://blog.csdn.net/wang725/article/details/84844059
    '''
    name = 'p0003_xyz'
    url_dir_path = IMAGES_STORE + name + "/"
    url_dir_path = url_dir_path.replace('/', '\\')
    for tup in os.walk(url_dir_path):
        file_list = tup[2]
        if len(file_list) > 0:
            file_list.sort()
            file_path = tup[0]
            new_file_name = get_md5(file_path)
            # new_file_path = file_path + '/' + new_file_name + '.ts'
            new_file_path = IMAGES_STORE + new_file_name + '.ts'
            try:
                with open(new_file_path, 'ab+') as fw:
                    for file_name in file_list:
                        cont_path = os.path.join(file_path, file_name)
                        with open(cont_path, 'rb') as fr:
                            fw.write(fr.read())
                print(file_path + " 文件合成成功咯！")
            except:
                print(file_path + " 文件合成失败咯！")
    print('文件合成操作结束！')


if __name__ == '__main__':
    from scrapy.cmdline import execute
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'p0003_xyz'])
    compose_videos()
