# -*- coding:utf-8 -*-
# @ProjectName: python-100-days
# @Email	  : 276517382@qq.com
# @FileName   : day_post.py
# @DATETime   : 2020/3/3 16:30
# @Author     : 笑看风云

import requests

'''
DayPostData.txt 文件中，一行对应一条 URL 地址
'''
with open('./天级提交数据.txt', 'r') as dpd:
    urls = [line.rstrip('\n') for line in dpd]

api = 'http://data.zz.baidu.com/urls?appid={}&token={}&type={}'
week_conf = {
    'appid': '1625859537941985',
    'token': '9qZlalUxq7SxmlVh',
    'type': 'realtime'
}
api = api.format(week_conf['appid'], week_conf['token'], week_conf['type'])

headers = {'Content-Type': 'text/plain'}

if urls:
    print(urls)
    result = requests.post(api, data="\n".join(urls), headers=headers)
    print(result.text)
    print('---------------------------------------------------------')
