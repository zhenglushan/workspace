# -*- coding:utf-8 -*-
import re
import os
import requests
import datetime
import time
import MySQLdb
import MySQLdb.cursors
from random import randint
from scrapy.http import HtmlResponse
from ScrapyUploadImage.settings import MYSQL_CHARSET, MYSQL_DBNAME_SEARCH, MYSQL_HOST, \
    MYSQL_PASSWORD, \
    MYSQL_USER, SQL_DATETIME_FORMAT
from ScrapyUploadImage.tools.commons import get_md5, get_image_extension
from ScrapyUploadImage.tools.domysql_requests import CreateSearchResultDatabaseAndtable

from ScrapyUploadImage.spiders_requests.search_result._0_search_result_config import keyword_list, \
    BAIDU_SEARCH_IMAGE_STORE, BAIDU_SEARCH_KEYWORD


class SearchResultImportKeywords():

    def __init__(self, keyword, keyword_path):
        '''
        初始化对象
        :param table_name: 既做表名，又做文件夹名，同时也是下载图片的关键词
        :param word_path: 分类关键词词库路径，该路径下可包含多个关键词文件
        '''
        self.table_name = keyword + '_' + 'contents'
        self.word_path = keyword_path

        CreateSearchResultDatabaseAndtable.create_contents_table(self.table_name)

        # 获取所有关键词文件的路径
        self.getKeywordPathArr()

        # 循环打开所有关键词文件 并按行读取该文件的所有关键词
        for word_path in self.word_path_arr:
            print("当前处理的关键词词库路径为：" + word_path)
            wordfile = open(word_path, 'r', encoding='UTF-8')
            while True:
                lines = wordfile.readlines(10000)  # 每次读取 10000 行关键词
                if not lines:
                    break
                insert_sql = "INSERT INTO `" + self.table_name + "`(word,titles,jianjies,is_crawl,is_published) VALUES "
                temp_arr = []
                for line in lines:
                    line = line.replace('-', '').strip()
                    if len(line) > 0:
                        line = str(MySQLdb.escape_string(line), encoding="utf-8")
                        temp = "('" + line + "','','',0,0)"
                        temp_arr.append(temp)
                temp_values = ",".join(temp_arr)
                insert_sql = insert_sql + temp_values
                result = self.do_insert(insert_sql)
                if result:
                    print("批量保存 " + keyword + " 关键词到数据库的操作……成功……")
                else:
                    print("批量保存 " + keyword + " 关键词到数据库的操作……失败……")
                time.sleep(0.1)
            wordfile.close()

    def getKeywordPathArr(self):
        '''
        获取关键词词库路径下的所有关键词文件的路径并保存到列表
        :return:
        '''
        word_file_arr = os.listdir(self.word_path)
        word_file_arr.sort()
        word_path_arr = []
        for df in word_file_arr:
            dict_path = self.word_path + df
            word_path_arr.append(dict_path)
        self.word_path_arr = word_path_arr

    def get_mysql_connection(self):
        '''
        获取数据库连接
        :return:
        '''
        conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
                               db=MYSQL_DBNAME_SEARCH)
        cursor = conn.cursor()
        return conn, cursor

    def do_insert(self, insert_sql):
        try:
            conn, cursor = self.get_mysql_connection()
            # 执行具体的 insert 操作语句
            cursor.execute(insert_sql)
        except:
            return False
        else:
            return True


if __name__ == '__main__':

    for keyword in keyword_list:
        keyword = keyword.strip()
        keyword_path = BAIDU_SEARCH_KEYWORD + keyword + '/'
        exist = os.path.exists(keyword_path)  # 判断关键词词库目录是否存在
        if exist:
            SearchResultImportKeywords(keyword, keyword_path)
        else:
            print(keyword + " 词库不存在哦，请补上，谢谢！")
