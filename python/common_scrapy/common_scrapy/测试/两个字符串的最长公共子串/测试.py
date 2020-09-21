# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 测试.py
# @DATETime   : 2020/5/19 9:49
# @Author     : 笑看风云

from ScrapyMongoDBForSearch.测试.两个字符串的最长公共子串.两个字符串的最长公共子串 import getLongestCommonSubStr

if __name__ == '__main__':
    # 匹配 title 中的内容
    with open("./one.txt", mode="r", encoding="UTF-8") as onef:
        one_part = onef.read()

    # 匹配 body 中的内容
    with open("./two.txt", mode="r", encoding="UTF-8") as onef:
        two_part = onef.read()

    # 求两个字符串的最长公共子串
    one, two = getLongestCommonSubStr(one_part, two_part)
    print("最长公共子串为：" + one)
    print("其长度为：" + str(two))
    print("len() 的长度为：" + str(len(one)))
