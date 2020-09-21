# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 配资.py
# @DATETime   : 2020-04-30 上午 10:19
# @Author     : 笑看风云

import random


def piece_together_keywor():
    """
    组合关键词
    :return:
    """
    p1 = []
    save_file = "../../my_files/组合关键词/配资.txt"
    new_arr = []
    with open("../../my_files/project_files/2020年2月县级以上行政.txt", mode="r", encoding="UTF-8") as p1fr:
        for line in p1fr:
            p1.append(line.strip())
    p2 = ["股票公司", "证券公司", "期货公司", "股票开户", "证券开户", "期货开户", "期货配资", "配资平台"]
    p3 = ["哪家", "哪些", "有哪家", "有哪些"]
    p4 = ["正规股票公司", "正规证券公司", "正规期货公司", "正规股票开户", "正规证券开户", "正规期货开户", "正规期货配资", "正规配资平台"]
    p5 = ["服务好", "比较好", "比较安全", "佣金低", "服务正规", "是正规的", "可以开户", "手续费低", "安全可靠", "口碑好", "实力雄厚", "资金雄厚", "最可靠"]

    for k1 in p1:
        for k2 in p2:
            for k3 in p3:
                for k4 in p4:
                    for k5 in p5:
                        title = k1 + k2 + k3 + k4 + k5
                        print(title)
                        new_arr.append(title)
    random.shuffle(new_arr)
    with open(save_file, mode="w", encoding="UTF-8") as kwr:
        kwr.write("\n".join(new_arr))


if __name__ == "__main__":
    piece_together_keywor()
