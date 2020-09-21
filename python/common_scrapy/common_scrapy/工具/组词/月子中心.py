# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 月子中心.py
# @DATETime   : 2020-04-30 下午 02:34
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
    save_file = "../../my_files/组合关键词/月子中心.txt"
    new_arr = []
    with open("../../my_files/project_files/2020年2月县级以上行政.txt", mode="r", encoding="UTF-8") as p1fr:
        for line in p1fr:
            p1.append(line.strip())
    p2 = ["专业月子中心", "产后月子中心", "加盟月子中心", "坐月子中心", "最好的月子中心", "月子中心", "月子中心一般多少钱", "月子中心价格", "月子中心会所", "月子中心加盟多少钱",
          "月子中心品牌", "月子中心哪家好", "月子中心哪家最好", "月子中心多少钱", "月子中心多少钱一个月", "月子中心如何", "月子中心怎么样", "月子中心怎样", "月子中心报价", "月子中心招聘",
          "月子中心排名", "月子中心排行榜", "月子中心收费", "月子中心服务", "月子中心服务项目", "月子中心要多少钱", "月子中心费用", "月子恢复中心", "月子护理中心", "直营月子中心",
          "高端月子中心"]

    for k1 in p1:
        for k2 in p2:
            title = k1 + k2
            print(title)
            new_arr.append(title)
    random.shuffle(new_arr)
    with open(save_file, mode="w", encoding="UTF-8") as kwr:
        kwr.write("\n".join(new_arr))


if __name__ == "__main__":
    piece_together_keywor()
