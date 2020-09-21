# -*- coding:utf-8 -*-

from scrapy_mongodb_for_search.my_tools.database.mongodb import get_MongoDB_DataBase

mg_database = get_MongoDB_DataBase()

"""
显示所有 collection 集合的名称
"""
# print(mg_database.list_collection_names())

"""
collection 集合的相关操作，以 伴游_伴游长尾词 为例
"""
collec_name = "伴游_伴游长尾词"  # 集合的名称
mg_collec = mg_database[collec_name]
doc_part = mg_collec.aggregate([
    {'$match': {'bd_body': {'$exists': True}, 'bd_title': {'$exists': True}}},
    {'$sample': {'size': 10}}
])
for doc in doc_part:
    keyword = doc['keyword'].strip()
    bd_title = doc['bd_title'].strip()
    bd_body = doc['bd_body'].strip()
    print(keyword + "~~~~~~" + bd_title[0:20] + "~~~~~~" + bd_body[0:20])
