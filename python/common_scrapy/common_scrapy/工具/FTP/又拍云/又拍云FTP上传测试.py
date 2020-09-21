# -*- coding:utf-8 -*-

import upyun
from upyun import FileStore
from upyun import print_reporter

############### 又拍云存储 ###############
# 又拍云存储 https://console.upyun.com/services/file/

# https://help.upyun.com/knowledge-base/tools-storage-process-sdk/
# https://github.com/upyun/python-sdk

# FTP/FTPS 登录方式
# http://docs.upyun.com/api/developer_tools/#ftpftps

############### 腾讯云 CDN ###############
# 腾讯云加速怎么用，腾讯云CDN接入教程
# https://cloud.tencent.com/developer/article/1419979
up = upyun.UpYun('img-up-hncg', 'lhx4xmupy', '6WQH73rdWIVJ732psGD3o4V4kl4pn1MO', timeout=30, endpoint=upyun.ED_AUTO)

with open('D:/WorkSpace/Python/0df431adcbef76099264a322502dadc97dd99e11.jpeg', 'rb') as f:
    result = up.put('/uploads/allimg/2019/7/1/2cbc5dd9cdc5d506daab64d36b662e09.jpeg', f, checksum=True,
                    need_resume=True, headers={'X-Upyun-Multi-Type': 'image/png'},
                    store=FileStore(), reporter=print_reporter)
    print(result)
