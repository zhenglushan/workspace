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
"""


def getMoreWord(keyword):
    """
    :param keyword: 关键词
    :return: 返回拓展关键词数组
    """
    all_words = []
    all_words.append(keyword)
    for i in 'abcdefghijklmnopqrstuvwxyz':
        '''
        在关键词后面输入 w，会出现跟拼音以 w 开头的一系列关键词，
        比如“黄山w”，会出现“黄山温泉”，”黄山玩几天“，“黄山五绝”等关键词（见上截图）。
        因此，当我们把 a~z 遍历一遍，会出现更多关键词。
        '''
        # all_words.append(keyword + i)
        pass
        for j in 'abcdefghijklmnopqrstuvwxyz':
            '''
            将上面的思路延展一下，如果在关键词后输入两个单词，就会出现以这 2 个字母为拼音开头的一系列关键词，
            比如“黄山tp”，会出现“黄山天气”，“黄山太平湖”。
            '''
            # all_words.append(keyword + i + j)
            pass
    return all_words


def getBaiduSuggestion_2(keyword):
    """
    获取百度下拉框推荐关键词的方法二：
    :param keyword: 获取下拉框推荐的关键词
    :return: 返回推荐关键词数组
    """
    sugg_url = "http://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd={}&sugmode=3&json=1".format(keyword)
    resp = requests.get(sugg_url, verify=False)
    content = resp.content
    content = content[17:-1].decode('gbk')
    json_text = json.loads(content)
    sugg_arr = json_text['s']
    if sugg_arr:
        print(keyword + " ++++++> " + ','.join(sugg_arr))
    else:
        print(keyword + " ------> 没有抓取到下拉框关键词！ ")
        sugg_arr = []
    return sugg_arr


def getBaiduSuggestion_1(keywords, filter_word, save_kw_file_path):
    """
    获取百度下拉框推荐关键词的方法一：
    :param keyword: 获取下拉框推荐的关键词
    :return: 返回推荐关键词数组
    """
    print("保存文件地址:\t" + save_kw_file_path + "\n")
    temp = set()  # 保存下拉框关键词的集合
    for keyword in keywords:
        sugg_url = "http://suggestion.baidu.com/su?wd={}&sugmode=3&json=1".format(keyword)
        resp = requests.get(sugg_url, verify=False)
        content = resp.content
        content = content[17:-2].decode('gbk')
        temp.add(keyword)
        try:
            json_text = json.loads(content)
            sugg_arr = json_text['s']
            if sugg_arr:
                print(keyword + " ++++++> " + ','.join(sugg_arr))
                for text in sugg_arr:
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
    print("\n")


if __name__ == '__main__':
    """
    应该在采集完成之后，再进行过滤
    """
    keyword_dir = "七夕节图片"  # 要采集的关键词目录名称
    filter_word = [
        # 子列表最多五个元素
        # 元素为字符串或者字符串数组
        # 如果子列表元素的数量修改了，
        # 则主代码里面的元素个数也需要修改
        ['七夕', '图片', '', '', ''],
        ['七夕', '海报', '', '', ''],
        ['七夕', '封面', '', '', ''],
        ['七夕', '素材', '', '', '']
    ]
    keyword_arr = ["七夕节图片", "七夕节海报", "七夕节封面", "七夕节素材", "七夕图片", "七夕海报", "七夕封面", "七夕素材"]

    level_number = 30  # 需要循环采集几层

    keyword_path = "D:/WorkSpace/数据采集/百度相关搜索/" + keyword_dir + "/"
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
            getBaiduSuggestion_1(lines, filter_word, save_kw_file_path)
