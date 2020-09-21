# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 百度翻译API.py
# @DATETime   : 2020/5/19 10:41
# @Author     : 笑看风云


# http://api.fanyi.baidu.com/api/trans/product/apidoc

import http.client
from urllib import parse
import http.client
import hashlib
import urllib
import random
import json


def baidu_trans(text, fromLang, toLang):
    """
    fromLang = 'en'
    toLang = 'zh'
    :param text: 汉字不超过 1000 字，英文不超过 3000 字
    :param fromLang: 原文语种
    :param toLang: 译文语种
    :return:
    """
    appid = '20190720000319852'  # 填写你的appid
    secretKey = 'WEyxvPQ5BlOJKn3kcCq7'  # 填写你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    data = {
        'appid': appid,
        'q': text,
        'from': fromLang,
        'to': toLang,
        'salt': str(salt),
        'sign': sign
    }
    data = urllib.parse.urlencode(data)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('POST', myurl, body=data, headers=headers)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        trans_result = result['trans_result']
        text_arr = [trans['dst'] for trans in trans_result]
        text_arr_str = "".join(text_arr)
        return text_arr_str

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


# 对字符串数组进行重新拼接
def split_text(text_arr, max_length=4500):
    """
    :param text_arr: 文本数组
    :param xianchang: 限长
    :return:
    """
    wenben_len = len("".join(text_arr))
    new_text_arr = []
    # print(wenben_len)
    if wenben_len > max_length:
        # print("需要分割数组")
        text_temp = ""
        for i, tex in enumerate(text_arr):
            if len(text_temp + tex) < max_length:
                text_temp = text_temp + tex
                if i == len(text_arr) - 1:
                    new_text_arr.append(text_temp)
            else:
                new_text_arr.append(text_temp)
                text_temp = tex
    else:
        # print("直接调用翻译")
        new_text_arr.append("".join(text_arr))
    return new_text_arr


text_arr = []
with open("../1.txt", mode='r', encoding='utf8') as rf:
    for line in rf:
        line = line.strip()
        line = line.replace('<p>', '♈').replace('<P>', '♈').replace('</p>', '♉').replace('</P>', '♉')
        text_arr.append(line)

text = "".join(text_arr)

text = text[0:2000]
print(text)
print(len(text))

en_result = baidu_trans(text, fromLang="zh", toLang="en")
print(en_result)

print(len(en_result))
en_result = en_result[0:6000]
cn_result = baidu_trans(en_result, fromLang="en", toLang="zh")
print(cn_result)
