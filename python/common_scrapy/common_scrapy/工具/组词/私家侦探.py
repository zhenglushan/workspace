# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 私家侦探.py
# @DATETime   : 2020-04-30 上午 11:12
# @Author     : 笑看风云


import random


def piece_together_keywor():
    """
    组合关键词

    "多少","怎么","哪家","哪里","吗"
    在使用组合关键词时，需要判断是否包含如上字符串，
    如果有则需要加上问号，且整个作为标题使用；
    如果没有，则作为关键词和分隔符和其它截取的字符串作为标题使用；

    :return:
    """
    p1 = []
    save_file = "../../my_files/组合关键词/私家侦探.txt"
    new_arr = []
    with open("../../my_files/project_files/2020年2月县级以上行政.txt", mode="r", encoding="UTF-8") as p1fr:
        for line in p1fr:
            p1.append(line.strip())
    p2 = ["私家侦探", "私家侦探公司", "私家侦探调查公司", "私家侦探", "私人侦探", "私人侦探公司", "私人侦探调查公司", "私人侦探"]
    p3 = ["价格", "价格是多少", "取证", "哪家好", "哪家靠谱", "哪里找", "哪里有", "器材", "多少钱", "婚姻调查", "怎么找", "怎么收费", "找人多少钱", "找人怎么收费","找人费用是多少", "招聘", "收费", "收费标准", "服务", "电话", "私人调查", "联系方式", "调查", "费用", "靠谱吗"]

    for k1 in p1:
        for k2 in p2:
            for k3 in p3:
                title = k1 + k2 + k3
                print(title)
                new_arr.append(title)
    random.shuffle(new_arr)
    with open(save_file, mode="w", encoding="UTF-8") as kwr:
        kwr.write("\n".join(new_arr))


if __name__ == "__main__":
    piece_together_keywor()
