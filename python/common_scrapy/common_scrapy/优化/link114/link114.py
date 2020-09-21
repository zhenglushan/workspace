# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : BaiduRelatedSearches.py
# @DATETime   : 2019/12/12 16:32
# @Author     : 笑看风云

# 查询页面在百度的收录情况

import execjs
from urllib import parse
import requests
from scrapy.http import HtmlResponse
from time import sleep
from ScrapyMongoDBForSearch.工具.通用工具 import generator_file_arr

post_url = "http://www.link114.cn/multi.php"

headers = {
    "Host": "www.link114.cn",
    "Origin": "http://www.link114.cn",
    "Referer": "http://www.link114.cn/",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "cache-control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.16 Safari/537.36",
}

func = ["baidu_kz"]


def cha_shou_lu(urlstr):
    resp = requests.post(url=post_url, data={'func': func[0], 'websites': urlstr}, headers=headers)
    print(resp.text)

    # while is_while:
    #     request_url = 'http://www.baidu.com/s?ie=UTF-8&wd=' + parse.quote(url)
    #     headers.update({'referer': request_url})
    #     try:
    #         resp = requests.get(request_url, headers=headers, verify=False)
    #         resp.encoding = 'UTF-8'
    #         response = HtmlResponse(url=request_url,
    #                                 body=resp.text,
    #                                 encoding=resp.encoding)
    #         print(response.text)
    #         print("当前请求的链接为：" + request_url)
    #         if "百度安全验证" in response.text:
    #             sleep(3)
    #             continue
    #         else:
    #             is_while = False  # 不再循环 while
    #             if "www.baidu.com/link?url=" in response.text:
    #                 return url, '已收录'
    #             else:
    #                 return url, '未收录'
    #     except Exception as e:
    #         sleep(3)


if __name__ == '__main__':
    # url_path = "./article-urls.txt"
    # gfr = generator_file_arr(url_path, 500)
    # for url_list in gfr:
    #     urlstr = "|".join(url_list).replace("https://",'')
    #     cha_shou_lu(urlstr)
    #     sleep(10)
    #     exit()
    func = "baidu_kz"
    websites = "www.gaoding.com/article/3423|www.gaoding.com/article/10275|www.gaoding.com/article/10273|www.gaoding.com/article/10271|www.gaoding.com/article/10269|www.gaoding.com/article/10267|www.gaoding.com/article/10266|www.gaoding.com/article/10264|www.gaoding.com/article/10262|www.gaoding.com/article/10260|www.gaoding.com/article/10232|www.gaoding.com/article/10230|www.gaoding.com/article/10228|www.gaoding.com/article/10055|www.gaoding.com/article/10053|www.gaoding.com/article/10087|www.gaoding.com/article/10084|www.gaoding.com/article/10082|www.gaoding.com/article/10080|www.gaoding.com/article/10079|www.gaoding.com/article/10048|www.gaoding.com/article/10216|www.gaoding.com/article/10213|www.gaoding.com/article/10212|www.gaoding.com/article/10215|www.gaoding.com/article/10169|www.gaoding.com/article/10211|www.gaoding.com/article/10171|www.gaoding.com/article/10170|www.gaoding.com/article/10255"

    with open('./myfunction.js',"r",encoding='UTF-8') as f:
        data_func = f.read()
    ctx = execjs.compile(data_func)
    data =  {'func': func, 'websites': websites}
    ctx = ctx.call('create_result',data)
    print(ctx)

