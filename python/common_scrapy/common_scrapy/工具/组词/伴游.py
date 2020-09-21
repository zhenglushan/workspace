# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 伴游.py
# @DATETime   : 2020-04-30 下午 02:06
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
    save_file = "../../my_files/组合关键词/伴游.txt"
    new_arr = []
    with open("../../my_files/project_files/2020年2月县级以上行政.txt", mode="r", encoding="UTF-8") as p1fr:
        for line in p1fr:
            p1.append(line.strip())
    p2 = ["伴游交友", "伴游价格", "伴游价格表", "伴游信息", "伴游公司", "伴游天下", "伴游女生", "伴游小姐", "伴游招聘", "伴游最新招聘", "伴游服务", "伴游模特", "伴游网价格",
          "伴游网价格表", "伴游网站", "兼职伴游", "兼职陪游", "出国陪游", "哪里找伴游", "哪里有陪游", "商务伴游", "商务陪游", "大学生陪游", "女大学生陪游", "嫩模陪游", "当地陪游",
          "性伴游", "找个伴游", "找陪游多少钱", "找陪游女", "招聘陪游", "招聘陪游男", "极品伴游", "海外伴游", "男伴游", "男商务伴游", "男陪游", "私人伴游", "私人伴游招聘",
          "私人男伴游", "私人陪游", "私人陪游招聘", "网络陪游", "美女陪游", "美美伴游", "自驾游陪游", "陪床伴游", "陪游价格", "陪游保姆", "陪游公司", "陪游兼职", "陪游女",
          "陪游女价格表", "陪游女哪里找", "陪游女微信", "陪游妹子", "陪游小姐", "陪游平台", "陪游怎么找", "陪游招聘", "陪游服务", "陪游模特", "陪游男", "陪游网站", "陪玩陪游",
          "靠谱伴游", "高端伴游", "高端陪游", "高端陪游小姐", "高级伴游"]

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
