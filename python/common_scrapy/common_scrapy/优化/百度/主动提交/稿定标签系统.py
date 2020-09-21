# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : tag_end.py
# @DATETime   : 2020/3/3 16:41
# @Author     : 笑看风云


import re, requests, json
from ScrapyMongoDBForSearch.工具.通用工具 import arr_size

result_urls = []  # 稿定设计网站地图提取结果数组

# 标签系统网站地图: https://t.gaoding.com/sitemap/detail-1.xml
webpage = 'https://t.gaoding.com/sitemap/detail-1.xml'
pattern = 'https:\/\/t\.gaoding\.com\/muban\/[\d]+\.html'
content_first = requests.get(webpage).text
tag_urls = re.findall(pattern, content_first, flags=re.I | re.S)
urls_res = result_urls
if tag_urls:
    urls_res = urls_res + tag_urls

avg_num = 1500

urls_res_arr = arr_size(urls_res, avg_num)

week_conf = {
    'site': 'https://t.gaoding.com',
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
