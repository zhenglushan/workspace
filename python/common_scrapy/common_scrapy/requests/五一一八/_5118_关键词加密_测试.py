# -*- coding:utf-8 -*-

import urllib.parse
import execjs, requests, termcolor
import json
'''
5118 与 爱站的 URL 加密是一样的方式。
区别是 5118 对加密结果做了字符串反转，而爱站没有。
'''


class Return_tk():
    def __init__(self):
        self.ctx = execjs.compile("""
        function encode_unicode_param(t) {
            for (var e = "", a = 0; a < t.length; a++) {
                var i = t.charCodeAt(a).toString(16);
                2 == i.length ? e += "n" + i: e += i
            }
            return e
        }
        
        function decode_unicode_param(t) {
            t = t.replace(/n/g, "00");
            for (var e = "", a = 0; a < t.length / 4; a++)
                e += unescape("%u" + t.substr(4 * a, 4));
            return e
        }
        """)


if __name__ == '__main__':
    js = Return_tk()
    word_list = ["网络营销", "网络营销公司", "网络营销课程", "网络营销培训"]
    ci_url = "https://ci.5118.com/"
    for word in word_list:
        result = js.ctx.call("encode_unicode_param", word)
        result = result[::-1]
        new_url = ci_url + result + "/"
        print(new_url)
