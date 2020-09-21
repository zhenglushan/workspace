# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 打印MongoDB不符合条件的集合.py
# @DATETime   : 2020/5/19 10:38
# @Author     : 笑看风云

'''
查询 MongoDB 数据库中每个集合的符合记录的条数，
把少于 10000 条的集合名称打印到控制台；
'''

from ScrapyMongoDBForSearch.工具.数据库工具 import get_MongoDB_DataBase

if __name__ == '__main__':
    database = get_MongoDB_DataBase()
    collection_names = database.list_collection_names()
    for coll_name in collection_names:
        collcetion = database[coll_name]
        # 选择 bd_body 字段的长度大于 0 的总条数
        # 对应的 MongoDB 查询语句为：
        # db.getCollection('集合名称').find({"bd_body":{$ne:null}}).count()
        # count = collcetion.find({"bd_body": {'$regex': '/^.{1,}$/'}}).count()
        count = collcetion.count_documents({"bd_body": {'$exists': True}})
        if count < 5000:
            # PyCharm 控制台输出带颜色的文字方法：
            # https://www.cnblogs.com/LY-C/p/9112720.html
            # print("\033[0;32;40m" + coll_name + " ------> 集合的数据不足 5000 条！" + "\033[0m")
            print(coll_name + " ------> 集合的数据不足 5000 条！")
        # else:
        #     print("\033[31m" + coll_name + " ------> 集合的数据已达 5000 条！" + "\033[0m")
