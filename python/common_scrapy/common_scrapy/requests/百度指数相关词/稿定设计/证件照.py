# -*- coding:utf-8 -*-
# @ProjectName: PyCompany
# @Email	  : 276517382@qq.com
# @FileName   : BaiduSuggestion.py
# @DATETime   : 2019/12/18 13:39
# @Author     : 笑看风云

import requests, json, time, os
from ScrapyMongoDBForSearch.工具.通用工具 import generator_file_arr

"""
本程序为百度搜索下拉框关键词的采集实现代码
"""

"""
实际应用中，单字母循环的性价比更高，速度和词数都比较可观。
字母双循环，速度慢，词量也并没有那么高。
百度移动端是另外一个 API ，搜狗，360，Google也有不同的API，可以作为扩展方式。


不用登陆
http://index.baidu.com/api/WordGraph/multi?wordlist%5B%5D=keyword

需要登陆
http://index.baidu.com/api/SearchApi/index?area=0&word=[[%7B%22name%22:%22keyword%22,%22wordType%22:1%7D]]&days=30


"""


def getMoreWord(keywords, filter_word, save_kw_file_path):
    """
    获取百度下拉框推荐关键词的方法一：
    :param keyword: 获取下拉框推荐的关键词
    :return: 返回推荐关键词数组
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (compatible;Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

    print("保存文件地址:\t" + save_kw_file_path + "\n")
    temp = set()  # 保存下拉框关键词的集合
    for keyword in keywords:
        temp.add(keyword)
        try:
            sugg_url = "http://index.baidu.com/api/WordGraph/multi?wordlist%5B%5D={}".format(keyword)
            resp = requests.get(sugg_url, verify=False, headers=headers)
            content = resp.content.decode('unicode_escape')
            content = json.loads(content)
            content_list = content['data']['wordlist']
            sugg_arr = content_list[0]['wordGraph']
            if sugg_arr:
                for text in sugg_arr:
                    text = text['word']
                    text = text.strip()
                    # 过滤关键词
                    for word in filter_word:
                        if isinstance(word, str):
                            if word.lower() in text.lower():
                                temp.add(text)
                        else:
                            w0 = word[0]
                            w1 = word[1]
                            w2 = word[2]
                            w3 = word[3]
                            w4 = word[4]
                            if (w0 in text) and (w1 in text) and (w2 in text) and (w3 in text) and (w4 in text):
                                temp.add(text)
            else:
                print(keyword + " ------> 没有抓取到下拉框关键词！ \n")
        except Exception as  e:
            pass
        time.sleep(1)
    if len(temp):
        temp_list = list(temp)
        temp_list.sort()
        temp_str = "\n".join(temp_list)
        with open(save_kw_file_path, 'a+', encoding='UTF-8') as savef:
            savef.write(temp_str)


if __name__ == '__main__':
    """
    应该在采集完成之后，再进行过滤
    """
    keyword_dir = "证件照"  # 要采集的关键词目录名称
    filter_word = [
        # 子列表最多五个元素
        # 元素为字符串或者字符串数组
        # 如果子列表元素的数量修改了，
        # 则主代码里面的元素个数也需要修改
        ['证照', '', '', '', ''],
        ['件照', '', '', '', ''],
        ['寸照', '', '', '', ''],
        ['装照', '', '', '', ''],
    ]
    keyword_arr = ["证件照"]

    level_number = 30  # 需要循环采集几层

    keyword_path = "D:/WorkSpace/数据采集/百度指数相关词/" + keyword_dir + "/"
    if not os.path.exists(keyword_path):
        os.makedirs(keyword_path)
    for i in range(1, level_number + 1):
        lines = []
        if i == 1:
            lines = keyword_arr
        else:
            file_path = keyword_path + str(i - 1) + '.txt'
            gfr = generator_file_arr(file_path, 20000)
            for keyword_list in gfr:
                for keyword in keyword_list:
                    if keyword in lines:
                        continue
                    else:
                        lines.append(keyword)
        if lines:
            save_kw_file_path = keyword_path + str(i) + '.txt'
            getMoreWord(lines, filter_word, save_kw_file_path)
