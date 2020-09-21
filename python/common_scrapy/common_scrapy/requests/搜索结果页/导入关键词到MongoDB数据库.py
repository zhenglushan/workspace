# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 导入关键词到MongoDB数据库.py
# @DATETime   : 2020/5/19 10:53
# @Author     : 笑看风云


import os
from common_scrapy.工具.通用.方法库 import generator_file
from common_scrapy.工具.通用.数据库 import get_MongoDB_DataBase

if __name__ == '__main__':
    # 获取 MongoDB 数据库对象
    database = get_MongoDB_DataBase()

    # 把关键词导入到数据库
    base_dir = "D:/WorkSpace/Python/ScrapyMongoDBForSearchKeywordFiles/2_拆分指数"
    cate_dirs = os.listdir(base_dir)
    if cate_dirs:
        for cate_dir_name in cate_dirs:
            cate_dir_name = cate_dir_name.strip()
            cate_dir = base_dir + "/" + cate_dir_name
            kw_files = os.listdir(cate_dir)
            for kw_file in kw_files:
                kw_file = kw_file.strip()
                kw_name = kw_file.replace(".txt", "")
                coll_name = cate_dir_name + "_" + kw_name
                coll_name = coll_name.lower()  # 集合名称
                kw_file_path = cate_dir + "/" + kw_file  # 关键词文件路径
                collcetion_list = database.list_collection_names()
                if coll_name not in collcetion_list:
                    # 判断集合是否已存在
                    # https://www.runoob.com/python3/python-mongodb.html
                    collcetion = database[coll_name]
                    # 大型文件读取器
                    gen = generator_file(kw_file_path)
                    keyword_arr = []
                    for keyword_list in gen:
                        for keyword in keyword_list:
                            keyword_arr.append(keyword.lower())
                        # db.getCollection('集合').count() MongoDB 客户端查询记录总数
                        # db.getCollection('集合').find({"_id":ObjectId("5dae747df263ead8f9ae8699")}) 根据 _id 的值查询
                        keyword_data = ({'keyword': kw} for kw in keyword_arr)
                        collcetion.insert_many(keyword_data, ordered=False, bypass_document_validation=True)
                        keyword_arr = []
                    # 查询 关键词 字段不为空的所有记录条数
                    print(coll_name + " 共导入 " + str(collcetion.count_documents({'keyword': {'$ne': None}})) + " 条数据")
                else:
                    print(coll_name + " 集合已存在！不再重复导入！")
