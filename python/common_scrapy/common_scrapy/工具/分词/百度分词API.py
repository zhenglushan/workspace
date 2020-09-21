# -*- coding:utf-8 -*-
"""
    API 使用说明: http://ai.baidu.com/docs#/NLP-Python-SDK/top

    API 安装: pip install baidu-aip

    百度云 - 自然语言处理 - 主页
    https://console.bce.baidu.com/ai/#/ai/nlp/overview/index
"""
from aip import AipNlp
from time import sleep

""" 你的 APPID AK SK """
APP_ID = '16868446'
API_KEY = 'XU7yXikgVMtQUGgKumeLAD4v'
SECRET_KEY = 'cxqGAttPCGYcEGYGkw333yIVP4dVPfP7'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
client.setConnectionTimeoutInMillis(3000)
client.setSocketTimeoutInMillis(3000)

text_arr = [
    "妩媚少妇二宮ナナ大胆性感美图",
    "可爱萝莉仓井优香真空演绎湿身诱惑",
    "乌克兰美女车模性感双眼迷人",
    "原幹恵高清性感美图 不一样的精彩",
    "美空美丽模特儿杨丽Lacee",
    "足球宝贝杨棋涵浴火重生",
    "霸气尤老师左拥右抱床上调教母女花",
    "超漂亮的平面代言模特小欣",
    "看不够的迷人韩国美女车模—韩敏智",
    "性感翘臀美女丝袜美腿高清写真",
]

pos_arr = ['n', 'nr', 'ns', 'nt', 'nz', 'a', 'an', 'vn']  # 词性，词性标注算法使用。
ne_arr = ['PER', 'LOC', 'ORG']  # 命名实体类型，命名实体识别算法使用。

for text in text_arr:
    print(text)
    result = client.lexer(text)
    items = result['items']
    for temp_item in items:
        pos = temp_item['pos']
        ne = temp_item['ne']
        byte_length = temp_item['byte_length']
        item = temp_item['item']
        basic_words = temp_item['basic_words']
        if byte_length > 2:  # 长度必须超过一个汉字
            if (len(pos) > 0 and pos in pos_arr) or (len(pos) == 0 and ne in ne_arr):
                if len(basic_words) == 1:  # 只留 basic_words 长度为 1 的 temp_item
                    print(item, pos, ne, byte_length, basic_words)
                    print("--------------------")
    print("********************")
    sleep(1)
