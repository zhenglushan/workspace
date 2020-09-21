# -*- coding:utf-8 -*-
# @ProjectName: PyCompany
# @Email	  : 276517382@qq.com
# @FileName   : BaiduSuggestion.py
# @DATETime   : 2019/12/18 13:39
# @Author     : 笑看风云

import requests, json, time, os
from scrapy_mongodb_for_search.my_tools.common import generator_file_arr

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
    for i in 'abcdef':
        '''
        在关键词后面输入 w，会出现跟拼音以 w 开头的一系列关键词，
        比如“黄山w”，会出现“黄山温泉”，”黄山玩几天“，“黄山五绝”等关键词（见上截图）。
        因此，当我们把 a~z 遍历一遍，会出现更多关键词。
        '''
        all_words.append(keyword + i)
        for j in 'ab':
            '''
            将上面的思路延展一下，如果在关键词后输入两个单词，就会出现以这 2 个字母为拼音开头的一系列关键词，
            比如“黄山tp”，会出现“黄山天气”，“黄山太平湖”。
            '''
            all_words.append(keyword + i + j)
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


def getBaiduSuggestion_1(keyword):
    """
    获取百度下拉框推荐关键词的方法一：
    :param keyword: 获取下拉框推荐的关键词
    :return: 返回推荐关键词数组
    """
    sugg_url = "http://suggestion.baidu.com/su?wd={}&sugmode=3&json=1".format(keyword)
    resp = requests.get(sugg_url, verify=False)
    content = resp.content
    content = content[17:-2].decode('gbk')
    json_text = json.loads(content)
    sugg_arr = json_text['s']
    if sugg_arr:
        print(keyword + " ++++++> " + ','.join(sugg_arr))
    else:
        print(keyword + " ------> 没有抓取到下拉框关键词！ ")
        sugg_arr = []
    return sugg_arr


def return_scan_dirs(base_dir, include_keywords, not_include_keywords):
    """
    include_keywords 和 not_include_keywords 最多只能配置其中一个
    如果两个都配置了，则把 include_keywords 设置为空
    """
    scan_dirs = []
    if not_include_keywords or include_keywords:
        if not_include_keywords:
            include_keywords = []
            for root, sub_dirs, files in os.walk(base_dir):
                for sub_dir in sub_dirs:
                    if sub_dir not in not_include_keywords:
                        sub_dir_path = base_dir + sub_dir + "/"
                        scan_dirs.append(sub_dir_path)
        if include_keywords:
            for keyword in include_keywords:
                temp_path = base_dir + keyword + "/"
                scan_dirs.append(temp_path)
    else:
        for root, sub_dirs, files in os.walk(base_dir):
            for sub_dir in sub_dirs:
                sub_dir_path = base_dir + sub_dir + "/"
                scan_dirs.append(sub_dir_path)
    return scan_dirs


if __name__ == '__main__':
    base_dir = "./关键字/"
    include_keywords = ["元宵", "大年初一", "拜年", "春节", "正月十五", "贺年", "贺新春", "鼠年"]
    not_include_keywords = ["年终总结", "情人节", "拼图"]
    scan_dirs = return_scan_dirs(base_dir, include_keywords, not_include_keywords)

    level_number = 30  # 需要循环采集几层
    start = 1  # 从 1 开始
    for current_i in range(start, level_number + 1):
        for scan_dir in scan_dirs:
            next_i = current_i + 1
            read_file_path = scan_dir + str(current_i) + '.txt'
            write_file_path = scan_dir + str(next_i) + '.txt'
            print(read_file_path)
            lines = []
            gfr = generator_file_arr(read_file_path, 20000)
            for keyword_list in gfr:
                for keyword in keyword_list:
                    keyword = keyword.strip()
                    if keyword:
                        if keyword in lines:
                            continue
                        else:
                            lines.append(keyword)
            if lines:
                for line in lines:
                    all_word = []
                    words = getMoreWord(line)
                    for word in words:
                        temp = getBaiduSuggestion_1(word)
                        if temp:
                            for ever in temp:
                                all_word.append(ever)
                        time.sleep(0.2)
                    if all_word:
                        all_word = list(set(all_word))
                        print(all_word)
                        all_word = "\n".join(all_word) + "\n"
                        with open(write_file_path, 'a+', encoding='UTF-8') as fw:
                            fw.write(all_word)
