# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : week_post.py
# @DATETime   : 2020/3/3 16:31
# @Author     : 笑看风云

import re, requests
from ScrapyMongoDBForSearch.工具.通用工具 import arr_size

# 网站地图抽取提交地址
# 稿定设计 PC 端网站地图: https://www.gaoding.com/api/sitemap.xml
result_urls = []  # 稿定设计网站地图提取结果数组
webpage = 'https://www.gaoding.com/api/sitemap.xml'
content_first = requests.get(webpage).text
pattern = '<loc>(.*?)<\/loc>'  # 匹配的正则表达式
sm_index_file_arr = re.findall(pattern, content_first, flags=re.I | re.S)
if sm_index_file_arr:
    for index_url in sm_index_file_arr:
        content_second = requests.get(index_url).text
        if ('.xml' in content_second):
            # 继续提取索引文件里面的地址
            index_second_arr = re.findall(pattern, content_second, flags=re.I | re.S)
            if index_second_arr:
                for index_second_url in index_second_arr:
                    content_third = requests.get(index_second_url).text
                    result_third = re.findall(pattern, content_third, flags=re.I | re.S)
                    result_urls = result_urls + result_third
        else:
            result_sec = re.findall(pattern, content_second, flags=re.I | re.S)
            if result_sec:
                result_urls = result_urls + result_sec

# 稿定设计 M 端网站地图: https://m.gaoding.com/api/sitemap.xml
webpage = 'https://m.gaoding.com/api/sitemap.xml'
pattern = '<loc>(.*?)<\/loc>'  # 匹配的正则表达式
content_first = requests.get(webpage).text
sm_index_file_arr = re.findall(pattern, content_first, flags=re.I | re.S)
if sm_index_file_arr:
    for index_url in sm_index_file_arr:
        content_second = requests.get(index_url).text
        if ('.xml' in content_second):
            # 继续提取索引文件里面的地址
            index_second_arr = re.findall(pattern, content_second, flags=re.I | re.S)
            if index_second_arr:
                for index_second_url in index_second_arr:
                    content_third = requests.get(index_second_url).text
                    result_third = re.findall(pattern, content_third, flags=re.I | re.S)
                    result_urls = result_urls + result_third
        else:
            result_sec = re.findall(pattern, content_second, flags=re.I | re.S)
            if result_sec:
                result_urls = result_urls + result_sec

# 标签系统网站地图: https://t.gaoding.com/sitemap/detail-1.xml
webpage = 'https://t.gaoding.com/sitemap/detail-1.xml'
pattern = 'https:\/\/t\.gaoding\.com\/muban\/[\d]+\.html'
content_first = requests.get(webpage).text
tag_urls = re.findall(pattern, content_first, flags=re.I | re.S)
urls_res = result_urls
if tag_urls:
    urls_res = urls_res + tag_urls

# 由于每次最多只能提交 2000 条 url 地址，
# 所以需要对 url 地址按 1500 条来分组，

urls_res_arr = arr_size(urls_res, 1500)

# https://ziyuan.baidu.com/ydzq/includeweek?officeId=1625859537941985
# 示例提交地址
# $urls = array(
# 	'https://www.gaoding.com/topic/4490',
# 	'https://www.gaoding.com/topic/4496',
# 	'https://www.gaoding.com/topic/4491',
# 	'https://www.gaoding.com/topic/4504',
# )

week_conf = {
    'appid': '1625859537941985',
    'token': '9qZlalUxq7SxmlVh',
    'type': 'batch'
}
api = 'http://data.zz.baidu.com/urls?appid={}&token={}&type={}'

# 天级收录 api:
# http://data.zz.baidu.com/urls?appid=1625859537941985&token=9qZlalUxq7SxmlVh&type=realtime
headers = {'Content-Type': 'text/plain'}
api = api.format(week_conf['appid'], week_conf['token'], week_conf['type'])
if urls_res_arr:
    for urls in urls_res_arr:
        print(urls)
        result = requests.post(api, data="\n".join(urls), headers=headers)
        print(result.text)
        print('---------------------------------------------------------')

# result_urls = "\n".join(result_urls)
# with open("C:/Users/Administrator/Desktop/result.txt", "a") as fxml:
#     fxml.writelines(result_urls)
