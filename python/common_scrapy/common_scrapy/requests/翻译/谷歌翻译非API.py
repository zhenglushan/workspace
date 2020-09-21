# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 谷歌翻译非API.py
# @DATETime   : 2020/5/19 10:42
# @Author     : 笑看风云


import urllib.parse
import execjs, requests, termcolor
import json


# https://translate.google.cn/

class Return_tk():
    '''
    使用时，不要超过 1500 个汉字
    '''

    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };
    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        '''
        返回 tk 对象
        :param text:
        :return:
        '''
        return self.ctx.call("TL", text)

    def open_url(self, url):
        '''
        打开请求地址
        :param url:
        :return:
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        req = requests.get(url=url, headers=headers)
        if req.status_code == 200:
            return req.content.decode('utf-8')
        else:
            return "是不是翻译的文本太长了？？？"

    def max_length(self, content):
        '''
        检测请求字符串的长度
        使用时，不要超过 1500 个汉字
        :param content:
        :return:
        '''
        if len(content) > 4891:
            print("----------> 翻译文本超过限制！----------> ")
            return

    def print_result(self, parm):
        '''
        打印翻译结果
        :param parm:
        :return:
        '''
        return_str = ''
        result = parm
        result_list = json.loads(result)
        result_list = result_list[0]
        if len(result_list) > 0:
            for temp_list in result_list:
                if temp_list:
                    one = temp_list[0]
                    if one:
                        return_str = return_str + str(one)
        return return_str
        # str_end = result.find("\",")
        # if str_end > 4:
        #     print("翻译的结果为：", result[4:str_end])

    def en_to_zn_translate(self, content, tk):
        '''
        英文翻译成中文
        :param content:
        :param tk:
        :return:
        '''
        self.max_length(content)
        content = urllib.parse.quote(content)
        # 英译汉
        url = "http://translate.google.cn/translate_a/single?client=t" \
              "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
              "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
              "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)
        result = self.open_url(url)
        return self.print_result(result)

    def zn_to_en_translate(self, content, tk):
        '''
        中文翻译成英文
        :param content:
        :param tk:
        :return:
        '''
        self.max_length(content)
        content = urllib.parse.quote(content)
        # 汉译英
        url = "http://translate.google.cn/translate_a/single?client=t" \
              "&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
              "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8" \
              "&source=btn&ssel=3&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)
        result = self.open_url(url)
        return self.print_result(result)


if __name__ == '__main__':
    content = '很少有国家有审查双重用途研究的明确程序。 美国也许有最强硬的政策，但它仍然有一些漏洞。 它只覆盖了15个大的、不好的病原体和马瘟，尽管与其中一种病原体有关，但它本身并不存在。 它也只涉及联邦资助的研究，埃文斯的研究是私人资助的。 他在加拿大做了他的工作，但他在美国也可以轻而易举地这样做。如果没有更明确的指导方针，科研企业将承担起自我监管的责任，而且它并不能很好地做到这一点。 伦敦大学国王学院研究生物威胁的 Filippa Lentzos 说，学术界竞争激烈,"驱动因素是获得奖学金和出版物，而不一定是要成为负责任的公民。"他研究生物威胁。 这意味着科学家常常把他们的工作留给自己，以免被同龄人挖走。 他们的计划只有在已经颁布之后才会广为人知，而且结果已经准备就绪，可以提交或公布。 这种缺乏透明度的做法创造了一种环境，人们几乎可以单方面作出可能影响整个世界的决定。以马瘟研究为例。 埃文斯是世界卫生组织的一个委员会的成员，该委员会负责监督天花的研究，但是他只是在实验完成后。'
    print(content)
    content = content.replace("&amp;", "&")  # 需要把 &amp; 替换为空或者 &，否则无法翻译
    js = Return_tk()
    tk = js.getTk(content)
    result = js.zn_to_en_translate(content, tk)
    print(result)

    tk = js.getTk(result)
    result = js.en_to_zn_translate(result, tk)
    print(result)
