# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 代孕.py
# @DATETime   : 2020-04-30 上午 11:40
# @Author     : 笑看风云


import random


def piece_together_keywor():
    """
    组合关键词
    代孕 助孕

    "多少","怎么","怎样","哪","吗"
    在使用组合关键词时，需要判断是否包含如上字符串，
    如果有则需要加上问号，且整个作为标题使用；
    如果没有，则作为关键词和分隔符和其它截取的字符串作为标题使用；

    :return:
    """
    p1 = []
    save_file = "../../my_files/组合关键词/代孕.txt"
    new_arr = []
    with open("../../my_files/project_files/2020年2月县级以上行政.txt", mode="r", encoding="UTF-8") as p1fr:
        for line in p1fr:
            p1.append(line.strip())
    p2 = ["代孕", "助孕", "借卵代孕"]
    p3 = ["网", "招聘", "电话", "服务", "价格", "费用", "中介", "过程", "公司", "产子", "产子价格", "产子公司", "供卵", "流程", "试管", "多少钱", "机构",
          "医院", "怎么怀孕", "中心", "试管婴儿", "案例", "包成功", "条件", "户口", "生孩子", "公司哪家好", "中介哪家好", "价格是多少", "费用怎么样", "电话是多少",
          "产子贵吗", "网哪家靠谱", "网哪个靠谱"]

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
