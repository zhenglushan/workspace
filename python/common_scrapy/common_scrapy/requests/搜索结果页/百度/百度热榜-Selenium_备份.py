# -*- coding:utf-8 -*-
# @Email	  : 276517382@qq.com
# @FileName   : 百度热榜-Selenium.py
# @DATETime   : 2020-05-06 上午 09:59
# @Author     : 笑看风云

from urllib import parse
from selenium import webdriver
from scrapy.http import HtmlResponse
from time import sleep
import datetime
from scrapy_mongodb_for_search.settings import SQL_DATETIME_FORMAT

"""
备用采集:
https://tophub.today/n/Jb0vmloB1G
"""

save_path = "D:/WorkSpace/数据采集/百度热搜/"

def get_search_keywords(keyword_arr):
    url = "https://www.baidu.com/s?wd=" + parse.quote("实时热榜")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 无界面执行
    options.add_argument("--window-size=100,100")  # 设置浏览器大小
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    browser = webdriver.Chrome(executable_path="D:/WorkSpace/web_driver/chromedriver.exe", options=options)
    browser.get(url)
    page_source = browser.page_source
    browser.quit()
    sleep(0.3)
    response = HtmlResponse(url=url, body=page_source, encoding='utf8')
    text_arr = response.css('table.c-table.opr-toplist1-table a::text')
    if text_arr:
        for text in text_arr:
            text = text.root
            text = text.strip()
            if text not in keyword_arr:
                keyword_arr.append(text)
    if keyword_arr:
        return keyword_arr
    else:
        return []


def get_list_keywords(keyword_arr):
    url_list = [
        'http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513',
        'http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513',
        'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341_c513',
        'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513',
        'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513',
        'http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513'
    ]
    for url in url_list:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # 无界面执行
        options.add_argument("--window-size=100,100")  # 设置浏览器大小
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        browser = webdriver.Chrome(executable_path="D:/WorkSpace/web_driver/chromedriver.exe", options=options)
        browser.get(url)
        page_source = browser.page_source
        browser.quit()
        sleep(0.3)
        response = HtmlResponse(url=url, body=page_source, encoding='utf8')
        text_arr = response.css('table.list-table td.keyword a:first-of-type::text')
        if text_arr:
            for text in text_arr:
                text = text.root
                text = text.strip()
                if text not in keyword_arr:
                    keyword_arr.append(text)
    if keyword_arr:
        return keyword_arr
    else:
        return []

def create_file():
    pass


def get_article(article_arr, keyword):
    url = "https://www.baidu.com/s?wd=" + parse.quote(keyword)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 无界面执行
    options.add_argument("--window-size=100,100")  # 设置浏览器大小
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    browser = webdriver.Chrome(executable_path="D:/WorkSpace/web_driver/chromedriver.exe", options=options)
    browser.get(url)
    page_source = browser.page_source
    browser.quit()
    sleep(0.1)
    response = HtmlResponse(url=url, body=page_source, encoding='utf8')
    href_arr = response.css('div.c-offset div.c-row a::attr(href)')
    if href_arr:
        href_arr_temp = []
        for href in href_arr:
            href = href.root
            href = href.strip()
            if href not in href_arr_temp:
                href_arr_temp.append(href)




    return article_arr


if __name__ == '__main__':
    all_time_start = "百度热榜开始采集的时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"

    # 1、获取关键词数组
    keyword_arr = []
    keyword_arr = get_search_keywords(keyword_arr)
    keyword_arr = get_list_keywords(keyword_arr)
    print(keyword_arr)

    # 2、采集关键词对应的文章
    article_arr = []
    for keyword in keyword_arr:
        article_arr = get_article(article_arr, keyword)
    print(article_arr)

    all_time_end = "百度热榜结束采集的时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    print(all_time_start)
    print(all_time_end)
