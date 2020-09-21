# -*- coding:utf-8 -*-

import re
import random
from urllib import parse
import requests
import time
from threading import Thread
from random import choice, shuffle
from scrapy.http import HtmlResponse
from ScrapyMongoDBForSearch.tools.common import raplace_domains, pc_user_agent_arr
from ScrapyMongoDBForSearch.tools.database.MongoDB import get_MongoDB_DataBase
from ScrapyMongoDBForSearch.spiders_requests.common_part import collection_names

database = get_MongoDB_DataBase()


class BaiduCrawlContents():
    def sava_mongodb(self, coll_name, uid, keyword):
        title, body = self.get_title_body(keyword)
        if title and body:
            collcetion = database[coll_name]
            collcetion.update_one({'_id': uid}, {'$set': {'bd_title': title, 'bd_body': body}}, upsert=True)
            print("更新：集合名为：" + coll_name + "；关键词为：" + keyword + "；_id 值为： " + str(uid))
        else:
            print("没有采集到数据的关键词为：" + keyword)

    def get_title_body(self, keyword):
        title_all = ""
        body_all = ""
        request_url = 'http://www.baidu.com/s?wd=' + parse.quote(keyword) + '&pn={0}&rn=50'
        headers = {
            "Host": "www.baidu.com",
            # "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
            "User-Agent": random.choice(pc_user_agent_arr)
        }
        # pn_max = randint(1, 2)
        for pn in range(0, 2):
            req_url = request_url.format(pn * 50)
            headers.update({"Referer": req_url})
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
            time.sleep(0.01)
        title_all = title_all.rstrip("[tt]")
        body_all = body_all.rstrip("[bd]")
        return title_all, body_all


if __name__ == '__main__':
    '''
    修改成按照单表多线程查询
    '''
    # 公共代码
    crawl = BaiduCrawlContents()

    # 循环每个集合进行数据采集
    # coll_name = "pos机_pos机长尾词"
    # collcetion = database[coll_name]
    for j in range(100):
        print("……………进入第 " + str(j + 1) + " 次……………大……………循环……………")
        random.shuffle(collection_names)
        for coll_name in collection_names:
            collcetion = database[coll_name]
            for i in range(10):
                print(coll_name + " 进入第 " + str(i + 1) + " 次循环………………………………")
                doc_part = collcetion.aggregate([
                    {'$match': {'bd_title': {'$exists': False}}},
                    {'$sample': {'size': 30}}
                ])
                line_threads = []
                for doc in doc_part:
                    uid = doc['_id']
                    keyword = doc['keyword']
                    keyword = keyword.strip()
                    line_thread = Thread(target=crawl.sava_mongodb, args=(coll_name, uid, keyword))
                    line_threads.append(line_thread)
                for lt in line_threads:
                    lt.start()
                    time.sleep(0.1)
                for lt in line_threads:
                    lt.join()
                    time.sleep(0.1)
                time.sleep(10)
            time.sleep(1)
        time.sleep(10)
