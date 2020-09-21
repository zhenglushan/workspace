# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : pc_end.py
# @DATETime   : 2020/3/3 16:40
# @Author     : 笑看风云


import re, requests, json
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
            # 获取模板、专题、文章每种类型的第一张网站地图
            index_second_arr_count = len(index_second_arr) - 26
            index_second_arr = index_second_arr[-index_second_arr_count:-index_second_arr_count + 1]
            if index_second_arr:
                for index_second_url in index_second_arr:
                    content_third = requests.get(index_second_url).text
                    result_third = re.findall(pattern, content_third, flags=re.I | re.S)
                    result_urls = result_urls + result_third
        else:
            result_sec = re.findall(pattern, content_second, flags=re.I | re.S)
            if result_sec:
                result_urls = result_urls + result_sec

avg_num = 1500

urls_res_arr = arr_size(result_urls, avg_num)

week_conf = {
    'site': 'www.gaoding.com',
    'token': 'ZTrx6cSp619A0SYM'
}
postUrl = 'http://data.zz.baidu.com/urls?site={}&token={}'

headers = {'Content-Type': 'text/plain'}
postUrl = postUrl.format(week_conf['site'], week_conf['token'])
if urls_res_arr:
    for urls in urls_res_arr:
        print(urls)
        result = requests.post(postUrl, data="\n".join(urls), headers=headers)
        reText = result.text
        if 'error' in reText:
            if 'site error' in reText:
                print("站点未在站长平台验证")
            elif 'empty content' in reText:
                print("post内容为空")
            elif 'only 2000 urls are allowed once' in reText:
                print("每次最多只能提交2000条链接")
            elif 'over quota' in reText:
                print("超过每日配额了，超配额后再提交都是无效的")
            elif 'token is not valid' in reText:
                print("token错误")
            elif 'not found' in reText:
                print("接口地址填写错误")
            elif 'internal error, please try later' in reText:
                print("服务器偶然异常，通常重试就会成功")
            break
        else:
            print(reText)
            jsonStr = json.loads(reText)
            remain = jsonStr['remain']
            success = jsonStr['success']
            if remain < avg_num:
                break
        print('---------------------------------------------------------')
