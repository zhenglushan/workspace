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
# # 用于过滤词库的词根
# ci_gen_file_path = "D:/WorkSpace/company_work/稿定设计/关键词过滤和导入/1-电商-教育培训-日历词根.txt"
# # 需要过滤的图怪兽词库
# filter_keyword_file_path = "D:/WorkSpace/company_work/稿定设计/关键词过滤和导入/818ps_keywords.txt"
# # 保存过滤出来的关键词
# save_result_keyword_path = "D:/WorkSpace/company_work/稿定设计/关键词过滤和导入/1-save-keywords.txt"
# # 保存没有过滤出来的、剩余的关键词
# shengyu_keyword_file_path = "D:/WorkSpace/company_work/稿定设计/关键词过滤和导入/shengyu_818ps_keywords.txt"
#
# ci_gen_arr = []
# with open(ci_gen_file_path, mode="r", encoding="utf8") as readf:
#     for line in readf.readlines():
#         line = line.strip()
#         ci_gen_arr.append(line)
# # print(ci_gen_arr)
#
# filter_keyword_file = generator_file_one(filter_keyword_file_path)
#
# # 根据词根过滤关键词
# with open(save_result_keyword_path, mode="+a", encoding="utf8") as fwsrkp:
#     with open(shengyu_keyword_file_path, mode="+a", encoding="utf8") as fwskfp:
#         for keyword in filter_keyword_file:
#             keyword = strQ2B(keyword)  # 把全角字符转换成半角字符
#             if "http:" in keyword or "https:" in keyword or "32O5444888" in keyword or len(keyword) >= 20:
#                 continue
#             else:
#                 # 提取字符串中的字母、数字、汉字
#                 keyword = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", keyword)
#                 keyword = keyword.strip()
#                 if keyword:
#                     keyword = keyword.replace("2018", "2020").replace("2019", "2020")
#                     # 判断 keyword 是否包含 ci_gen_arr 数组中的某些子串
#                     matches = [(word) for word in ci_gen_arr if word.lower() in keyword.lower()]
#                     if len(matches) > 0:
#                         print("把\t" + keyword + "\t保存到\t++++++\t过滤出来的关键词文件")
#                         fwsrkp.write(keyword + "\n")
#                     else:
#                         print("把\t" + keyword + "\t保存到\t------\t没有过滤出来的、剩余的关键词文件")
#                         fwskfp.write(keyword + "\n")
#
# print("暂停 3 秒钟")
# time.sleep(3)
#
# print("下面开始去重操作")
# qu_chong_arr = []
# with open(save_result_keyword_path, mode="r", encoding="utf8") as readf:
#     for line in readf.readlines():
#         line = line.strip()
#         qu_chong_arr.append(line)
#
# qu_chong_arr = list(set(qu_chong_arr))
# qu_chong_arr.sort()
# with open(save_result_keyword_path, mode="w", encoding="utf8") as writef:
#     qu_chong_arr = "\n".join(qu_chong_arr)
#     writef.write(qu_chong_arr)
#
# # 手工删除黄赌毒相关词
