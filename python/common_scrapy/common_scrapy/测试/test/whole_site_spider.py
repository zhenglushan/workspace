# -*- coding:utf-8 -*-

import re
import sys
import urllib3
import requests
from queue import Queue
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# sys.setrecursionlimit(3000)  # 设置递归调用最大值
# https://www.goosndiy.com/ "[\d]+\.html$"
# https://www.caoyaowu.com/ "\/[\d]+\.html$" "\/[\d]+$"
# http://www.jshy.com "_[\d]+\.html$"

class MyClass():
    web_domain = "http://www.jshy.com"  # 网站域名
    web_host = "www.jshy.com"
    re_rule_arr = [
        "_[\d]+\.html$",  # 匹配以 /12345.html 格式为结尾的链接
        # "\/[\d]+$",  # 匹配以 /12345 格式为结尾的链接
    ]
    page_code = "UTF-8"  # 目标采集站的网站编码
    dict_name = "quban"  # 定义词库目录名称

    all_url_set = set()  # 该队列只增加新的 URL 地址
    alterable_url_set = Queue()  # 该队列动态增加新的地址并减少已访问的地址
    content_url_set = set()  # 内容页 url 的队列

    def __init__(self):
        self.all_url_set.add(self.web_domain)
        self.alterable_url_set.put(self.web_domain)

        self.headers = self.get_baidu_headers()

        self.circulation_url_set()

        self.filter_content_url()
        self.parse_content_url()

    def get_baidu_headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
        }
        return headers

    def circulation_url_set(self):
        '''
        遍历队列里面的 URL 地址
        :return:
        '''
        while not self.alterable_url_set.empty():
            pageurl = self.alterable_url_set.get()
            self.collect_a_href(pageurl)

    def collect_a_href(self, pageurl):
        '''
        采集给定 URL 的页面里面的所有 href 链接地址
        :param pageurl:
        :return:
        '''
        try:
            resp = requests.get(pageurl, self.headers, timeout=30)
            resp.encoding = self.page_code
            html = resp.text
            soup = BeautifulSoup(html, 'html5lib')
            for ak in soup.find_all('a'):
                href = ak['href']
                href = self.completed_http_url(href)
                # 判断 url 是否为空且属于站内链接
                if href and href.startswith(self.web_domain) and '?' not in href:
                    if href not in self.all_url_set:
                        print("把 " + href + " 链接放入集合中")
                        self.all_url_set.add(href)  # 把新链接放到 set 集合
                        self.alterable_url_set.put(href)  # 把新链接放到 queue 队列

        except Exception:
            # 如果有异常则直接返回
            return
        finally:
            print("此时 all_url_set 的大小为 : " + str(len(self.all_url_set)))
            print("此时 alterable_url_set 的大小为 : " + str(self.alterable_url_set.qsize()))

    def filter_content_url(self):
        '''
        过滤出符合采集需求的内容页的 URL 地址
        :return:
        '''
        for re_rule in self.re_rule_arr:
            for url in self.all_url_set:
                result = re.search(re_rule, url, flags=re.I|re.S)
                if result:
                    self.content_url_set.add(url)

    def parse_content_url(self):
        for content_url in self.content_url_set:
            print("当前解析的 URL 地址为: " + content_url)
            pass

    def completed_http_url(self, url):
        '''
        补全 内容页 的 url 的值: 一般 url 有如下三种格式, 需要针对每种格式做出判断

        1、  http://www.baidu.com/guonei/9999.html
        2、  //www.baidu.com/guonei/9999.html → 补上 http
        3、  /guonei/9999.html → 补上当前域名

        :param domain: 当前采集站的域名
        :param url: 内容页 的 url 地址
        :return:
        '''
        full_url = ''

        if url.startswith('http'):
            full_url = url
        elif url.startswith('//'):  # 第二种和第三种情况的顺序不能对换
            if self.web_domain.startswith('https'):
                full_url = 'https:' + url
            else:
                full_url = 'http:' + url
        elif url.startswith('/'):  # 第三种和第二种情况的顺序不能对换
            full_url = self.web_domain + url
        else:
            full_url = ''  # 把 href="javascript:" 之类的链接设置为空字符串

        return full_url


if __name__ == "__main__":
    myClass = MyClass()
