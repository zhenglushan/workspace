# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : BaiduRelatedSearches.py
# @DATETime   : 2019/12/12 16:32
# @Author     : 笑看风云

# 抓取百度相关搜索结果关键词

import re, os
from urllib import parse
import requests
from scrapy.http import HtmlResponse
from time import sleep
from ScrapyMongoDBForSearch.工具.通用工具 import generator_file_arr

# headers = {
#     "Host": "www.baidu.com",
#     "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
# }

headers = {
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (compatible;Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'cache-control': 'max-age=0',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


class ZhuTu:
    def __init__(self, keywords, filter_word, save_kw_file_path):
        # 保存关键词的文件
        temp = set()  # 保存相关搜索关键词的集合
        print(save_kw_file_path)
        for keyword in keywords:
            temp.add(keyword)
            is_while = True
            while is_while:
                request_url = 'http://www.baidu.com/s?ie=UTF-8&wd=' + parse.quote(keyword)
                headers.update({'referer': request_url})
                try:
                    resp = requests.get(request_url, headers=headers)
                    resp.encoding = 'UTF-8'
                    response = HtmlResponse(url=request_url, body=resp.text, encoding=resp.encoding)
                    print("当前请求的链接为：" + request_url)
                    if "百度安全验证" in response.text:
                        # sleep(1)  # 暂停 1 秒
                        continue
                    else:
                        is_while = False  # 不再循环 while

                        # 匹配相关搜索的关键词
                        text_arr = response.css('div#rs table a::text')
                        if text_arr:
                            for text in text_arr:
                                text = text.extract().strip()
                                # 过滤关键词
                                for word in filter_word:
                                    if isinstance(word, str):
                                        if word.lower() in text.lower():
                                            temp.add(text)
                                    else:
                                        w0 = word[0]
                                        w1 = word[1]
                                        w2 = word[2]
                                        w3 = word[3]
                                        w4 = word[4]
                                        if (w0 in text) and (w1 in text) and (w2 in text) and (w3 in text) and (
                                                w4 in text):
                                            temp.add(text)

                        # 匹配右侧 'rsv_re_ename':'网站优化','rsv_re_uri' 格式的关键词
                        re_sub = "'rsv_re_ename':'(.*?)','rsv_re_uri'"
                        rsv_res = re.findall(re_sub, response.text, flags=re.I | re.S)
                        if rsv_res:
                            for rsv_re in rsv_res:
                                rsv_re = rsv_re.strip()
                                # 过滤关键词
                                for word in filter_word:
                                    if isinstance(word, str):
                                        if word.lower() in rsv_re.lower():
                                            temp.add(rsv_re)
                                    else:
                                        w0 = word[0]
                                        w1 = word[1]
                                        w2 = word[2]
                                        w3 = word[3]
                                        w4 = word[4]
                                        if (w0 in rsv_re) and (w1 in rsv_re) and (w2 in rsv_re) and (w3 in rsv_re) and (
                                                w4 in rsv_re):
                                            temp.add(rsv_re)

                        # sleep(2)  # 暂停 2 秒
                except Exception as e:
                    sleep(3)
        if len(temp):
            temp_list = list(temp)
            temp_list.sort()
            temp_str = "\n".join(temp_list)
            with open(save_kw_file_path, 'a+', encoding='UTF-8') as savef:
                savef.write(temp_str)


if __name__ == '__main__':
    """
    应该在采集完成之后，再进行过滤
    """
    keyword_dir = "主图_2"  # 要采集的关键词目录名称
    filter_word = [
        '主图',
        # 子列表最多五个元素
        # 如果子列表元素的数量修改了，
        # 则主代码里面的元素个数也需要修改
        ['淘宝', '商品', '图片', '', ''],
        ['淘宝', '产品', '图片', '', ''],
        ['京东', '商品', '图片', '', ''],
        ['京东', '产品', '图片', '', ''],
        ['天猫', '商品', '图片', '', ''],
        ['天猫', '产品', '图片', '', ''],
    ]
    keyword_arr = ["主图", "淘宝主图", "直通车主图", "淘宝直通车主图", "京东主图", "商品主图", "产品主图", "淘宝商品主图", "淘宝产品主图", "商品图片", "产品图片",
                   "淘宝产品图片", "淘宝商品图片", "天猫商品图片", "主图图标"]
    level_number = 10  # 需要循环采集几层

    keyword_path = "D:/WorkSpace/数据采集/百度相关搜索/" + keyword_dir + "/"
    if not os.path.exists(keyword_path):
        os.makedirs(keyword_path)
    for i in range(1, level_number + 1):
        lines = []
        if i == 1:
            lines = keyword_arr
        else:
            file_path = keyword_path + str(i - 1) + '.txt'
            gfr = generator_file_arr(file_path, 20000)
            for keyword_list in gfr:
                for keyword in keyword_list:
                    if keyword in lines:
                        continue
                    else:
                        lines.append(keyword)
        if lines:
            save_kw_file_path = keyword_path + str(i) + '.txt'
            ZhuTu(lines, filter_word, save_kw_file_path)
