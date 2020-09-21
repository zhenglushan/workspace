# -*- coding:utf-8 -*-

import re
from urllib import parse
import requests
from random import choice
from scrapy.http import HtmlResponse
from scrapy_mongodb_for_search.spiders_requests.search_result._step.search_result_tools import raplace_domains
from scrapy_mongodb_for_search.my_tools.tools.proxy.abuyun.requests_proxy import proxy_requests, is_use_proxy


class BaiduCrawlContents():
    def get_title_body(self, keyword):
        print("使用 百度 方式采集…………")
        '''
        采集标题和简介
        :param keyword:
        :return:
        搜索时，每次显示 50 条记录，就不用再分页了
        '''
        title_all = ""
        body_all = ""
        request_url = 'http://www.baidu.com/s?wd=' + parse.quote(
            keyword) + '&pn={0}&rn=50'
        headers = {
            "Host":
                "www.baidu.com",
            "User-Agent":
                "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
        }
        # pn_max = randint(1, 2)
        for pn in range(0, 2):
            # sleep(0.2)
            req_url = request_url.format(pn * 50)
            headers.update({"Referer": req_url})
            # 使用代理
            if is_use_proxy:
                try:
                    resp = proxy_requests(headers, request_url)
                    response = HtmlResponse(url=req_url,
                                            body=resp.text,
                                            encoding='utf8')
                except Exception as e:
                    print('代理有异常哦！')
                    print(e)
                    response = HtmlResponse(url=req_url,
                                            body="",
                                            encoding='utf8')
            else:
                resp = requests.get(req_url, headers=headers)
                response = HtmlResponse(url=req_url,
                                        body=resp.text,
                                        encoding='utf8')

            div_arr = response.css('div#content_left div[srcid]')
            for key, div in enumerate(div_arr):
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
                        title_arr = eve_div.css(
                            'div.result-op.c-container.xpath-log h3.t a')
                    if title_arr:
                        title_arr = title_arr.extract()
                        title = ''.join(title_arr)
                        re_sub = "</?[^>]*>"
                        title = re.sub(re_sub, '', title, flags=re.S | re.I)
                        title = title.split("_")
                        title = title[0].strip().split("-")
                        title = title[0].strip()
                        title = title.replace('(',
                                              '').replace(')', '').replace(
                            '【', '').replace('】', '')
                        title = title.replace('...', '')
                        title = raplace_domains(title)

                    # 处理正文
                    body_arr = eve_div.css(
                        'div.result.c-container div.c-abstract')
                    if not body_arr:
                        body_arr = eve_div.css(
                            'div.result-op.c-container.xpath-log div.c-row')
                    if not body_arr:
                        body_arr = eve_div.css(
                            'div.result-op.c-container.xpath-log table')
                    if body_arr:
                        body_arr = body_arr.extract()
                        body = ''.join(body_arr)
                        re_sub = "</?[^>]*>"
                        body = re.sub(re_sub, '', body, flags=re.S | re.I)
                        body = body.replace("\r", '').replace(
                            "\n",
                            '').replace("\t",
                                        '').replace(' ',
                                                    '').replace('&nbsp;', '')
                        re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日 - '
                        body = re.sub(re_sub, '', body, flags=re.S | re.I)
                        # 把 ... 替换为 。 或者 ？ 或者 ！
                        body = body.replace('...', choice(['。', '？', '！']))
                        re_sub = '\d{1,4}-\d{1,2}-\d{1,2}'
                        body = re.sub(re_sub, '', body, flags=re.S | re.I)
                        body = body.replace('(', '').replace(')', '').replace(
                            '【', '').replace('】', '')
                        body = raplace_domains(body)

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

                    if title:
                        if key == len(div_arr) - 1:
                            title_all = title_all + title
                        else:
                            title_all = title_all + title + '[tt]'
                    if body:
                        if key == len(div_arr) - 1:
                            body_all = body_all + body
                        else:
                            body_all = body_all + body + '[bd]'
        title_all = title_all.rstrip("[tt]")
        body_all = body_all.rstrip("[bd]")
        return title_all, body_all


if __name__ == '__main__':
    crawl = BaiduCrawlContents()
    title, body = crawl.get_title_body("祛皱纹")
    print(title)
    print(body)
