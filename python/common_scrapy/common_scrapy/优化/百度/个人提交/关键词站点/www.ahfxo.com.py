# -*- coding:utf-8 -*-
# @ProjectName: ForCompany
# @Email	  : 276517382@qq.com
# @FileName   : www.ahfxo.com.py
# @DATETime   : 2019/12/6 16:25
# @Author     : 笑看风云

import re, requests, json
from ScrapyMongoDBForSearch.工具.通用工具 import arr_size
from time import sleep

# 需求修改的内容
webpage = 'http://www.ahfxo.com/sitemap.xml'
week_conf = {
    'site': 'www.ahfxo.com',
    'token': '9uon0sDXlbeuDc6e'
}

# 下面的内容不需要修改
## 请求头信息
postUrl = 'http://data.zz.baidu.com/urls?site={}&token={}'
headers = {'Content-Type': 'text/plain'}
postUrl = postUrl.format(week_conf['site'], week_conf['token'])
## 采集具体网址代码
content = requests.get(webpage).text
pattern = '<loc>(.*?)<\/loc>'  # 匹配的正则表达式
xml_urls = re.findall(pattern, content, flags=re.I | re.S)
if xml_urls:
    xml_urls = xml_urls[:3]  # 只推送最新的 3 个 XML 文件
    is_break_out = False
    for xml_url in xml_urls:
        url_content = requests.get(xml_url).text
        con_urls = re.findall(pattern, url_content, flags=re.I | re.S)
        if con_urls:
            avg_num = 1000
            urls_res_arr = arr_size(con_urls, avg_num)
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
                    if remain < avg_num:
                        is_break_out = True
                        break
                print('---------------------------------------------------------')
            sleep(3)
        if is_break_out:
            break
