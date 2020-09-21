# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : BaiduRelatedSearches.py
# @DATETime   : 2019/12/12 16:32
# @Author     : 笑看风云

# 查询页面在百度的收录情况

from urllib import parse
import requests
from scrapy.http import HtmlResponse
from time import sleep
from ScrapyMongoDBForSearch.工具.通用工具 import generator_file_arr

# headers = {
#     # "Host": "www.baidu.com",
#     "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
# }


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    # 'User-Agent':'Mozilla/5.0 (compatible;Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'cache-control': 'max-age=0',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
# }

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.16 Safari/537.36",
}

def cha_shou_lu(url):
    is_while = True
    while is_while:
        request_url = 'http://www.baidu.com/s?ie=UTF-8&wd=' + parse.quote(url)
        headers.update({'referer': request_url})
        try:
            resp = requests.get(request_url, headers=headers, verify=False)
            resp.encoding = 'UTF-8'
            response = HtmlResponse(url=request_url,
                                    body=resp.text,
                                    encoding=resp.encoding)
            print(response.text)
            print("当前请求的链接为：" + request_url)
            if "百度安全验证" in response.text:
                sleep(3)
                continue
            else:
                is_while = False  # 不再循环 while
                if "www.baidu.com/link?url=" in response.text:
                    return url, '已收录'
                else:
                    return url, '未收录'
        except Exception as e:
            sleep(3)


if __name__ == '__main__':
    url_path = "./article-urls.txt"
    gfr = generator_file_arr(url_path, 10000)
    for url_list in gfr:
        for url in url_list:
            url, result = cha_shou_lu(url)
            print(url + " 查询结果为：" + result)
            sleep(3)
