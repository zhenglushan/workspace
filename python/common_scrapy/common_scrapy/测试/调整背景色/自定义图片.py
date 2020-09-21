# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 自定义图片.py
# @DATETime   : 2020/5/18 16:57
# @Author     : 笑看风云


import cv2
import numpy as np

# 参考地址 https://www.cnblogs.com/mjk961/p/9129211.html

# 构建一张图
img = np.zeros([512, 512, 3], dtype=np.uint8)

# 遍历每个像素点，并进行赋值
for i in range(512):
    for j in range(512):
        img[i, j, :] = [i % 256, j % 256, (i + j) % 256]

# 展示图片
cv2.namedWindow('custom image', cv2.WINDOW_NORMAL)
cv2.imshow('custom image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
