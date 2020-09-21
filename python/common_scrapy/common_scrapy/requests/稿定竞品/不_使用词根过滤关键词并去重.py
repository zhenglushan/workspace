# # -*- coding:utf-8 -*-
# # @ProjectName: flutter_lesson
# # @Email	  : 276517382@qq.com
# # @FileName   : 使用词根过滤关键词.py
# # @DATETime   : 2020/4/1 11:21
# # @Author     : 笑看风云
# import re, time
#
#
# def strQ2B(ustring):
#     """全角转半角"""
#     rstring = ""
#     for uchar in ustring:
#         inside_code = ord(uchar)
#         if inside_code == 12288:  # 全角空格直接转换
#             inside_code = 32
#         elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
#             inside_code -= 65248
#         rstring += chr(inside_code)
#     return rstring
#
#
# def strB2Q(ustring):
#     """半角转全角"""
#     rstring = ""
#     for uchar in ustring:
#         inside_code = ord(uchar)
#         if inside_code == 32:  # 半角空格直接转化
#             inside_code = 12288
#         elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
#             inside_code += 65248
#         rstring += chr(inside_code)
#     return rstring
#
#
# def generator_file_one(filepath):
#     '''
#     读取大型文件，采用生成器的方式
#     :param filepath: 文本路径
#     :return i: 返回每行关键词
#     '''
#     with open(filepath, 'r', encoding='utf-8') as f:
#         for i in f:
#             i = i.replace("\r", '').replace("\n", '').strip()
#             if i:
#                 yield i
#
#
# # 需要过滤的图怪兽词库
# file_path = "C:/Users/Administrator/Desktop/finally.txt"
# # 保存过滤出来的关键词
# filter_file_path = "C:/Users/Administrator/Desktop/finally_filter.txt"
#
# filter_keyword_file = generator_file_one(file_path)
#
# qu_chong_arr = []
# with open(file_path, mode="r", encoding="utf8") as readf:
#     for line in readf.readlines():
#         line = line.strip()
#         if line:
#             line = line.lower()
#             line = strQ2B(line)  # 把全角字符转换成半角字符
#             # line = line.replace("2018", "2020").replace("2019", "2020")
#             qu_chong_arr.append(line)
#
# qu_chong_arr = list(set(qu_chong_arr))  # 先转成集合，再转成列表，达到去重目的
#
# qu_chong_arr.sort()
#
# with open(filter_file_path, mode="w", encoding="utf8") as writef:
#     qu_chong_arr = "\n".join(qu_chong_arr)
#     writef.write(qu_chong_arr)
