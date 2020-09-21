# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 抓取搜索结果.py
# @DATETime   : 2020/5/19 10:17
# @Author     : 笑看风云

import re
from urllib import parse
import requests
import random
from random import choice
from time import sleep
from scrapy.http import HtmlResponse
from common_scrapy.工具.通用.方法库 import replace_domains
from common_scrapy.工具.通用.阿布云代理 import is_use_proxy, abuyun_proxy_requests


class SogouCrawlContents():

    def get_title_body(self, keyword):
        print("使用 搜狗 方式采集…………")
        '''
        采集标题和简介
        :param keyword:
        :return:
        搜索时，每次显示 50 条记录，就不用再分页了
        '''

        # 获取 cookie
        cookie_header = {
            "Host": "www.sogou.com",
            "Referer": "https://www.sogou.com/"
        }

        resp = requests.get("https://www.sogou.com/", headers=cookie_header)
        cookies = resp.cookies
        cookies.set("com_sohu_websearch_ITEM_PER_PAGE", '100')

        title_all = ""
        body_all = ""
        request_url = 'https://www.sogou.com/web?query=' + parse.quote(keyword)
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
            "Host": "www.sogou.com",
            "User-Agent": user_agent
        }
        headers.update({"Referer": request_url})
        # 使用代理
        if is_use_proxy:
            # sleep(0.2)
            try:
                sleep(0.2)
                resp = abuyun_proxy_requests(headers, request_url, cookies=cookies)
                response = HtmlResponse(url=request_url, body=resp.text, encoding='utf8')
            except:
                print('代理有异常哦！')
                response = HtmlResponse(url=request_url, body="", encoding='utf8')
        else:
            resp = requests.get(request_url, headers=headers, cookies=cookies)
            response = HtmlResponse(url=request_url, body=resp.text, encoding='utf8')
        div_arr = response.css('div div.results div')
        for key, div in enumerate(div_arr):
            title = div.css('div h3 a *::text').extract()
            if not title:
                title = div.css('div div h3 a *::text').extract()
            if title:
                title = "".join(title)
                re_sub = "</?[^>]*>"
                title = re.sub(re_sub, '', title, flags=re.S | re.I)
                re_sub = "[ ]+"
                title = re.sub(re_sub, " ", title, flags=re.S | re.I)
                title = title.replace("_", "").replace("-", "").replace("  ", " ").strip()
                title = title.replace('(', '').replace(')', '').replace('【', '').replace('】', ''). \
                    replace('[', '').replace(']', '').replace("﹥", '').replace("=", '')
                title = title.replace('...', '')
                title = replace_domains(title)
                if key == len(div_arr) - 1:
                    title_all = title_all + title
                else:
                    title_all = title_all + title + '[tt]'
            body = ""
            if not body:
                body = div.css('div div.strBox div.str_info_div p.str_info *::text').extract()
            if not body:
                body = div.css('div div.ft *::text').extract()
            if not body:
                body = div.css('div div div.base-clamp *::text').extract()
            if not body:
                body = div.css('div div div.img-text div.text-layout p *::text').extract()
            if body:
                body = "".join(body)
                body = body.replace("[图文]", '')
                re_sub = "</?[^>]*>"
                body = re.sub(re_sub, '', body, flags=re.S | re.I)
                body = body.replace("\r", '').replace("\n", '').replace("\t", '').replace(' ', '').replace(
                    '&nbsp;', '')
                re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日-'
                body = re.sub(re_sub, '', body, flags=re.S | re.I)
                re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日'
                body = re.sub(re_sub, '', body, flags=re.S | re.I)
                # 把 ... 替换为 。 或者 ？ 或者 ！
                body = body.replace('...', choice(['。', '？', '！']))
                re_sub = '\d{1,4}-\d{1,2}-\d{1,2}'
                body = re.sub(re_sub, '', body, flags=re.S | re.I)
                body = body.replace('(', '').replace(')', '').replace('【', '').replace('】', ''). \
                    replace('[', '').replace(']', '').replace("﹥", '').replace("=", '')
                body = replace_domains(body)
                if key == len(div_arr) - 1:
                    body_all = body_all + body
                else:
                    body_all = body_all + body + '[bd]'
        title_all = title_all.rstrip("[tt]")
        body_all = body_all.rstrip("[bd]")
        return title_all, body_all


if __name__ == '__main__':
    crawl = SogouCrawlContents()
    title_all, body_all = crawl.get_title_body("网络营销")
    print(title_all)
    print(body_all)
