# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 抓取搜索结果.py
# @DATETime   : 2020/5/19 10:23
# @Author     : 笑看风云


import re
from urllib import parse
import requests
import random
from random import choice
from time import sleep
from scrapy.http import HtmlResponse
from ScrapyUploadImage.spiders_requests.search_result.search_result_tools import raplace_domains, replace_qihoo360
from ScrapyUploadImage.tools.proxy.abuyun.requests_proxy import proxy_requests, is_use_proxy


class QiHoo360CrawlContents():

    def get_title_body(self, keyword):
        print("使用 360 方式采集…………")
        '''
        采集标题和简介
        :param keyword:
        :return:
        搜索时，每次显示 50 条记录，就不用再分页了
        '''
        title_all = ""
        body_all = ""
        request_url = 'https://www.so.com/s?q=' + parse.quote(keyword) + '&pn={0}'

        '''
        构造不是爬虫也不是浏览器的 UA
        '''

        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) {0}/{1} {2}/{3}.{4}"

        a_z = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
               "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        random.shuffle(a_z)
        rand_a_z_1 = random.sample(a_z, random.randint(3, 10))
        random.shuffle(a_z)
        rand_a_z_2 = random.sample(a_z, random.randint(3, 10))

        user_agent = user_agent.format("".join(rand_a_z_1), random.randint(1, 1000000), "".join(rand_a_z_2),
                                       random.randint(1, 1000000), random.randint(1, 1000000))
        # print(user_agent)

        headers = {
            "Host": "www.so.com",
            "User-Agent": user_agent
        }

        for pn in range(1, 6):  # 实际使用时，调整为 11
            # sleep(0.2)
            req_url = request_url.format(pn)
            headers.update({"Referer": req_url})
            # 使用代理
            if is_use_proxy:
                try:
                    sleep(0.2)
                    resp = proxy_requests(headers, req_url)
                    response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
                except Exception as e:
                    print('代理有异常哦！')
                    print(e)
                    response = HtmlResponse(url=req_url, body="", encoding='utf8')
            else:
                resp = requests.get(req_url, headers=headers)
                response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
            li_arr = response.css('div#main ul.result li.res-list')
            for key, li in enumerate(li_arr):

                title = li.css('li.res-list h3.res-title *::text').extract()
                if title:
                    title = "".join(title)
                    title = replace_qihoo360(title)
                    title = raplace_domains(title)
                    if key == len(li_arr) - 1:
                        title_all = title_all + title
                    else:
                        title_all = title_all + title + '[tt]'

                body = ""
                if not body:
                    body = li.css('li.res-list div.res-rich.res-desc.so-ask span.so-ask-best *::text').extract()
                if not body:
                    body = li.css('li.res-list div.res-rich.so-rich-news.clearfix div.res-comm-con *::text').extract()
                if not body:
                    body = li.css(
                        'li.res-list div.res-rich.so-rich-jingyan.clearfix div.res-comm-con *::text').extract()
                if not body:
                    body = li.css('li.res-list div.res-rich.so-rich-svideo.clearfix div.res-comm-con *::text').extract()
                if not body:
                    body = li.css('li.res-list div.res-rich.so-rich-jingyan.clearfix div *::text').extract()
                if not body:
                    body = li.css('li.res-list p.res-desc *::text').extract()
                if body:
                    body = "".join(body)
                    body = replace_qihoo360(body)
                    body = raplace_domains(body)
                    if key == len(li_arr) - 1:
                        body_all = body_all + body
                    else:
                        body_all = body_all + body + '[bd]'
        title_all = title_all.rstrip("[tt]")
        body_all = body_all.rstrip("[bd]")
        return title_all, body_all


if __name__ == '__main__':
    crawl = QiHoo360CrawlContents()
    title, body = crawl.get_title_body("祛皱纹")
    print(title)
    print(body)
