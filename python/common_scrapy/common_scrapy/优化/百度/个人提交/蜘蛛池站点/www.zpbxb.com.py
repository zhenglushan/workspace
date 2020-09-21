# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : WeekPost.py
# @DATETime   : 2019/12/2 10:46
# @Author     : 笑看风云

import re, requests, json
from time import sleep
from ScrapyMongoDBForSearch.工具.通用工具 import arr_size

webpage = 'http://www.zpbxb.com/sitemap.xml'
week_conf = {
    'site': 'www.zpbxb.com',
    'token': '9uon0sDXlbeuDc6e'
}
is_break_out = False
postUrl = 'http://data.zz.baidu.com/urls?site={}&token={}'

headers = {'Content-Type': 'text/plain'}
postUrl = postUrl.format(week_conf['site'], week_conf['token'])
for _ in range(20):
    result_urls = []
    content_first = requests.get(webpage).text
    pattern = '<loc>(.*?)<\/loc>'  # 匹配的正则表达式
    tag_urls = re.findall(pattern, content_first, flags=re.I | re.S)
    if tag_urls:
        result_urls = result_urls + tag_urls
    avg_num = 1500
    urls_res_arr = arr_size(result_urls, avg_num)
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
                is_break_out = True
                break
            else:
                print(reText)
                jsonStr = json.loads(reText)
                remain = jsonStr['remain']
                success = jsonStr['success']
                if remain < 500:  # 因为每次提交都是固定的 500 条
                    is_break_out = True
                    break
            print('---------------------------------------------------------')
            sleep(3)
    sleep(3)
    if is_break_out:
        break
