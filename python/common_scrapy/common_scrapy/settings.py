# Scrapy settings for common_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'common_scrapy'

SPIDER_MODULES = ['common_scrapy.spiders']
NEWSPIDER_MODULE = 'common_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'common_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# 日志级别, 默认是 DEBUG, 即打印 DEBUG, INFO, WARNING, ERROR 所有 LOG 信息
LOG_LEVEL = 'ERROR'
# LOG_FILE = 'Log.txt' # 记录日志的文件

HTTPERROR_ALLOWED_CODES = [302, 304, 400, 403, 404]  # 允许返回 400 403 404 状态的页面

# 配置图片保存地址
# IMAGES_MIN_WIDTH = 100  # 限制图片的最小宽度
# IMAGES_MIN_HEIGHT = 100  # 限制图片的最小高度
# 当图片小于限制的尺寸时, 会方式图片下载异常
# 配置保存图片的根目录
IMAGES_STORE = "D:/数据采集/" + BOT_NAME + "_images/"
# 图片路径格式为 IMAGES_STORE SpiderName ContentURL
# E:/ScrapyUploadImageData/mm131mm/1a2s3d456h7j8k9l12s3d4fg6h7j8/
# MEDIA_ALLOW_REDIRECTS = False  # 允许图片 301

# 项目关键词文件地址
# D:/WorkSpace/数据采集/scrapy_mongodb_for_search_keyword_files/

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'ScrapyUploadImage.middlewares.ScrapyuploadimageDownloaderMiddleware': 543,
    # 'ScrapyUploadImage.middlewares.UserAgentMiddleware',100,
}
DOWNLOAD_DELAY = 0.1  # 下载延迟 0.3 秒

ITEM_PIPELINES = {
    'common_scrapy.pipelines.DownloadImagePipeline': 1,
    'common_scrapy.pipelines.MysqlTwistedPipeline': 2,
    'common_scrapy.pipelines.ScrapyMongodbForSearchPipeline': 300,
}

# SQL 日期时间格式
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 阿布云代理 IP
# 通行证书
PROXY_USER = 'HG852AT514B0W11D'
# 通行密钥
PROXY_PASS = '5EE9BE9B8B92882D'
# 拼接阿布云代理字符串
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": "http-dyn.abuyun.com",
    "port": "9020",
    "user": PROXY_USER,
    "pass": PROXY_PASS,
}

# MySQL 保存数据
MYSQL_HOST = '127.0.0.1'
# MYSQL_DBNAME = 'scrapy_upload_image'
MYSQL_DBNAME = 'zlswordpress'
MYSQL_DBNAME_SEARCH = 'search_result_baidu'  # 保存百度搜索结果的数据库
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_CHARSET = 'utf8mb4'

# 使用 MongoDB 数据库
MongoDB_HOST = '127.0.0.1'
MongoDB_PORT = 27017
MongoDB_DBNAME = 'scrapy_mongodb_search'

# 大无极香港服务器 Remote FTP
# FTP_HOST = '5.180.96.47'
FTP_HOST = '5.180.96.47'
FTP_PORT = 20110
FTP_USERNAME = 'root'
FTP_PASSWORD = 'JD844ujdhje$@'
FTP_REMOTE_PATH = '/zls/server/apache/htdocs/{0}/zlslhxwww'

# 配置参考:
# https://blog.csdn.net/xc_zhou/article/details/82760608
# https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/settings.html
