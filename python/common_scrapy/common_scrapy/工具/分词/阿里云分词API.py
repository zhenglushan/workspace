# -*- coding:utf-8 -*-
'''
https://market.aliyun.com/products/57124001/cmapi033005.html
'''

from urllib import request
from urllib import parse
from urllib.request import urlopen

host = 'http://lexical.market.alicloudapi.com'
path = '/zhongwenfenci'
method = 'POST'
appcode = '74d70f21545b41c4980591f299bd19db'
querys = ''
bodys = {}
url = host + path

bodys['in'] = '超漂亮的平面代言模特小欣'
post_data = parse.urlencode(bodys).encode('utf-8')

req = request.Request(url, data=post_data, method=method)
req.add_header('Authorization', 'APPCODE ' + appcode)
req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')

resp = urlopen(req)
content = resp.read().decode()
if (content):
    print(content)
