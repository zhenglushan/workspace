# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 抓取搜索结果.py
# @DATETime   : 2020/5/19 10:21
# @Author     : 笑看风云


import re
import os
import chardet
import requests
from random import randint
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from scrapy_mongodb_for_search.spiders_requests.search_result._step._0_search_result_config import BAIDU_SEARCH_IMAGE_STORE
from scrapy_mongodb_for_search.my_tools.tools.commons import get_md5, get_image_extension


class TopKeyword():

    def __init__(self):
        self.top_dir = BAIDU_SEARCH_IMAGE_STORE + "SearchHotspots" + "/"

        self.top_urls = [
            'http://top.baidu.com/buzz?b=1&fr=topboards',
            'http://top.baidu.com/buzz?b=341&fr=topboards',
            'http://top.baidu.com/buzz?b=42&fr=topboards',
            'http://top.baidu.com/buzz?b=342&fr=topboards',
            'http://top.baidu.com/buzz?b=344&fr=topboards',
            'http://top.baidu.com/buzz?b=11&fr=topboards'
        ]

        self.top_headers = {
            "Host": "top.baidu.com",
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
        }

        self.www_headers = {
            "Host": "www.baidu.com",
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
        }

        self.image_headers = {
            "Host": "image.baidu.com",
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
        }

        self.normal_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
        }

        self.get_top_words()

    def get_top_words(self):
        '''
        获取百度搜索热点关键词
        判断每个关键词是否存在，
            不存在，则创建文件夹并进入下一步操作
            存在，则进入下一次循环

        :return:
        '''
        for top_url in self.top_urls:
            self.top_headers.update({"Referer": top_url})
            resp = requests.get(top_url, {'headers': self.top_headers})
            resp.encoding = 'gbk'
            cont = resp.text.encode(resp.encoding, 'ignore')
            soup = BeautifulSoup(cont, 'html5lib')
            keywords = soup.select('td.keyword > a.list-title')
            if keywords:
                for word in keywords:
                    word = word.string
                    word = word.strip()
                    if len(word) > 3:  # 长度大于 3 才收集
                        pic_dir = self.top_dir + (word) + '/'
                        exist = os.path.exists(pic_dir)  # 去重
                        if not exist:
                            os.makedirs(pic_dir, mode=0o777)
                            print("当前抓取的关键词为 ： " + word)
                            title_all, body_all = self.get_title_body(word)
                            print(word + " 的 标题 组合串 为： " + title_all)
                            print(word + " 的 简介 组合串 为： " + body_all)
                            image_path_str = self.get_image_urls(word)
                            print(word + " 的 图片 组合串 为： " + image_path_str)
                        else:
                            print(word + " 已经采集过了！！！ ")

    def get_title_body(self, keyword):
        '''
        采集标题和简介
        :param keyword:
        :return:
        '''
        title_all = ""
        body_all = ""
        request_url = 'http://www.baidu.com/s?wd=' + keyword + '&pn={0}'
        pn_max = randint(5, 15)
        for pn in range(0, pn_max):
            req_url = request_url.format(pn * 10)
            self.www_headers.update({"Referer": req_url})
            resp = requests.get(req_url, {'headers': self.www_headers})
            response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
            div_arr = response.css('div#content_left div[srcid]')
            for div in div_arr:
                eve_div = div.css('div.result.c-container')
                if not eve_div:
                    eve_div = div.css('div.result-op.c-container.xpath-log')
                if eve_div:
                    title = ''
                    body = ''
                    # url = ''
                    # 处理标题
                    title_arr = eve_div.css('div.result.c-container h3.t a')
                    if not title_arr:
                        title_arr = eve_div.css('div.result-op.c-container.xpath-log h3.t a')
                    if title_arr:
                        title_arr = title_arr.extract()
                        title = ''.join(title_arr)
                        re_sub = "</?[^>]*>"
                        title = re.sub(re_sub, '', title, flags=re.S | re.I)
                    # 处理正文
                    body_arr = eve_div.css('div.result.c-container div.c-abstract')
                    if not body_arr:
                        body_arr = eve_div.css('div.result-op.c-container.xpath-log div.c-row')
                    if not body_arr:
                        body_arr = eve_div.css('div.result-op.c-container.xpath-log table')
                    if body_arr:
                        body_arr = body_arr.extract()
                        body = ''.join(body_arr)
                        re_sub = "</?[^>]*>"
                        body = re.sub(re_sub, '', body, flags=re.S | re.I)
                        body = body.replace("\r", '').replace("\n", '').replace("\t", '').replace(' ', '').replace(
                            '&nbsp;', '')
                        re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日 - '
                        body = re.sub(re_sub, '', body, flags=re.S | re.I)
                    # # 处理 URL
                    # url_arr = eve_div.css('div.result.c-container h3.t a::attr(href)')
                    # if not url_arr:
                    #     url_arr = eve_div.css('div.result-op.c-container.xpath-log h3.t a::attr(href)')
                    # if url_arr:
                    #     url_arr = url_arr.extract()
                    #     url = ''.join(url_arr)
                    #     re_sub = "</?[^>]*>"
                    #     url = re.sub(re_sub, '', url, flags=re.S | re.I)
                    # print('当前采集的标题为：' + title)
                    # print('当前采集的简介为：' + body)
                    title_all = title_all + title + '[zlslhx]'
                    body_all = body_all + body + '[zlslhx]'
        return title_all, body_all

    def get_image_urls(self, keyword):
        '''
        收集即将下载的 image 的 url 路径集合
        :param keyword:
        :return:
        '''
        image_arr = set()
        request_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn={0}'
        pn_max = randint(1, 1)
        for pn in range(0, pn_max):
            # 每个页面的 objURL 数量为 60 所以要 乘以 60
            req_url = request_url.format(pn * 60)
            self.image_headers.update({"Referer": req_url})
            resp = requests.get(req_url, {'headers': self.image_headers})
            print("正在抓取 " + req_url + " 页面的图片！")
            pic_url = re.findall('"objURL":"(.*?)",', resp.text, flags=re.I | re.S)
            if pic_url:
                for url in pic_url:
                    if len(url) > 0:
                        image_arr.add(url)
        if len(image_arr) > 0:
            print("共需要下载" + str(len(image_arr)) + "张图片！")
            image_path_str = self.download_image(keyword, image_arr)
            return image_path_str
        else:
            return ''

    def download_image(self, keyword, image_arr):
        '''
        下载图片的操作
        :param keyword:
        :param image_arr:
        :return:
        '''
        download_num = 0
        image_path_str = ''

        for image_url in image_arr:
            self.normal_headers.update({"Referer": image_url})
            try:
                pic = requests.get(image_url, headers=self.normal_headers, timeout=7)
                content = pic.content
            except BaseException:
                print('错误 ' + image_url + ' 图片无法下载！')
                continue
            else:
                if len(content) < 1024 * 10:  # 过滤内容长度小于 10K 的图片
                    print('图片 ' + image_url + ' 太小了，放弃下载')
                else:
                    if download_num > 5:
                        break
                    print("当前下载的图片地址为：" + image_url)
                    pic_dir = self.top_dir + (keyword) + '/'
                    pic_sort_path = get_md5(image_url) + get_image_extension(image_url)
                    pic_file_path = pic_dir + pic_sort_path
                    exist = os.path.exists(pic_file_path)  # 去重
                    if not exist:
                        fp = open(pic_file_path, 'wb')
                        fp.write(content)
                        fp.close()
                        image_path_str = image_path_str + (keyword) + '/' + pic_sort_path + '[zlslhx]'
                    download_num = download_num + 1
        return image_path_str


if __name__ == '__main__':
    topKeyword = TopKeyword()

# 采集百度热点搜索关键词
