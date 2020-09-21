# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : BaiduRelatedSearches.py
# @DATETime   : 2019/12/12 16:32
# @Author     : 笑看风云

# 抓取百度相关搜索结果关键词

import re
from urllib import parse
import requests
from scrapy.http import HtmlResponse
from time import sleep
from common_scrapy.工具.通用.方法库 import generator_file_arr

# headers = {
#     "Host": "www.baidu.com",
#     "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
# }

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


class baidu_related_searches:
    def __init__(self, keywords, keyword_dir, file_id):
        save_kw_file_path = './' + keyword_dir + '/' + str(file_id) + '.txt'
        for keyword in keywords:
            request_url = 'https://www.baidu.com/s?wd=' + parse.quote(keyword) + '&pn=0&rn=10'
            resp = requests.get(request_url, headers=headers)
            resp.encoding = 'UTF-8'
            response = HtmlResponse(url=request_url, body=resp.text, encoding=resp.encoding)
            print("当前请求的链接为：" + request_url)
            with open(save_kw_file_path, 'a+', encoding='UTF-8') as savef:
                # 匹配相关搜索的关键词
                text_arr = response.css('div#rs table a::text')
                if text_arr:
                    for text in text_arr:
                        text = text.extract().strip()
                        if text:
                            print("当前正在保存的---相关搜索---关键词为： --->   " + text)
                            savef.write(text + "\n")
                # 匹配 'rsv_re_ename':'网站优化','rsv_re_uri' 格式的关键词
                re_sub = "'rsv_re_ename':'(.*?)','rsv_re_uri'"
                rsv_res = re.findall(re_sub, response.text, flags=re.I | re.S)
                if rsv_res:
                    for rsv_re in rsv_res:
                        rsv_re = rsv_re.strip()
                        if rsv_re:
                            print("当前正在保存的---rsv---关键词为： --->   " + rsv_re)
                            savef.write(rsv_re + "\n")
            sleep(1)


if __name__ == '__main__':
    keyword_dir = '网赚'  # 要采集的关键词目录名称
    level_number = 3  # 需要循环采集几层
    for i in range(1, level_number + 1):
        i_1 = i + 1
        lines = []
        file_path = './' + keyword_dir + '/' + str(i) + '.txt'
        gfr = generator_file_arr(file_path, 20000)
        for keyword_list in gfr:
            for keyword in keyword_list:
                if keyword in lines:
                    continue
                else:
                    lines.append(keyword)
        if lines:
            baidu_related_searches(lines, keyword_dir, i_1)
