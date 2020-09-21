# -*- coding:utf-8 -*-
# @ProjectName: PyCompany
# @Email	  : 276517382@qq.com
# @FileName   : MongoDBService.py
# @DATETime   : 2020/1/7 17:27
# @Author     : 笑看风云

from pymongo import MongoClient

# 使用 MongoDB 数据库
MongoDB_HOST = '127.0.0.1'
MongoDB_PORT = 27017
MongoDB_DBNAME = 'scrapy_mongodb_search'


def get_MongoDB_DataBase():
    '''

    :return: 返回数据库 database
    '''
    client = MongoClient(host=MongoDB_HOST, port=MongoDB_PORT)
    database = client[MongoDB_DBNAME]
    return database


if __name__ == '__main__':
    pass
    # print(get_MongoDB_DataBase())
