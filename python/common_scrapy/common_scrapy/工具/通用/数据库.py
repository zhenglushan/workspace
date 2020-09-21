# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 数据库工具.py
# @DATETime   : 2020/5/18 15:07
# @Author     : 笑看风云

import MySQLdb
import MySQLdb.cursors
from pymongo import MongoClient
from ScrapyMongoDBForSearch.settings import MongoDB_HOST, MongoDB_PORT, MongoDB_DBNAME
from ScrapyMongoDBForSearch.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET, \
    MYSQL_DBNAME_SEARCH


def get_MongoDB_DataBase():
    '''

    :return: 返回数据库 database
    '''
    client = MongoClient(host=MongoDB_HOST, port=MongoDB_PORT)
    database = client[MongoDB_DBNAME]
    return database


class crate_mysql_database_table():
    '''
    创建 MySQL 的数据库和表结构
    '''

    def __init__(self, table_name):
        result = self.create_database()
        if result:
            self.create_table(table_name)

    # 获取数据库的链接 connecttion
    def get_mysql_connection(self, dbname=None):
        if dbname:
            conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
                                   db=dbname)
            cursor = conn.cursor()
        else:
            conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET)
            cursor = conn.cursor()
        return conn, cursor

    # 创建数据库
    def create_database(self):
        try:
            conn, cursor = self.get_mysql_connection()
            cursor.execute("CREATE database if NOT EXISTS {0}".format(MYSQL_DBNAME))
            conn.commit()
            conn.close()
            result = True
            print("数据库", MYSQL_DBNAME, "创建成功")
        except MySQLdb.Error as e:
            print("MySQL 数据库错误信息:%s" % str(e))
            result = False
            print("数据库", MYSQL_DBNAME, "创建失败")
        return result

    # 创建表结构
    def create_table(self, table_name):
        try:
            conn, cursor = self.get_mysql_connection(MYSQL_DBNAME)
            cursor.execute("""
        		CREATE TABLE if NOT EXISTS `{0}` (
        		  `id` mediumint(10) unsigned NOT NULL AUTO_INCREMENT, # 主键 ID
        		  `url` varchar(200) NOT NULL, # 内容页的 URL 地址
        		  `urlhash` varchar(200) NOT NULL, # URL 哈希值 对应去重的 目录
        		  `title` varchar(200) NOT NULL, # 标题
        		  `body` longtext NOT NULL, # 正文
        		  `is_published` tinyint DEFAULT FALSE, # 是否已经发布
        		  `has_image` tinyint DEFAULT FALSE, # 是否包含图片
        		  PRIMARY KEY USING BTREE (`id`)
        		) ENGINE=MyISAM DEFAULT CHARSET={1};
        		""".format(table_name, MYSQL_CHARSET))
            conn.commit()
            conn.close()
            result = True
            print("表结构", table_name, "创建成功")
        except MySQLdb.Error as e:
            print("MySQL 数据库错误信息:%s" % str(e))
            result = False
            print("表结构", table_name, "创建失败")
        return result


class CreateSearchResultDatabaseAndtable():
    '''
    创建 MySQL 的数据库和表结构
    '''

    # 主构造函数
    def __init__(self, table_name, type):
        result = self.create_database()
        if result:
            self.create_table(table_name, type)

    # 创建保存图片信息的表结构
    @classmethod
    def create_images_table(cls, table_name):
        return cls(table_name, type='images')

    # 创建保存图片信息的表结构
    @classmethod
    def create_contents_table(cls, table_name):
        return cls(table_name, type='contents')

    # 获取数据库的链接 connecttion
    def get_mysql_connection(self, dbname=None):
        if dbname:
            conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
                                   db=dbname)
            cursor = conn.cursor()
        else:
            conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET)
            cursor = conn.cursor()
        return conn, cursor

    # 创建数据库
    def create_database(self):
        try:
            conn, cursor = self.get_mysql_connection()
            cursor.execute("CREATE database if NOT EXISTS {0}".format(MYSQL_DBNAME_SEARCH))
            conn.commit()
            conn.close()
            result = True
            print("数据库", MYSQL_DBNAME_SEARCH, "创建成功")
        except MySQLdb.Error as e:
            print("MySQL 数据库错误信息:%s" % str(e))
            result = False
            print("数据库", MYSQL_DBNAME_SEARCH, "创建失败")
        return result

    # 创建表结构
    def create_table(self, table_name, type):
        try:
            conn, cursor = self.get_mysql_connection(MYSQL_DBNAME_SEARCH)
            if type == 'contents':
                cursor.execute("""
                    CREATE TABLE if NOT EXISTS `{0}` (
                      `id` mediumint(10) unsigned NOT NULL AUTO_INCREMENT, # 主键 ID
                      `word` longtext NOT NULL, # 关键词
                      `titles` longtext NOT NULL, # 标题
                      `jianjies` longtext NOT NULL, # 简介
                      `is_crawl` tinyint DEFAULT FALSE, # 是否已经采集
                      `is_published` tinyint DEFAULT FALSE, # 是否已经发布
                      PRIMARY KEY USING BTREE (`id`)
                    ) ENGINE=MyISAM DEFAULT CHARSET={1};
                    """.format(table_name, MYSQL_CHARSET))
            else:
                cursor.execute("""
                    CREATE TABLE if NOT EXISTS `{0}` (
                      `id` mediumint(10) unsigned NOT NULL AUTO_INCREMENT, # 主键 ID
                      `word` longtext NOT NULL, # 关键词
                      `image_urls` longtext NOT NULL, # 图片地址
                      PRIMARY KEY USING BTREE (`id`)
                    ) ENGINE=MyISAM DEFAULT CHARSET={1};
                    """.format(table_name, MYSQL_CHARSET))
            conn.commit()
            conn.close()
            result = True
            print("表结构", table_name, "创建成功")
        except MySQLdb.Error as e:
            print("MySQL 数据库错误信息:%s" % str(e))
            result = False
            print("表结构", table_name, "创建失败")
        return result
