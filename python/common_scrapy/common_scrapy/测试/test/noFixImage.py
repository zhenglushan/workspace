# -*- coding:utf-8 -*-

import requests

def get_baidu_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
    }
    return headers

def getImageFix(img_src):
    headers = get_baidu_headers()
    req = requests.get(img_src, headers=headers)
    print(req.headers['Content-Type'])
    print(req.content)


img_src = 'https://static.52z.com/2015images/2015logo.png'
img_src = 'https://img.52z.com/upload/5/37faf29d32b7f3d34070481749fa07fd_600_340.jpg'
getImageFix(img_src)





