# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import re
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import codecs
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from common_scrapy.settings import IMAGES_STORE
from common_scrapy.工具.通用工具 import get_md5, get_image_extension


class CommonScrapyPipeline:
    def process_item(self, item, spider):
        return item


class DownloadImagePipeline(ImagesPipeline):
    '''
    下载图片的类
    '''

    def file_path(self, request, response=None, info=None):
        '''
        处理每个图片对应的本地保存路径
        :param request:
        :param response:
        :param info:
        :return:
        '''
        item = request.meta['item']
        directory = item['spider_name'] + '/' + item['urlhash']
        image_url = request.url
        image_md5 = get_md5(image_url)
        image_ext = get_image_extension(image_url)
        image_guid = image_md5 + image_ext
        file_name = '{0}/{1}'.format(directory, image_guid)  # 生成图片保存位置
        return file_name

    def get_media_requests(self, item, info):
        '''
        发起下载图片的请求:
        :param item:
        :param info:
        :return:
        Referer 使用图片的 URL 还是 图片所在页面的 URL 以后碰到再进行调整
        调整时，可以先看看 item 里面是否包含 request
        '''
        headers = item['headers']
        headers['User-Agent'] = item['user_agent']
        headers['Referer'] = item['url']
        image_list = item['image_url_fulls']
        if image_list:
            for image_url in image_list:
                image_url = image_url.replace("&amp;", "&")
                yield Request(image_url, headers=headers, meta={'item': item})

    def image_downloaded(self, response, request, info):
        '''
        下载图片操作:
        :param response:
        :param request:
        :param info:
        :return:
        '''
        try:
            super(DownloadImagePipeline, self).image_downloaded(response, request, info)
        except:
            print("有问题的图片地址为: " + request.url)
            print("有问题的图片的网页地址为: " + request.meta['item']['url'])
            # image_downloaded 能否修改 内容?
            # item = request.meta['item']
            # body = item['body']
            # re_sub = '<img[^>]*src=[\"\']' + request.url + '[\"\'][^>]*>'
            # body = re.sub(re_sub, "", body, 1)
            # item['body'] = body
            # request.meta['item'] = item

    def item_completed(self, results, item, info):
        '''
        图片下载完成:
        把本地存储图片的路径保存到 item['image_paths'] 变量中
        :param results:
        :param item:
        :param info:
        :return:
        '''
        image_url_sources = item['image_url_sources']
        body = item['body']
        image_paths = []
        for result in results:
            index = results.index(result)
            state = result[0]
            '''
                通过 state 判断图片是否下载成功
                成功，则把 body 中的该图片的 src 替换为本地路径
                失败，则删除 body 中的该图片代码
            '''
            if state:
                image_path = result[1]['path']
                # image_path = IMAGES_STORE + image_path
                image_paths.append(image_path)
                body = body.replace(image_url_sources[index], image_path)
            else:
                re_sub = "<img[^>]*src=[\"\']" + image_url_sources[index] + "[\"\'][^>]*>"
                body = re.sub(re_sub, "", body, count=1)

        item['body'] = body
        item['image_paths'] = image_paths

        if len(image_paths) > 0:
            item['has_image'] = True
        else:
            item['has_image'] = False
        # print(item)
        return item


class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 该函数的定义是固定的，也就是说函数名 from_settings 是固定的,用于读取 settings.py 配置文件
    # 该方法在我们自定义组件和扩展的时候非常有用
    # 这里的参数 settings 其实就是对应于 settings.py 这个文件
    # from_settings 由 scrapy 自动调用，在调用的时候会把 settings.py 的内容传递到 settings 变量
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        body = item['body']

        root_domain = item['root_domain']
        # body = raplace_domains(body, root_domain)  # 删除站点域名

        # 在 img 前后加 div 标签，并使图片居中显示

        body = re.sub(r'(</?img[^>]*>)', r'<span class ="yrkj" style="display:block;text-align:center;">\1</span>',
                      body, flags=re.I | re.S)
        item['body'] = body
        # 使用 twisted 将 mysql 的 insert 操作变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的 insert 操作语句
        insert_sql = """
            insert into {0}(url,urlhash,title,body,is_published,has_image)
            values(%s,%s,%s,%s,%s,%s)
        """.format(item['table_name'])
        # cursor.execute(insert_sql,
        #                (item['url'], item['urlhash'], item['title'], item['body'], item['is_published'],
        #                 item['has_image']))
        print("网址为: " + item['url'] + " 的数据已成功保存到数据库！")
