# -*- coding:utf-8 -*-
import re
import os
import requests
import datetime
import MySQLdb
import MySQLdb.cursors
from random import randint
from ScrapyUploadImage.spiders_requests.search_result._0_search_result_config import keyword_list, \
    BAIDU_SEARCH_IMAGE_STORE
from ScrapyUploadImage.settings import MYSQL_CHARSET, MYSQL_DBNAME_SEARCH, MYSQL_HOST, MYSQL_PASSWORD, \
    MYSQL_USER, SQL_DATETIME_FORMAT
from ScrapyUploadImage.tools.commons import get_md5, get_image_extension
from ScrapyUploadImage.tools.domysql_requests import CreateSearchResultDatabaseAndtable


class SearchResultCrawlImages():

    def __init__(self, name):
        '''
        初始化对象
        :param table_name: 既做表名，又做文件夹名，同时也是下载图片的关键词
        '''
        self.table_name = name + '_' + 'images'
        self.kwdir_name = name

        # 创建表结构
        CreateSearchResultDatabaseAndtable.create_images_table(self.table_name)

        # 下载和保存关键词对应的图片的路径字符串
        print("当前正在下载图片………………")
        image_path_str = self.get_image_urls(self.kwdir_name)
        print("当前正在保存图片路径………………")
        result = self.do_insert(name, image_path_str)
        print("当前时间为：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT))
        if result:
            print("图片路径信息保存成功………………")
        else:
            print("图片路径信息保存失败………………")

    def get_image_urls(self, keyword):
        '''
        收集即将下载的 image 的 url 路径集合
        :param keyword:
        :return:
        '''
        image_arr = set()
        request_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn={0}'

        headers = {
            "Host": "image.baidu.com",
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
        }

        pn_max = randint(6, 12)  # 实战中设置为 (6, 12) 测试时设置为 (1, 2)
        for pn in range(0, pn_max):
            # 每个页面的 objURL 数量为 60 所以要 乘以 60
            req_url = request_url.format(pn * 60)
            headers.update({"Referer": req_url})
            resp = requests.get(req_url, {'headers': headers})
            print("正在抓取 " + req_url + " 页面的图片！")
            pic_url = re.findall('"objURL":"(.*?)",', resp.text, flags=re.I | re.S)
            if pic_url:
                for url in pic_url:
                    if len(url) > 0:
                        image_arr.add(url)
        if len(image_arr) > 0:
            print("共需要下载" + str(len(image_arr)) + "张图片！")
            image_path_str = self.download_image(image_arr)
            return image_path_str
        else:
            return ''

    def download_image(self, image_arr):
        '''
        下载图片的操作
        :param keyword:
        :param image_arr:
        :return:
        '''
        image_path_str = ''
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
        }
        for image_url in image_arr:
            headers.update({"Referer": image_url})
            try:
                pic = requests.get(image_url, headers=headers, timeout=7)
                content = pic.content
            except BaseException:
                print('错误 ' + image_url + ' 图片无法下载！')
                continue
            else:
                if len(content) < 1024 * 10:  # 过滤内容长度小于 10K 的图片
                    print('图片 ' + image_url + ' 太小了，放弃下载')
                else:
                    print("当前下载的图片地址为：" + image_url)
                    # print("当前下载的图片长度为：" + str(len(content)))
                    # print("当前下载的图片名称为：" + get_md5(image_url))
                    # 去重和创建文件夹
                    pic_dir = BAIDU_SEARCH_IMAGE_STORE + (self.kwdir_name) + '/'
                    exist = os.path.exists(pic_dir)  # 去重
                    if not exist:
                        os.makedirs(pic_dir, mode=0o777)  # 创建 URL 对应的文件夹
                    # 去重和创建图片文件
                    pic_sort_path = get_md5(image_url) + get_image_extension(image_url)
                    pic_file_path = pic_dir + pic_sort_path
                    exist = os.path.exists(pic_file_path)  # 去重
                    if not exist:
                        fp = open(pic_file_path, 'wb')
                        fp.write(content)
                        fp.close()
                        image_path_str = image_path_str + (self.kwdir_name) + '/' + pic_sort_path + '[ips]'
        return image_path_str

    def get_mysql_connection(self):
        '''
        获取数据库连接
        :return:
        '''
        conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
                               db=MYSQL_DBNAME_SEARCH)
        cursor = conn.cursor()
        return conn, cursor

    def do_insert(self, word, image_urls):
        try:
            conn, cursor = self.get_mysql_connection()
            # 执行具体的 insert 操作语句
            insert_sql = "INSERT INTO {0}(word,image_urls) VALUES (%s,%s)".format(self.table_name)
            cursor.execute(insert_sql, (word, image_urls))
        except:
            print("图片保存操作失败！")
            return False
        else:
            print("图片数据保存操作成功！")
            return True


if __name__ == '__main__':
    for keyword in keyword_list:
        keyword = keyword.strip()
        SearchResultCrawlImages(keyword)
