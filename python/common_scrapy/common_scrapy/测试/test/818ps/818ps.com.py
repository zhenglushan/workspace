# -*- coding:utf-8 -*-
import requests
import urllib3
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from threading import Thread

url_temp = "https://818ps.com/muban/{0}.html"


def arr_size(arr, size):
    '''
    将数组 arr 分割成若干个数组块
    每个数组块的长度不超过 size 的大小
    :param arr: 要分割的数组
    :param size: 数组块的长度
    :return: 返回值是一个二维数组
    '''
    arr_arr = []
    for i in range(0, int(len(arr)) + 1, size):
        temp = arr[i:i + size]
        if len(temp) > 0:
            arr_arr.append(temp)
    return arr_arr


def get_baidu_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
    }
    return headers


headers = get_baidu_headers()
headers.update({"Host": "818ps.com"})

int_list = range(1, 6100000)
file_path_temp_open = open("818ps.com.txt", 'a')


def fetch_url(url_source):
    global file_path_temp_open
    req = requests.get(url_source, headers=headers, allow_redirects=True)
    url_result = req.url
    if url_source == url_result:
        print(url_source + " 没有跳转地址！！！")
    else:
        print(url_source + " 跳转后的地址为： " + url_result)
        file_path_temp_open.write(url_source + "[zls]" + url_result + "\n")


line_array = []

for i in int_list:
    url_source = url_temp.format(i)
    line_array.append(url_source)

print("line_array 填充 url_source 完成！")

line_threads = []  # 添加线程组
for url_source in line_array:
    line_thread = Thread(target=fetch_url, args=(url_source,))
    line_threads.append(line_thread)

print("line_threads 线程组填充 url_source 完成！")

# 分割数组，变成二维数组
line_threads_arr = arr_size(line_threads, 1000)
for lt in line_threads_arr:
    for l in lt:  # 开启线程
        l.start()
    for l in lt:  # 阻塞线程
        l.join()
    sleep(0.1)

file_path_temp_open.close()
