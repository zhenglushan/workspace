# -*- coding:utf-8 -*-
import re
import os
import requests
from ScrapyUploadImage.tools.commons import baidu_user_agent
from bs4 import BeautifulSoup
import random
import urllib3
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from threading import Thread


class CollectIP_1():
    '''
    采集西刺免费代理IP
    '''
    headers = {
        'User-Agent':baidu_user_agent
    }
    page_code = 'UTF-8'
    proxy_list = []
    ip_file_name = __name__ + ".txt"

    def __init__(self):
        self.read_ips_file()
        if len(self.proxy_list) < 50:
            self.crawl_ips()
            self.write_ips_file()

    def crawl_ips(self):
        '''
        抓取代理的 IP 端口 HTTP(S) 访问速度的数据
        :return:
        '''
        for i in range(1, 10):
            resp = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=self.headers)
            resp.encoding = self.page_code
            html = resp.text
            soup = BeautifulSoup(html, 'html5lib')
            all_trs = soup.select("table#ip_list tr")

            for tr in all_trs[1:]:
                speed_str = tr.select("div.bar")[0].get('title')
                if speed_str:
                    speed = float(speed_str.split("秒")[0])  # 速度
                    reg = re.compile("[a-zA-Z0-9_\u4e00-\u9fa5]+", flags=re.I | re.S)
                    tds_arr = tr.find_all(text=reg)
                    if len(tds_arr) == 7:
                        ip = tds_arr[0]  # ip
                        port = tds_arr[1]  # 端口
                        httptype = tds_arr[4]  # http https
                        speed = speed  # 访问速度
                        if self.judge_ip(ip, port, httptype):
                            print(ip, port, httptype, speed, "   可以使用哦！！！")
                            self.proxy_list.append("{0},{1},{2},{3}".format(ip, port, httptype, speed))
                        else:
                            print(ip, port, httptype, speed, "   无法使用了哦！！！")

    def judge_ip(self, ip, port, httptype):
        '''
        判断 ip 是否可用
        :param ip: ip 地址
        :param port: 端口号
        :return:
        '''
        http_url = "https://www.baidu.com/"
        proxy_url = "{0}://{1}:{2}".format(ip, port, httptype)
        try:
            proxy_dict = {
                httptype: proxy_url,
            }
            # 设置代理，并使用代理来访问百度
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            # print("无效的 ip 和 port")
            return False
        else:
            code = response.status_code  # 状态码
            if code >= 200 and code < 300:
                # print(" code 的值为 : " + str(code))
                # print("有效的 ip 和 port")
                return True
            else:
                # print("无效的 ip 和 port")
                return False

    def write_ips_file(self):
        '''
        把代理 IP 写入文件中
        :return:
        '''
        with open("./" + self.ip_file_name, 'w') as f:
            f.write("\n".join(self.proxy_list))

    def read_ips_file(self):
        '''
        从文件中读取 IP 地址
        :return:
        '''
        if os.path.exists("./" + self.ip_file_name):
            with open("./" + self.ip_file_name, 'r') as f:
                proxy_str = f.read()
            if proxy_str:
                self.proxy_list = proxy_str.split("\n")
        else:
            self.proxy_list.append("")


class CollectIP_2():
    headers = baidu_user_agent
    page_code = 'UTF-8'
    proxy_list = []

    def __init__(self):
        self.read_ips_file()
        if len(self.proxy_list) < 50:
            self.crawl_ips()
            self.write_ips_file()

    def crawl_ips(self):
        '''
        抓取代理的 IP 端口 HTTP(S) 访问速度的数据
        :return:
        '''
        for i in range(1, 10):
            resp = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=self.headers)
            resp.encoding = self.page_code
            html = resp.text
            soup = BeautifulSoup(html, 'html5lib')
            all_trs = soup.select("table#ip_list tr")

            for tr in all_trs[1:]:
                speed_str = tr.select("div.bar")[0].get('title')
                if speed_str:
                    speed = float(speed_str.split("秒")[0])  # 速度
                    reg = re.compile("[a-zA-Z0-9_\u4e00-\u9fa5]+", flags=re.I | re.S)
                    tds_arr = tr.find_all(text=reg)
                    if len(tds_arr) == 7:
                        ip = tds_arr[0]  # ip
                        port = tds_arr[1]  # 端口
                        httptype = tds_arr[4]  # http https
                        speed = speed  # 访问速度
                        if self.judge_ip(ip, port, httptype):
                            print(ip, port, httptype, speed, "   可以使用哦！！！")
                            self.proxy_list.append("{0},{1},{2},{3}".format(ip, port, httptype, speed))
                        else:
                            print(ip, port, httptype, speed, "   无法使用了哦！！！")

    def judge_ip(self, ip, port, httptype):
        '''
        判断 ip 是否可用
        :param ip: ip 地址
        :param port: 端口号
        :return:
        '''
        http_url = "https://www.baidu.com/"
        proxy_url = "{0}://{1}:{2}".format(ip, port, httptype)
        try:
            proxy_dict = {
                httptype: proxy_url,
            }
            # 设置代理，并使用代理来访问百度
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            # print("无效的 ip 和 port")
            return False
        else:
            code = response.status_code  # 状态码
            if code >= 200 and code < 300:
                # print(" code 的值为 : " + str(code))
                # print("有效的 ip 和 port")
                return True
            else:
                # print("无效的 ip 和 port")
                return False

    def write_ips_file(self):
        '''
        把代理 IP 写入文件中
        :return:
        '''
        with open("./ips.txt", 'w') as f:
            f.write("\n".join(self.proxy_list))

    def read_ips_file(self):
        '''
        从文件中读取 IP 地址
        :return:
        '''
        with open("./ips.txt", 'r') as f:
            proxy_str = f.read()
        if proxy_str:
            self.proxy_list = proxy_str.split("\n")


if __name__ == '__main__':
    CollectIP_1()
