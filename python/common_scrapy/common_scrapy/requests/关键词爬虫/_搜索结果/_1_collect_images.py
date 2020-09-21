# -*- coding:utf-8 -*-
import re
import os
import datetime
from threading import Thread
import requests
from random import randint
from scrapy_mongodb_for_search.settings import SQL_DATETIME_FORMAT
from scrapy_mongodb_for_search.my_tools.common import get_md5
from scrapy_mongodb_for_search.my_tools.tools.commons import get_image_extension

create_dir = "D:/WorkSpace______/python/ScrapyUploadImageData/关键词/"


def list_level_two_dir():
    # 一级关键词数组
    one_level_keyword_arr = os.listdir(create_dir)
    for one_level_keyword in one_level_keyword_arr:
        one_level_keyword = one_level_keyword.strip()
        print("当前下载图片的一级关键词为： " + one_level_keyword)
        one_level_keyword_dir = create_dir + one_level_keyword + "/"
        # 二级关键词数组
        two_level_keyword_arr = os.listdir(one_level_keyword_dir)
        for two_level_keyword in two_level_keyword_arr:
            two_level_keyword = two_level_keyword.strip()
            # print("------>" + two_level_keyword)
            print("当前下载图片的二级关键词为： " + two_level_keyword)
            two_level_keyword_dir = create_dir + one_level_keyword + "/" + two_level_keyword + "/"
            if not os.listdir(two_level_keyword_dir + "图片" + "/"):
                # 判断图片文件夹是否为空
                # 如果是空文件夹，则下载图片
                # 如果不是空文件夹，则不下载图片
                # print("------>" + two_level_keyword_dir)
                get_image_urls(two_level_keyword, two_level_keyword_dir)
            print("二级关键词 " + two_level_keyword + " 的相关图片下载完成！")


def get_image_urls(keyword, save_dir):
    keyword = keyword.strip("长尾词")
    image_arr = set()
    request_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn={0}'

    headers = {
        "Host": "image.baidu.com",
        "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
    }

    # pn_max = randint(6, 12)  # 实战中设置为 (6, 12) 测试时设置为 (1, 2)
    for pn in range(0, 12):
        # 每个页面的 objURL 数量为 60 所以要 乘以 60
        req_url = request_url.format(pn * 60)
        headers.update({"Referer": req_url})
        resp = requests.get(req_url, {'headers': headers})
        print("正在抓取 " + req_url + " 页面的图片 URL 地址！")
        pic_url = re.findall('"objURL":"(.*?)",', resp.text, flags=re.I | re.S)
        if pic_url:
            for url in pic_url:
                if len(url) > 0:
                    image_arr.add(url)
    if len(image_arr) > 0:
        line_threads = []
        print("共需要下载 " + str(len(image_arr)) + " 张图片！")
        # 这里可以修改成多线程的方式
        for image_url in image_arr:
            line_thread = Thread(target=download_image, args=(image_url, save_dir))
            line_threads.append(line_thread)
        for lt in line_threads:
            lt.start()
        for lt in line_threads:
            lt.join()
        print(str(len(image_arr)) + " 下载完成！")


def download_image(image_url, save_dir):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
    }
    headers.update({"Referer": image_url})
    try:
        pic = requests.get(image_url, headers=headers, timeout=7)
        content = pic.content
    except BaseException:
        print('错误 ' + image_url + ' 图片无法下载！')
    else:
        if len(content) < 1024 * 10:  # 过滤内容长度小于 10K 的图片
            print('图片 ' + image_url + ' 太小了，放弃下载')
        else:
            print("当前下载的图片地址为：" + image_url)
            # print("当前下载的图片长度为：" + str(len(content)))
            # print("当前下载的图片名称为：" + get_md5(image_url))
            # 去重和创建文件夹
            pic_dir = save_dir + "图片" + "/"
            # 去重和创建图片文件
            pic_sort_path = get_md5(image_url) + get_image_extension(image_url)
            pic_file_path = pic_dir + pic_sort_path
            exist = os.path.exists(pic_file_path)  # 去重
            if not exist:
                fp = open(pic_file_path, 'wb')
                fp.write(content)
                print(image_url + " 的图片下载成功！")
                fp.close()


if __name__ == '__main__':
    all_time_start = "发布开始时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    list_level_two_dir()
    all_time_end = "发布结束时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    print(all_time_start)
    print(all_time_end)
