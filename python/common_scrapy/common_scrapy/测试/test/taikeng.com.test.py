# -*- coding:utf-8 -*-

import requests

kv = {"User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"}
r = requests.get('http://taikeng.com/peizizixun/list_1_3.html', headers=kv, allow_redirects=False)
location = r.headers['Location']
print(r.status_code)

print(r.cookies)
print(r.url)

print(r.cookies['__cdnuid'])
cookies = {'__cdnuid': r.cookies['__cdnuid']}


print(r.headers)
print(r.text)
print('hehe')
