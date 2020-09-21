# -*- coding:utf-8 -*-

import re
from urllib import parse
import requests
import time, random
from time import sleep
from random import choice, shuffle
from scrapy.http import HtmlResponse
from ScrapyMongoDBForSearch.tools.common import raplace_domains, replace_qihoo360, generator_file, returnBaseDir
from ScrapyMongoDBForSearch.tools.proxy.abuyun import proxy_requests, is_use_proxy
from ScrapyMongoDBForSearch.tools.database.MongoDB import get_MongoDB_DataBase
from pymongo import UpdateOne


class SoCrawlContents():

    def get_title_body(self, keyword):
        print("使用 360 方式采集…………")
        '''
        采集标题和简介
        :param keyword:
        :return:
        搜索时，每次显示 50 条记录，就不用再分页了
        '''
        title_all = ""
        body_all = ""
        request_url = 'https://www.so.com/s?q=' + parse.quote(keyword) + '&pn={0}'

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
            "Host": "www.so.com",
            "User-Agent": user_agent
        }

        for pn in range(1, 11):  # 实际使用时，调整为 11
            # sleep(0.2)
            req_url = request_url.format(pn)
            headers.update({"Referer": req_url})
            # 使用代理
            if is_use_proxy:
                try:
                    sleep(0.2)
                    resp = proxy_requests(headers, req_url)
                    response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
                except Exception as e:
                    print('代理有异常哦！')
                    print(e)
                    response = HtmlResponse(url=req_url, body="", encoding='utf8')
            else:
                resp = requests.get(req_url, headers=headers)
                response = HtmlResponse(url=req_url, body=resp.text, encoding='utf8')
            li_arr = response.css('div#main ul.result li.res-list')
            for key, li in enumerate(li_arr):
                title = li.css('li.res-list h3.res-title *::text').extract()
                if title:
                    title = "".join(title)
                    title = replace_qihoo360(title)
                    title = raplace_domains(title)
                    if key == len(li_arr) - 1:
                        title_all = title_all + title
                    else:
                        title_all = title_all + title + '[tt]'

                body = ""
                if not body:
                    body = li.css('li.res-list div.res-rich.res-desc.so-ask span.so-ask-best *::text').extract()
                if not body:
                    body = li.css('li.res-list div.res-rich.so-rich-news.clearfix div.res-comm-con *::text').extract()
                if not body:
                    body = li.css(
                        'li.res-list div.res-rich.so-rich-jingyan.clearfix div.res-comm-con *::text').extract()
                if not body:
                    body = li.css('li.res-list div.res-rich.so-rich-svideo.clearfix div.res-comm-con *::text').extract()
                if not body:
                    body = li.css('li.res-list div.res-rich.so-rich-jingyan.clearfix div *::text').extract()
                if not body:
                    body = li.css('li.res-list p.res-desc *::text').extract()
                if body:
                    body = "".join(body)
                    body = replace_qihoo360(body)
                    body = raplace_domains(body)
                    if key == len(li_arr) - 1:
                        body_all = body_all + body
                    else:
                        body_all = body_all + body + '[bd]'
        title_all = title_all.rstrip("[tt]")
        body_all = body_all.rstrip("[bd]")
        return title_all, body_all


if __name__ == '__main__':

    # 如果 coll_name 为空，则按照数据库集合进行均衡采集
    # 如果 coll_name 不为空，则只按照 coll_name 的集合进行采集
    coll_name = "私家侦探_私人侦探长尾词"
    coll_name_arr = [
        "半永久_半永久长尾词",
        "代运营_代运营长尾词",
        "网赚_网上赚钱长尾词",
        "网赚_网络赚钱长尾词",
        "网赚_网赚长尾词",
        "代孕_代孕长尾词",
        "代孕_代怀孕长尾词",
        "代孕_助孕长尾词",
        "私家侦探_私人侦探长尾词",
        "私家侦探_私家侦探长尾词",
        "壮阳_万艾可长尾词",
        "壮阳_他达拉非长尾词",
        "壮阳_伟哥长尾词",
        "壮阳_壮阳长尾词",
        "壮阳_威尔刚长尾词",
        "壮阳_希爱力长尾词",
        "壮阳_早泄长尾词",
        "壮阳_肾虚长尾词",
        "壮阳_补肾长尾词",
        "壮阳_阳痿长尾词",
        "壮阳药_壮阳药长尾词",
        "伴游_伴游长尾词",
        "伴游_陪游长尾词",
        "婚纱摄影_婚纱摄影长尾词",
        "婚纱摄影_婚纱照长尾词",
        "月子中心_月子中心长尾词",
        "月子中心_月子会所长尾词",
        "私服_私服长尾词",
        "试管婴儿_试管婴儿长尾词",
    ]  # 收集所有要采集的集合名称

    # 公共代码
    crawl = SoCrawlContents()
    database = get_MongoDB_DataBase()

    # 判断 coll_name_arr 是否为空
    # 为空，则增加要采集的集合名称
    # 不为空，则按照 coll_name_arr 里面的集合进行采集
    if not coll_name_arr:
        # 判断 coll_name 是否为空
        if coll_name:
            coll_name_arr = coll_name_arr.append(coll_name)
        else:
            collcetion_list = database.list_collection_names()  # 获取所有集合名称
            for coll_name in collcetion_list:
                coll_name_arr.append(coll_name)
    else:
        shuffle(coll_name_arr)  # 对列表中的元素随机排序

    # 循环每个集合进行数据采集
    for coll_name in coll_name_arr:
        collcetion = database[coll_name]
        # 循环 20 次
        for i in range(20):
            doc_part = collcetion.find({"so_title": {'$exists': False}}).limit(50)  # 每次更新 50 条数据
            update_coll = []
            for doc in doc_part:
                uid = doc['_id']
                keyword = doc['keyword']
                keyword = keyword.strip()
                title, body = crawl.get_title_body(keyword)
                time.sleep(1)  # 间隔 1 秒钟
                # 两个字段都存在才保存
                if title and body:
                    print("集合名称为：" + coll_name + " 当前为第 " + str(i + 1) + " 次循环；当前的 _id 值为： " + str(uid))
                    op = UpdateOne({'_id': uid}, {'$set': {'so_title': title, 'so_body': body}}, upsert=True)
                    update_coll.append(op)
            if update_coll:
                collcetion.bulk_write(update_coll, ordered=False, bypass_document_validation=True)
            time.sleep(10)  # 间隔 10 秒钟
        break  # 只采集其中一个集合
        # MongoDB 随机选择 20 条记录，适合于发布场合使用
        # https://www.jianshu.com/p/24465cdc2dee
        # doc_part = collcetion.aggregate([{'$sample': {'size': 20}}])
        # doc_part = collcetion.find({"title": {'$exists': False}}).skip(40).limit(20)

        # Python3 操作 MongoDB 看这一篇就够了
        # https://www.cnblogs.com/aademeng/articles/9779271.html
