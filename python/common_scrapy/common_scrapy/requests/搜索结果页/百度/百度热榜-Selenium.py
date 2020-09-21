# -*- coding:utf-8 -*-
# @Email	  : 276517382@qq.com
# @FileName   : 百度热榜-Selenium.py
# @DATETime   : 2020-05-06 上午 09:59
# @Author     : 笑看风云

import os
import re
import base64
import random
from urllib import parse
from selenium import webdriver
from scrapy.http import HtmlResponse
from time import sleep
import datetime
from scrapy_mongodb_for_search.settings import SQL_DATETIME_FORMAT
from scrapy_mongodb_for_search.my_tools.common import get_md5
from scrapy_mongodb_for_search.my_tools.tools.commons import post_dede
from scrapy_mongodb_for_search.my_tools.fenci import FenCi

"""
流程：
1、采集关键词并保存到文件；
2、通过关键词直接采集文章并发布；
3、修改文件名，加 _ 前缀，代表已经使用；
4、判断是否重复采集时，需要判断加和没加 _ 的 MD5 文件是否存在。

读取网址采集时，需要过滤关键词，查看文件大小 2K 的文件。
"""

"""
备用采集:
https://tophub.today/n/Jb0vmloB1G
"""

fen_ge_path = "D:/WorkSpace/python/scrapy_mongodb_for_search/scrapy_mongodb_for_search/my_files/project_files/标题分隔符.txt"
fen_ge_arr = []
with open(fen_ge_path, mode='r', encoding="UTF-8") as fgfr:
    for line in fgfr:
        line = line.strip("\r\n")
        if "空格" in line:
            line = line.replace("空格", " ")
        fen_ge_arr.append(line)

save_path = "D:/WorkSpace/数据采集/百度热榜/1/"


# 文件名还原成未发布
def huan_yuan():
    txt_file_list = os.listdir(save_path)
    for txt_file_name in txt_file_list:
        if txt_file_name.startswith("_"):
            old_file_path = save_path + txt_file_name
            new_file_path = save_path + txt_file_name[1:]
            os.rename(old_file_path, new_file_path)


# 通过搜索收集关键词
def get_search_keywords():
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
            # 判断文件是否已存在
            save_file_path_1 = save_path + get_md5(text) + ".txt"
            save_file_path_2 = save_path + "_" + get_md5(text) + ".txt"
            if (not os.path.exists(save_file_path_1)) and (not os.path.exists(save_file_path_2)):
                print("当前采集的关键词是：\t" + text)
                urls = get_urls(text)
                urls = [text] + urls
                with open(save_file_path_1, mode="a", encoding="UTF-8") as textfw:
                    textfw.write("\n".join(urls))


# 通过热榜页面收集关键词
def get_list_keywords():
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
                # 判断文件是否已存在
                save_file_path_1 = save_path + get_md5(text) + ".txt"
                save_file_path_2 = save_path + "_" + get_md5(text) + ".txt"
                if (not os.path.exists(save_file_path_1)) and (not os.path.exists(save_file_path_2)):
                    print("当前采集的关键词是：\t" + text)
                    urls = get_urls(text)
                    urls = [text] + urls
                    with open(save_file_path_1, mode="a", encoding="UTF-8") as textfw:
                        textfw.write("\n".join(urls))


# 搜索关键词的最新相关信息
def get_urls(keyword):
    href_arr_temp = []
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
        for href in href_arr:
            href = href.root
            href = href.strip()
            if href not in href_arr_temp:
                href_arr_temp.append(href)
    return href_arr_temp


# 读取所有文件
def read_all_txt_file():
    txt_file_list = os.listdir(save_path)
    # random.shuffle(txt_file_list)
    # txt_file_list = txt_file_list[0:10]
    for txt_file_name in txt_file_list:
        if not txt_file_name.startswith("_"):
            txt_file_path = save_path + txt_file_name
            with open(txt_file_path, mode='r', encoding='UTF-8') as fr:
                print("当前文件地址：\t" + txt_file_path)
                keyword = ''
                for index, line in enumerate(fr):
                    line = line.strip()
                    if index == 0:
                        # print("当前关键词为：\t" + line)
                        keyword = line
                    else:
                        # print("当前采集网址为：\t" + line)
                        lit_pic_path, day_time, title, body = spider_content(line)
                        if day_time and title and body:
                            post_article(keyword, lit_pic_path, day_time, title, body)
            # 修改文件名称，加上 _ 前缀符号
            txt_file_path_new = save_path + "_" + txt_file_name
            os.rename(txt_file_path, txt_file_path_new)


# 抓取页面的标题、发布日期时间、正文
def spider_content(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 无界面执行
    options.add_argument("--window-size=100,100")  # 设置浏览器大小
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    browser = webdriver.Chrome(executable_path="D:/WorkSpace/web_driver/chromedriver.exe", options=options)
    browser.get(url)
    page_source = browser.page_source
    current_url = browser.current_url
    browser.quit()
    sleep(0.1)
    if "baijiahao.baidu.com" in current_url:
        # print("当前地址：\t" + current_url)
        # print(page_source)
        response = HtmlResponse(url=current_url, body=page_source, encoding='utf8')
        day_time_slct = response.css("meta[itemprop=dateUpdate]::attr(content)")
        day_time = day_time_slct[0].root
        title_slct = response.css("div.article-title h2::text")
        title = title_slct[0].root
        body_slct = response.xpath(
            "//div[@class='article-content']//p | //div[@class='article-content']/div[@class='img-container']//img")
        body_slct = body_slct.extract()
        body = ''
        for item in body_slct:
            if item.startswith("<img"):
                item = "<p>" + item + "</p>"
            body = body + item

        # 过滤所有HTML标签的属性除了 src 和 alt 属性，同时把值的长度为零的属性也删除
        # re_rule = re.compile('\s(?!src|alt)[a-zA-Z]+=[\'\"]{1}[^\'\"]+[\'\"]{1}', re.I)
        re_rule = re.compile('\s(?!src)[a-zA-Z0-9|\-|:]+=[\'\"]{1}[^\'\"]*[\'\"]{1}', flags=re.I | re.S)
        body = re_rule.sub("", body).replace("<span>", "").replace("</span>", "")
        # 提取并替换 src 属性值
        re_rule = re.compile('src=[\"\']([^<]*)[\"\']', flags=re.I | re.S)
        src_arr = re.findall(re_rule, body)
        lit_pic_path = ""
        if src_arr:
            src_arr_len = len(src_arr)
            src_arr_index = random.randint(0, src_arr_len - 1)
            for index_n, src in enumerate(src_arr):
                src_base64_enc = base64.encodebytes(src.encode("UTF-8"))
                src_base64 = src_base64_enc.decode("UTF-8")
                src_base64_len = len(src_base64)
                index = random.randint(0, src_base64_len // 3)
                start = src_base64[0:index]
                end = src_base64[index:src_base64_len - 1]
                img_fix = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.swf']
                new_src = "/uploads/allimg/" + start + random.choice(img_fix) + "?token=" + end
                body = body.replace(src, new_src)
                if index_n == src_arr_index:
                    lit_pic_path = new_src
        return lit_pic_path, day_time, title, body
    else:
        return '', '', '', ''


# 发布文章到网站
def post_article(keyword, lit_pic_path, day_time, title, body):
    keyword = fen_ge_arr[random.randint(0, len(fen_ge_arr) - 1)].format(keyword)
    title = keyword + title
    fenci = FenCi(body)
    tags, _, _ = fenci.returnValues()
    keywords = tags
    try:
        # print("缩略图为：" + lit_pic_path)
        result = post_dede(title, day_time, body, "www.btzkl.com", lit_pic_path, tags, keywords)  # 发布操作
    except Exception as e:
        print(title + " 文章因为异常而导致发布失败！" + "\n")
    else:
        if result:
            pass
            # print(title + " 文章提交后发布成功！" + "\n")
        else:
            print(title + " 文章提交后发布失败！" + "\n")


if __name__ == '__main__':
    all_time_start = "百度热榜开始采集的时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"

    # 1、获取关键词数组
    get_search_keywords()
    get_list_keywords()

    # 2、读取所有文件
    read_all_txt_file()

    # 3、把已发布文件还原成未发布
    # huan_yuan()

    all_time_end = "百度热榜结束采集的时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"

    print(all_time_start)
    print(all_time_end)
