# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 夜场.py
# @DATETime   : 2020-04-30 下午 03:42
# @Author     : 笑看风云


import random


def piece_together_keywor():
    """
    组合关键词

    "多少","怎么","怎样","哪","吗"
    在使用组合关键词时，需要判断是否包含如上字符串，
    如果有则需要加上问号，且整个作为标题使用；
    如果没有，则作为关键词和分隔符和其它截取的字符串作为标题使用；

    :return:
    """
    p1 = []
    save_file = "../../my_files/组合关键词/夜场.txt"
    new_arr = []
    with open("../../my_files/project_files/2020年2月县级以上行政.txt", mode="r", encoding="UTF-8") as p1fr:
        for line in p1fr:
            p1.append(line.strip())
    p2 = ["夜场"]
    p3 = ["找工作", "工作", "兼职", "招聘", "招聘信息", "美女", "小姐", "模特", "公关", "男模", "女模", "KTV", "男公关", "女公关", "价格", "多少钱", "服务",
          "出台", "赚钱", "鸭子", "招工", "玩什么", "坐台", "招聘女", "妈咪"]

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
