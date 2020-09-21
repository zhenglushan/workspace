# -*- coding:utf-8 -*-
'''
import sys
import os

    在 VSCode 中运行 Scrapy Django 等项目时，以下三行代码是必须的，
    每个执行文件中都需要增加如下三行代码

pro_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
pro_path = os.path.abspath(os.path.join(pro_path,".."))
sys.path.append(pro_path)
'''
import re
from urllib import parse
import requests
import time
from random import choice, shuffle
from scrapy.http import HtmlResponse
from ScrapyMongoDBForSearch.tools.common import raplace_domains, generator_file, returnBaseDir
from ScrapyMongoDBForSearch.tools.proxy.abuyun import proxy_requests, is_use_proxy
from ScrapyMongoDBForSearch.tools.database.MongoDB import get_MongoDB_DataBase
from pymongo import UpdateOne
from ScrapyMongoDBForSearch.spiders_requests.common_part import collection_names


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
        request_url = 'http://www.baidu.com/s?wd=' + parse.quote(keyword) + '&pn={0}&rn=50'
        headers = {
            "Host": "www.baidu.com",
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
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
                    response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
                except Exception as e:
                    print('代理有异常哦！')
                    print(e)
                    response = HtmlResponse(url=req_url, body="", encoding='utf8')
            else:
                resp = requests.get(req_url, headers=headers)
                response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')

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
                        title_arr = eve_div.css('div.result-op.c-container.xpath-log h3.t a')
                    if title_arr:
                        title_arr = title_arr.extract()
                        title = ''.join(title_arr)
                        re_sub = "</?[^>]*>"
                        title = re.sub(re_sub, '', title, flags=re.S | re.I)
                        title = title.split("_")
                        title = title[0].strip().split("-")
                        title = title[0].strip()
                        title = title.replace('(', '').replace(')', '').replace('【', '').replace('】', '')
                        title = title.replace('...', '')
                        title = raplace_domains(title)

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
                        # 把 ... 替换为 。 或者 ？ 或者 ！
                        body = body.replace('...', choice(['。', '？', '！']))
                        re_sub = '\d{1,4}-\d{1,2}-\d{1,2}'
                        body = re.sub(re_sub, '', body, flags=re.S | re.I)
                        body = body.replace('(', '').replace(')', '').replace('【', '').replace('】', '')
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
    # 公共代码
    crawl = BaiduCrawlContents()
    database = get_MongoDB_DataBase()

    # 循环每个集合进行数据采集
    for coll_name in collection_names:
        collcetion = database[coll_name]
        # 循环 20 次
        for i in range(20):
            # doc_part = collcetion.find({"bd_title": {'$exists': False}}).limit(50)  # 每次更新 50 条数据
            # db.getCollection('代孕_代孕长尾词').aggregate([
            #   {$match: {"bd_title":{$exists: false}}},
            #   {$sample: { size: 10}}
            # ])
            doc_part = collcetion.aggregate([
                {'$match': {'bd_title': {'$exists': False}}},
                {'$sample': {'size': 50}}
            ])  # 每次获取没有 bd_title 中随机 50 条
            update_coll = []
            for doc in doc_part:
                uid = doc['_id']
                keyword = doc['keyword']
                keyword = keyword.strip()
                title, body = crawl.get_title_body(keyword)
                time.sleep(1)  # 间隔 1 秒钟
                # 两个字段都存在才保存
                if title and body:
                    print("集合名为：" + coll_name + " 第 " + str(i + 1) + " 次循环；关键词为：" + keyword + " _id 值为： " + str(uid))
                    op = UpdateOne({'_id': uid}, {'$set': {'bd_title': title, 'bd_body': body}}, upsert=True)
                    update_coll.append(op)
                else:
                    print("没有采集到数据的关键词为：" + keyword)
            if update_coll:
                collcetion.bulk_write(update_coll, ordered=False, bypass_document_validation=True)
            time.sleep(10)  # 间隔 10 秒钟

        # MongoDB 随机选择 20 条记录，适合于发布场合使用
        # https://www.jianshu.com/p/24465cdc2dee
        # doc_part = collcetion.aggregate([{'$sample': {'size': 20}}])
        # doc_part = collcetion.find({"title": {'$exists': False}}).skip(40).limit(20)

        # Python3 操作 MongoDB 看这一篇就够了
        # https://www.cnblogs.com/aademeng/articles/9779271.html
