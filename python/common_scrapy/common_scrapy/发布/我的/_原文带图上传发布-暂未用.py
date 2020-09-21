# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors
from ScrapyMongoDBForSearch.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET, \
    SQL_DATETIME_FORMAT, IMAGES_STORE, FTP_REMOTE_PATH
import datetime
import re
from bs4 import BeautifulSoup
from ScrapyMongoDBForSearch.工具.通用工具 import file_uploads_path, post_dede, get_md5
from ScrapyMongoDBForSearch.工具.又拍云.又拍云FTP上传 import DoFTP
from ScrapyMongoDBForSearch.工具.分词工具.结巴带图片分词 import FenCiImage

import random
from threading import Thread
from time import sleep


# 上传正文中的全部图片
class PublishSuperMorePic():
    def __init__(self, tableName, dictName, webSites, pubNum):
        '''
        :param tableName: 需要查询的表名
        :param dictName: 需要分词的字典名
        :param webSites: 要发布内容的网站
        :param pubNum: 要发布的最大篇数
        '''
        self.tableName = tableName
        self.dictName = dictName
        self.webSites = webSites
        self.pubNum = pubNum

    def get_mysql_connection(self):
        '''
        获取数据库连接
        :return:
        '''
        conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
                               db=MYSQL_DBNAME)
        cursor = conn.cursor()
        return conn, cursor

    def main_publish(self):
        ids = []
        line_threads = []  # 添加线程组
        fetch_result = self.select_data()
        if fetch_result:
            for result in fetch_result:
                line_thread = Thread(target=self.post_data, args=(result,))
                line_threads.append(line_thread)
                id = result[0]
                ids.append(str(id))
            for lt in line_threads:
                lt.start()
            for lt in line_threads:
                lt.join()
            update_result = self.update_data(ids)
            if update_result:
                print("数据更新成功！")

    def select_data(self):
        '''
        选择要发布的数据
        :return:
        '''
        conn, cursor = self.get_mysql_connection()
        fetch_sql = "SELECT id,urlhash,title,body,has_image FROM `{0}` WHERE is_published=0 LIMIT 0,{1};".format(
            self.tableName, self.pubNum)
        cursor.execute(fetch_sql)
        fetch_result = cursor.fetchmany(self.pubNum)
        if fetch_result:
            return fetch_result
        else:
            return None

    def update_data(self, ids):
        conn, cursor = self.get_mysql_connection()
        ids = ','.join(ids)
        update_sql = "UPDATE `{0}` SET is_published=1 WHERE id IN ({1})".format(self.tableName, ids)
        update_result = cursor.execute(update_sql)
        if update_result:
            return True
        else:
            return False

    def delete_data(self, ids):
        conn, cursor = self.get_mysql_connection()
        ids = ','.join(ids)
        delete_sql = "DELETE FROM `{0}` WHERE id IN ({1})".format(self.tableName, ids)
        delete_result = cursor.execute(delete_sql)
        if delete_result:
            return True
        else:
            return False

    def post_data(self, result):
        urlhash = result[1]
        title = result[2]
        body = result[3]
        has_image = result[4]
        pub_date = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        domain = random.choice(self.webSites)
        domain_arr = domain.split('|')
        domain = domain_arr[0]
        service = domain_arr[1]

        lit_pic_path = ''
        if has_image:
            # 上传图片
            body, lit_pic_path = self.post_img(title, body, pub_date, domain, service)
        fenci = FenCiImage(title, self.dictName)  # 图片站，用 title 做分词处理
        tags, keywords = fenci.returnValues()
        try:
            # 发布内容
            result = post_dede(title, pub_date, body, domain, lit_pic_path, tags, keywords)  # 发布操作
            # sleep(3)
        except Exception as e:
            pass
        if result:
            print(title + " 文章发布成功！" + "\n")
        else:
            print(title + " 文章发布失败！" + "\n")

    def post_img(self, title, body, pub_date, domain, service):
        img_source = ''  # fitness39net/997c9a14092d600d2aa40b0093b3ef41/81d11515d2b5653bd47896c4e4a6e583.jpg
        img_source_full = ''  # C:/ScrapyUploadImageData/fitness39net/997c9a14092d600d2aa40b0093b3ef41/81d11515d2b5653bd47896c4e4a6e583.jpg
        img_name = ''  # 81d11515d2b5653bd47896c4e4a6e583.jpg
        img_path_full = ''  # C:/ScrapyUploadImageData/fitness39net/997c9a14092d600d2aa40b0093b3ef41/
        lit_pic_path = ''
        soup = BeautifulSoup(body, "html5lib")
        img_arr = soup.select("img")
        if img_arr:
            # 1、循环正文中的每张图片
            for img in img_arr:
                img_source = img.get("src")
                img_source_full = IMAGES_STORE + img_source
                img_name = img_source.split('/')[-1]
                img_path_full = img_source_full.replace(img_name, '')

                # 2、把图片上传到服务器, 并替换正文中的图片的路径
                if len(img_source) > 0:
                    # 图片上传的局部路径, 不包括文件名
                    # /uploads/allimg/2019/6/12/
                    part_remote_path = file_uploads_path(pub_date)
                    # 图片上传的完整路径, 不包括文件名
                    # /zls/server/apache/htdocs/{0}/zlslhxwww/uploads/allimg/2019/6/12/
                    full_remote_path = part_remote_path
                    doFtp = DoFTP()
                    domain_md5 = get_md5(domain)
                    full_remote_path_uploads = '/' + domain_md5 + full_remote_path
                    uploads_res = doFtp.uploads(img_path_full, full_remote_path_uploads, img_name, service)  # 上传图片
                    if not uploads_res:
                        print(title + " 中名为 : " + img_name + " 的图片上传失败了！" + "\n")
                        # 三种方式都匹配一次, 防止漏掉
                        re_sub = '<span[^>]*class =[\"\']yrkj[\"\'][^>]*><img[^>]*src=[\"\']' + img_source + '[\"\'][^>]*></span>'
                        body = re.sub(re_sub, "", body, count=1)
                        re_sub = '<p[^>]*><img[^>]*src=[\"\']' + img_source + '[\"\'][^>]*></p>'
                        body = re.sub(re_sub, "", body, count=1)
                        re_sub = '<img[^>]*src=[\"\']' + img_source + '[\"\'][^>]*>'
                        body = re.sub(re_sub, "", body, count=1)
                    else:
                        print(title + " 中名为 : " + img_name + " 的图片上传成功了！" + "\n")
                        body = body.replace(img_source, '/' + domain_md5 + part_remote_path + img_name)
                        lit_pic_path = '/' + domain_md5 + part_remote_path + img_name
        return body, lit_pic_path


if __name__ == "__main__":
    pass
    # publish = PublishSuper('jianfei', '减肥', jianfei_websites, 10)
    # publish.main_publish()
