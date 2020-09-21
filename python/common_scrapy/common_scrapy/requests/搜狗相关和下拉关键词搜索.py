# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 搜狗相关关键词搜索.py
# @DATETime   : 2020/4/8 10:50
# @Author     : 笑看风云

import requests
from urllib import parse
from scrapy.http import HtmlResponse

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


def total_fun(keyword):
    """
    在这里调用所有关键词方法
    :param keyword: 待搜索的关键词
    :return:
    """
    keyword = keyword.strip()
    keyword_arr = []
    keyword_arr = related_search(keyword, keyword_arr)
    keyword_arr = suggest_search(keyword, keyword_arr)
    return keyword_arr


def related_search(keyword, keyword_arr):
    """
    相关搜索
    :param keyword: 待搜索的关键词
    :return:
    """
    rel_url = "https://www.sogou.com/web?query={}&page=1&ie=utf8".format(parse.quote(keyword))
    resp = requests.get(rel_url, headers=headers)
    resp.encoding = 'UTF-8'
    response = HtmlResponse(url=rel_url, body=resp.text, encoding=resp.encoding)
    text_arr = response.css('div.top-hintBox#stable_uphint div.r-sech p a::text')  # 相关推荐
    if text_arr:
        for text in text_arr:
            text = text.extract().strip()
            if text not in keyword_arr:
                keyword_arr.append(text)
    text_arr = response.css('div.hint-mid a::text')  # 96%的人还搜了
    if text_arr:
        for text in text_arr:
            text = text.extract().strip()
            if text not in keyword_arr:
                keyword_arr.append(text)
    text_arr = response.css('div.hintBox table#hint_container.hint tr td p a::text')  # 相关搜索
    if text_arr:
        for text in text_arr:
            text = text.extract().strip()
            if text not in keyword_arr:
                keyword_arr.append(text)
    return keyword_arr


def suggest_search(keyword, keyword_arr):
    """
    建议搜索 下拉框搜索
    :param keyword: 待搜索的关键词
    :return:
    """
    sug_url = "http://www.sogou.com/suggnew/ajajjson?key={}&type=web".format(parse.quote(keyword))
    resp = requests.get(sug_url, headers=headers)
    text = resp.text

    begin_str = '''"{}",['''.format(keyword)
    begin_posi = text.find(begin_str)

    end_str = '''],["0;0;0;0"'''
    end_posi = text.find(end_str)

    if end_posi == -1:
        return keyword_arr
    else:
        sub_text = text[begin_posi + len(begin_str):end_posi]
        sub_text = sub_text.replace('"', '')
        text_arr = sub_text.split(',')
        for t in text_arr:
            if t not in keyword_arr:
                keyword_arr.append(t)
        return keyword_arr


if __name__ == '__main__':
    keyword = "五四青年节"
    keyword_arr = total_fun(keyword)
    print(keyword_arr)
