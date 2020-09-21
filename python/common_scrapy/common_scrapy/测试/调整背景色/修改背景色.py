# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 修改背景色.py
# @DATETime   : 2020/5/18 16:04
# @Author     : 笑看风云

import cv2
import numpy as np

img_path = "C:/Users/Administrator/Desktop/timg.jpg"

img = cv2.imread(img_path)
# 缩放
rows, cols, channels = img.shape
img = cv2.resize(img, None, fx=0.5, fy=0.5)
rows, cols, channels = img.shape
cv2.imshow('img', img)

# 转换hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 70, 70])  # 该三个数值可以控制好处理出来的效果和噪点
upper_blue = np.array([110, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow('Mask', mask)

# 腐蚀膨胀
erode = cv2.erode(mask, None, iterations=1)
cv2.imshow('erode', erode)
dilate = cv2.dilate(erode, None, iterations=1)
cv2.imshow('dilate', dilate)

# 遍历替换
for i in range(rows):
    for j in range(cols):
        if dilate[i, j] == 255:
            img[i, j] = (0, 0, 255)  # 此处替换颜色，为BGR通道
cv2.imshow('res', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
