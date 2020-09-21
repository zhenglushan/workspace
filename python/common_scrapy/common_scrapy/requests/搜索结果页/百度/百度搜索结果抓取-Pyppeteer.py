# -*- coding:utf-8 -*-

import re
from urllib import parse
import time
from random import choice
from scrapy.http import HtmlResponse
from scrapy_mongodb_for_search.my_tools.common import raplace_domains
from scrapy_mongodb_for_search.my_tools.database.mongodb import get_MongoDB_DataBase
from scrapy_mongodb_for_search.spiders_requests.common_part import collection_names
from selenium import webdriver

import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

database = get_MongoDB_DataBase()


def sava_mongodb(coll_name, uid, keyword):
    title, body = get_title_body(keyword)
    if title and body:
        collcetion = database[coll_name]
        collcetion.update_one({'_id': uid}, {'$set': {'bd_title': title, 'bd_body': body}}, upsert=True)
        print("更新：集合名为：" + coll_name + "；关键词为：" + keyword + "；_id 值为： " + str(uid))
    else:
        print("没有采集到数据的关键词为：" + keyword)


def get_title_body(keyword):
    title_all = ""
    body_all = ""
    req_url = 'http://www.baidu.com/s?wd=' + parse.quote(keyword) + '&pn=0&rn=50&ie=utf-8'
    asyncio.get_event_loop().run_until_complete(fetch_search(req_url))
    response = HtmlResponse(url=req_url, body="", encoding='utf8')
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


async def fetch_search(req_url):
    browser = await launch(headless=False)
    page = await browser.newPage()
    page_source = await page.goto(req_url)
    await browser.close()
    print(page_source)


def more_thread_caiji(collection_name):
    collcetion = database[collection_name]

    doc_part = collcetion.aggregate([
        {'$match': {'bd_title': {'$exists': False}}},
        {'$sample': {'size': 1}}
    ])

    for doc in doc_part:
        uid = doc['_id']
        keyword = doc['keyword'].strip()
        sava_mongodb(collection_name, uid, keyword)
        time.sleep(1)


if __name__ == '__main__':
    for collection_name in collection_names:
        more_thread_caiji(collection_name)
        break
