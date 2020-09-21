# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 刷百度排名.py
# @DATETime   : 2020/5/19 10:26
# @Author     : 笑看风云


import re
import random
import requests
from time import sleep
from scrapy.http import HtmlResponse
from ScrapyMongoDBForSearch.工具.通用工具 import pc_user_agent_arr, m_user_agent_arr

s_word = '厦门SEO'
s_url = 'www.suyyw.com'

request_url = 'http://www.baidu.com/s?wd=' + s_word + '&pn={0}'
headers = {
    'User-Agent': random.choice(pc_user_agent_arr)
}

for pn in range(0, 10):
    req_url = request_url.format(pn * 10)
    resp = requests.get(req_url, {'headers': headers})
    response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
    f13_arr = response.css('div.f13')
    if f13_arr:
        for f13 in f13_arr:
            jump_url = f13.css('a.c-showurl::attr(href)')
            kuaizhao_url = f13.css('a.m::attr(href)')
            if jump_url and kuaizhao_url:
                jump_url = jump_url.extract()[0]
                kuaizhao_url = kuaizhao_url.extract()[0]
                kuaizhao_url_resp = requests.get(kuaizhao_url, {'headers': headers})
                sleep(0.5)
                kuaizhao_url_text = kuaizhao_url_resp.text
                re_sub = '<base href="([^>].*?)">'
                base_url = re.search(re_sub, kuaizhao_url_text, flags=re.I | re.S)
                if base_url:
                    base_url = base_url.group(1)
                    print(base_url)
                    if s_url in base_url:
                        print(base_url)
                        print('----------------------------------------------')
                        print(jump_url)
                        print('----------------------------------------------')
                        print(kuaizhao_url)
                else:
                    print(kuaizhao_url + " 居然没有 base_url 地址！！！")
                    # 有可能是因为点击快照链接的时候，直接跳转到对应网站
            print('**********************************************')
    print("第 " + str(pn + 1) + " 页结束！")
    sleep(0.5)
