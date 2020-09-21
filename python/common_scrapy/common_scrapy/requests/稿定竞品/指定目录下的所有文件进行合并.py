# # -*- coding:utf-8 -*-
# # @ProjectName: flutter_lesson
# # @Email	  : 276517382@qq.com
# # @FileName   : 指定目录下的所有文件进行合并.py
# # @DATETime   : 2020/4/13 9:57
# # @Author     : 笑看风云
#
# import os
#
# if __name__ == "__main__":
#
#     files_path = "C:/Users/Administrator/Desktop/搜索关键词/"
#
#     new_file_path = "C:/Users/Administrator/Desktop/finally.txt"
#
#     list_files = os.listdir(files_path)
#
#     with open(new_file_path, 'a+', encoding='utf-8') as w:
#         for file in list_files:
#             file_path = files_path + file
#             with open(file_path, 'r', encoding='gbk') as f:
#                 txt_str = f.read().strip()
#                 print("正在读取合并的关键词为：\t" + txt_str)
#                 w.write(txt_str + "\n")
