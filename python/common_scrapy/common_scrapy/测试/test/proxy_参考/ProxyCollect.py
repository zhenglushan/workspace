# -*- coding:utf-8 -*-
import re
import os
import requests
from ScrapyUploadImage.tools.commons import baidu_user_agent
from bs4 import BeautifulSoup
import random
import urllib3
from time import sleep
from ScrapyUploadImage.tools.test.proxy_参考.collect_ip import CollectIP_1

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from threading import Thread


class CollectWebData():
    url_temp = "https://818ps.com/muban/{0}.html"
    headers = {
        'User-Agent': baidu_user_agent
    }
    headers.update({"Host": "818ps.com"})
    int_list = range(3200000, 6100000)
    page_code = 'UTF-8'
    use_proxy_list = {}

    def __init__(self):
        proxyCollect = CollectIP_1()
        proxy_list = proxyCollect.proxy_list
        for proxy in proxy_list:
            proxy_arr = proxy.split(",")
            ip = proxy_arr[0]  # ip
            port = proxy_arr[1]  # 端口
            httptype = proxy_arr[2]  # http https
            # speed = proxy_arr[3]  # 访问速度
            if proxyCollect.judge_ip(ip, port, httptype):
                self.use_proxy_list[httptype.lower()] = "{0}://{1}:{2}".format(httptype.lower(), ip, port)

        line_array = []

        for i in self.int_list:
            url_source = self.url_temp.format(i)
            line_array.append(url_source)

        print("line_array 填充 url_source 完成！")

        line_threads = []  # 添加线程组
        for url_source in line_array:
            line_thread = Thread(target=self.fetch_url, args=(url_source,))
            line_threads.append(line_thread)

        print("line_threads 线程组填充 url_source 完成！")

        # 分割数组，变成二维数组
        line_threads_arr = self.arr_size(line_threads, 1000)
        for lt in line_threads_arr:
            for l in lt:  # 开启线程
                l.start()
            for l in lt:  # 阻塞线程
                l.join()
            sleep(0.1)

    def arr_size(self, arr, size):
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

    def fetch_url(self, url_source):
        try:
            req = requests.get(url_source, proxies=self.use_proxy_list, headers=self.headers, allow_redirects=True,
                               timeout=30)
            url_result = req.url
            if url_source != url_result:
                print(url_source + " 跳转后的地址为： " + url_result)
                resp = requests.get(url_source, proxies=self.use_proxy_list, headers=self.headers, allow_redirects=True,
                                    timeout=30)
                resp.encoding = self.page_code
                soup = BeautifulSoup(resp.text, "html5lib")
                title = soup.select_one("title").text
                with open("818ps.com.txt", 'a') as fa:
                    fa.write(url_result + "[zls]" + title + "\n")
        except Exception:
            print(url_source + " 采集失败！！！")
            with open("false_818ps.com.txt", 'a') as fa:
                fa.write(url_source + "\n")
            # print("代理有问题，重新进入抓取行为！")
            # self.fetch_url(url_source)


if __name__ == '__main__':
    url = "http://ip.t086.com/getip.php"

    headers = {
        'User-Agent': baidu_user_agent,
        'Host': "ip.t086.com",
        "Referer": url
    }

    print("原有 IP ：" + requests.get(url, headers=headers).text)

    if os.path.exists("./__main__.txt"):
        with open("./__main__.txt", 'r') as f:
            proxy_str = f.read()
        if proxy_str:
            proxy_list = proxy_str.split("\n")
            for proxy in proxy_list:
                data_arr = proxy.split(",")
                ip_data = data_arr[0]
                port_data = data_arr[1]
                https_data = data_arr[2].lower()
                new_data = {
                    https_data: ip_data + ":" + port_data
                }
                try:
                    print("代理 IP ：" + requests.get(url, headers=headers, proxies=new_data, timeout=3).text)
                except Exception as e:
                    print(ip_data + "不可用")
