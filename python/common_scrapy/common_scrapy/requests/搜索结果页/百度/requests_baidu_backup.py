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
from ScrapyMongoDBForSearch.tools.proxy.abuyun_backup import proxy_requests, is_use_proxy
from ScrapyMongoDBForSearch.tools.database.MongoDB import get_MongoDB_DataBase
from pymongo import UpdateOne
from ScrapyMongoDBForSearch.spiders_requests.common_part import collection_names

import asyncio
import aiohttp

# 返回 MongoDB 数据库连接
database = get_MongoDB_DataBase()

# 代理配置

# 代理服务器
from ScrapyMongoDBForSearch.settings import proxyMeta


# 必须使用代理才能使用该类
async def get_title_body(coll_name, uid, keyword):
    print("使用 百度 方式采集…………")

    headers = {
        "Host": "www.baidu.com",
        "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
    }
    title_all = ""
    body_all = ""
    print("当前正在抓取的关键词为：" + keyword)
    # 第一次访问
    request_url = 'http://www.baidu.com/s?wd=' + parse.quote(keyword) + '&pn=0&rn=50'
    headers.update({"Referer": request_url})
    try:
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(3)
            async with session.get(url=request_url, headers=headers, timeout=30, proxy=proxyMeta) as response:
                resp = await response.text()
                resp = HtmlResponse(url=request_url, body=resp, encoding='utf8')
                title, body = match_title_body(resp)
                title_all = title_all + title
                body_all = body_all + body
    except Exception as e:
        print('代理有异常哦！' + e.__str__())

    # 第二次访问
    request_url = 'http://www.baidu.com/s?wd=' + parse.quote(keyword) + '&pn=1&rn=50'
    headers.update({"Referer": request_url})
    try:
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(3)
            async with session.get(url=request_url, headers=headers, timeout=30, proxy=proxyMeta) as response:
                resp = await response.text()
                resp = HtmlResponse(url=request_url, body=resp, encoding='utf8')
                title, body = match_title_body(resp)
                title_all = title_all + title
                body_all = body_all + body
    except Exception as e:
        print('代理有异常哦！' + e.__str__())

    if title_all and body_all:
        print("正在把 " + keyword + " 的采集结果保存到数据库中……")
        collcetion = database[coll_name]
        collcetion.update_one({'_id': uid}, {'$set': {'bd_title': title_all, 'bd_body': body_all}}, upsert=True,
                              bypass_document_validation=True)


def match_title_body(response):
    title_all = ""
    body_all = ""
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
    for coll_name in collection_names:
        collcetion = database[coll_name]
        for _ in range(200):
            loop = asyncio.get_event_loop()
            tasks = []
            doc_part = collcetion.aggregate([{'$match': {'bd_title': {'$exists': False}}}, {'$sample': {'size': 5}}])
            update_coll = []
            for doc in doc_part:
                uid = doc['_id']
                keyword = doc['keyword'].strip()
                coroutine = get_title_body(coll_name, uid, keyword)
                tasks.append(asyncio.ensure_future(coroutine))
            loop.run_until_complete(asyncio.wait(tasks))
