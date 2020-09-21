# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 两个字符串的最长公共子串.py
# @DATETime   : 2020/5/19 9:22
# @Author     : 笑看风云

"""
求两个字符串的最长公共子串
思想：建立一个二维数组，保存连续位相同与否的状态
参考：http://www.manongjc.com/article/3880.html
"""


def getLongestCommonSubStr(str1, str2):
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位
    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p], maxNum
