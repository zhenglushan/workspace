# -*- coding:utf-8 -*-

import urllib.parse
import execjs, requests, termcolor
import json


class getZhiShu():

    def __init__(self):
        jscode = self.get_jscode()
        self.ctx = execjs.compile(jscode)

    def get_jscode(self):
        with open("./detail.js", 'r', encoding='utf-8') as js:
            jscode = js.read()
        return jscode

    def get_encode_unicode(self, text):
        decodeURI = self.get_decode_uri(text)
        return self.ctx.call("search", decodeURI)

    def get_decode_uri(self,text):
        return self.ctx.call("submit", text)

if __name__ == '__main__':
    text = '网络营销'
    getZhiShu = getZhiShu()
    result = getZhiShu.get_decode_uri(text)
    print(result)
