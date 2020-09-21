# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommonScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    spider_name = scrapy.Field()  # 爬虫名称
    headers = scrapy.Field()  # 请求头信息
    user_agent = scrapy.Field()  # User-Agent 信息
    table_name = scrapy.Field()  # 表名
    root_domain = scrapy.Field()  # 根域名
    url = scrapy.Field()
    urlhash = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    is_published = scrapy.Field()
    has_image = scrapy.Field()

    # 图片处理相关字段
    images = scrapy.Field()  # 保存图片下载信息
    image_url_sources = scrapy.Field()  # 图片在 body 中的原本的 URL 路径
    image_url_fulls = scrapy.Field()  # 图片 URL 补全后的路径
    image_paths = scrapy.Field()  # 保存图片 本地 路径
