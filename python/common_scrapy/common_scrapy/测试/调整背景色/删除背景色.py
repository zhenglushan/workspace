# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 删除背景色.py
# @DATETime   : 2020/5/18 16:05
# @Author     : 笑看风云

from PIL import Image

img = Image.open(r"C:/Users/Administrator/Desktop/20181210-103341-LiVtU.png")

img = img.convert("RGBA")  # 转换获取信息

pixdata = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pixdata[x, y][0] > 220 and pixdata[x, y][1] > 220 and pixdata[x, y][2] > 220 and pixdata[x, y][3] > 220:
            pixdata[x, y] = (255, 255, 255, 0)

img.save(r"C:/Users/Administrator/Desktop/20181210-103341-LiVtU_2.png")

print("背景色删除完成！")
