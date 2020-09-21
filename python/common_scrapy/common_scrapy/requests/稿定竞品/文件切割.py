# from scrapy_mongodb_for_search.my_tools.common import list_split
#
# if __name__ == "__main__":
#     save_dir = "D:/WorkSpace/company_work/稿定设计/关键词过滤和导入/"
#     save_result_keyword_path = "D:/WorkSpace/company_work/稿定设计/关键词过滤和导入/1-save-keywords.txt"
#
#     keyword_arr = []
#     with open(save_result_keyword_path, mode="r", encoding="utf8") as readf:
#         for line in readf.readlines():
#             line = line.strip()
#             keyword_arr.append(line)
#
#     new_keyword_arr = list_split(keyword_arr, 300371)
#
#     for id, value in enumerate(new_keyword_arr):
#         file_id = id + 1
#         file_name = "new_file_" + str(file_id) + ".txt"
#         with open(save_dir + file_name, 'w', encoding='utf-8') as w:
#             w.write("\n".join(value))
