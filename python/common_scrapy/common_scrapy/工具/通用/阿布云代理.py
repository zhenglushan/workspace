# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : IP代理工具.py
# @DATETime   : 2020/5/18 15:08
# @Author     : 笑看风云
import requests
from common_scrapy.settings import PROXY_PASS, PROXY_USER

# 是否使用代理
is_use_proxy = True


def abuyun_proxy_requests(headers, url, cookies=None):
    """
    使用阿布云IP代理工具
    :param headers:
    :param url:
    :param cookies:
    :return:
    """
    # 要访问的目标页面
    targetUrl = "http://httpbin.org/get"  # 返回 IP 相关信息
    # targetUrl = "http://proxy.abuyun.com/switch-ip"
    # targetUrl = "http://proxy.abuyun.com/current-ip"

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 使用 HTTP 隧道 动态版
    # 代理隧道验证信息
    proxyUser = PROXY_USER  # 通行证书
    proxyPass = PROXY_PASS  # 通行密钥

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    try:
        if cookies:
            response = requests.get(url=url, headers=headers, proxies=proxies, timeout=30, cookies=cookies)
        else:
            response = requests.get(url=url, headers=headers, proxies=proxies, timeout=30)
        return response
    except:
        print("获取阿布云的代理 IP 时，出现了问题！")


if __name__ == '__main__':
    headers = {}
    resp = abuyun_proxy_requests(headers, "http://httpbin.org/get")
    print(resp.status_code)
    print(resp.text)
