# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from common_scrapy.工具.通用工具 import baidu_user_agent

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class CommonScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CommonScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class UserAgentMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        headers = spider

        dir(request)

        request.headers.setdefault('User-Agent', baidu_user_agent)


""" 配置阿布云代理 IP 中间件 """


class ABuYunProxyMiddleware(object):
    '''
    配置阿布云代理 IP 中间件
    '''
    # 要访问的目标页面
    targetUrl = "http://httpbin.org/get"  # 返回 IP 相关信息

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    proxyServer = "http://" + proxyHost + ":" + proxyPort

    # 使用 HTTP 隧道 动态版
    # 代理隧道验证信息
    proxyUser = PROXY_USER  # 通行证书
    proxyPass = PROXY_PASS  # 通行密钥
    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth
        # print("---------- 当前请求的 IP 地址为 : ----------:" + request.meta["proxy"])


"""
Company 使用阿布云代理 IP 的 Scrapy 爬虫
"""
from common_scrapy.spiders.jing_pin.abuyun_for_company import proxy_server, proxy_auth


class CompanyABuYunProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = proxy_server
        request.headers["Proxy-Authorization"] = proxy_auth
