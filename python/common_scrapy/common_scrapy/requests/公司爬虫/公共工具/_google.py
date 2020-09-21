# -*- coding:utf-8 -*-

import urllib.parse
import execjs, requests, termcolor
import json


# https://translate.google.cn/

# 对字符串数组进行重新拼接
def split_text(text_arr, xianchang=4500):
    """
    :param text_arr: 文本数组
    :param xianchang: 限长
    :return:
    """
    wenben_len = len("".join(text_arr))
    new_text_arr = []
    # print(wenben_len)
    if wenben_len > xianchang:
        # print("需要分割数组")
        text_temp = ""
        for i, tex in enumerate(text_arr):
            if len(text_temp + tex) < xianchang:
                text_temp = text_temp + tex
                if i == len(text_arr) - 1:
                    new_text_arr.append(text_temp)
            else:
                new_text_arr.append(text_temp)
                text_temp = tex

        # len_arr = [len(te) for te in new_text_arr]
        # print(len_arr)
        # for ti in new_text_arr:
        #     print(ti)
    else:
        # print("直接调用翻译")
        new_text_arr.append("".join(text_arr))
    return new_text_arr


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
    content = '''
1.有赞将按照国家法律规定采取相应的安全技术措施和保密措施，以防止泄露和保护你及消费者的数据。
2.就你使用本服务所收集、储存、处理、使用的消费者或其他第三方的数据和实施任何与这些数据有关的活动应当符合以下要求：
1)你应当遵守与有赞的相关协议和规则及现行法律法规的相关规定；
2)你搜集和使用消费者或其他第三方数据应当制定相关隐私保护政策，这些政策能够清晰并准确地向消费者或其他第三方说明你收集个人数据信息内容，如何使用这些信息，以及如何与第三方共享这些信息。隐私政策内容至少要遵从本协议以及有赞的隐私保护政策的要求；
3)如果要处理消费者或其他第三方的个人数据，你应当在向消费者或其他第三方请求获取其任何个人数据时予以充分告知，并取得当事人的明确同意，除非另行获得授权或同意，否则你只能在运行相关应用程序的操作或功能所需的最小限度内处理个人数据；
4)对于有赞提供的任何个人数据，你应当仅能依据有赞的要求来使用这些数据。在有赞要求删除这些数据的情况下，你应当删除这些数据并不得保存；
5)你应当为消费者或其他第三方的数据采取安全措施，以保护消费者或其他第三方的数据免受未经授权的访问和使用。当消费者或其他第三方希望删除其个人数据时，你应当向其提供修改或删除数据的途径和方法，以便他们可以自行完成修改或删除的操作，同时你应当确保相关数据是被彻底删除，无法被还原；
6)在没有得到有赞事先书面同意的情况下，禁止将有赞提供的任何个人数据传送给其他任何国家和个人。所有相关数据的传送都只能在现行的隐私和数据保护法律的允许下进行。
3.如果有赞认为你收集、使用消费者或其他第三方数据的方式，可能损害消费者或其他第三方体验，有赞有权要求你删除相关数据并不得再以该方式收集、使用该等数据。如果有赞要求你删除任何个人数据的，你应当做到：将该数据匿名化，使其不再成为个人数据；或者永久性地删除该数据或者使该数据永久不可读取。同时你应当根据有赞的要求向有赞提供已将该个人数据删除或已进行匿名化处理的书面确认书。
4.消费者或其他第三方授权给你的数据权利属于你，消费者或其他第三方授权给有赞的运营数据、个人数据等数据的全部权利均归属有赞，且是有赞的商业秘密。未经有赞事先书面同意，你不得为本协议约定之外的目的使用前述数据，亦不得以任何形式将前述数据提供给他人。
5.一旦你停止使用本服务，或有赞基于任何原因终止使用本服务，你必须立即删除全部从有赞获得的数据（包括各种备份），且不得再以任何方式进行使用。
6.在本服务之外，你应自行对因使用本服务而存储在有赞服务器的各类数据、信息，采取合理、安全的技术措施，确保其安全性，并对你的行为（包括但不限于自行安装软件、采取加密措施或进行其他安全措施等）所引起的结果承担全部责任。你应当按照国家法律法规的要求向有赞、消费者或其他第三方、相关数据保护机构报告任何对个人数据未经授权的访问和使用。
    '''
    print(content)
    content = content.replace("&amp;", "&")
    js = Return_tk()
    tk = js.getTk(content)
    result = js.zn_to_en_translate(content, tk)
    print(result)

    tk = js.getTk(result)
    result = js.en_to_zn_translate(result, tk)
    print(result)
