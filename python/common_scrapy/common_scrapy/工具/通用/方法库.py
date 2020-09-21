# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 通用工具.py
# @DATETime   : 2020/5/18 15:04
# @Author     : 笑看风云

'''
创建虚拟环境:
mkvirtualenv Py372BrowserCrawler
激活虚拟环境:
workon Py372BrowserCrawler
安装如下插件:
pip install requests
pip install lxml
pip install beautifulsoup4
pip install -i https://pypi.doubanio.com/simple/ selenium
pip install html5lib # 指定 beautifulsoup4 使用 html5lib 为解析库

Selenium Python3 请求头配置
https://blog.csdn.net/u013440574/article/details/81911954

删除保存 URL MD5 目录的命令
rd /s/q mt.sohu.com

Chrome WebDriver 下载地址:

FireFox WebDriver 下载地址:
https://github.com/mozilla/geckodriver/releases/

'''
import datetime
import hashlib
import os
import shutil
import random
import re
import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options
from ScrapyMongoDBForSearch.settings import SQL_DATETIME_FORMAT
import tldextract

import MySQLdb
import MySQLdb.cursors
from ScrapyMongoDBForSearch.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET
from ScrapyMongoDBForSearch.settings import IMAGES_STORE

import time
import re
import os
import hashlib
from urllib import parse
import datetime
import requests
from random import choice
import math

from ScrapyMongoDBForSearch.settings import SQL_DATETIME_FORMAT

'''
    定义变量
'''
'''
User Agent
'''
baidu_user_agent = "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"
google_user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
firefox_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"
chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"



def get_s_d_s(fulldomain):
    '''
    返回域名的各个组成部分
    :param fulldomain:
    :return:
    '''
    result = tldextract.extract(fulldomain)
    subdomain = result.subdomain
    domain = result.domain
    suffix = result.suffix
    return subdomain, domain, suffix


def get_host(fulldomain):
    '''
    返回类似 yimin.baidu.com.cn 的字符串
    :param fulldomain:
    :return:
    '''
    subdomain, domain, suffix = get_s_d_s(fulldomain)
    if subdomain:
        return subdomain + '.' + domain + '.' + suffix
    else:
        return domain + '.' + suffix


def get_name(fulldomain):
    '''
    返回类似 yimin_baidu_com_cn 的字符串
    :param fulldomain:
    :return:
    '''
    subdomain, domain, suffix = get_s_d_s(fulldomain)
    subdomain = subdomain.replace('.', '_')
    domain = domain.replace('-', '_')
    suffix = suffix.replace('.', '_')
    if subdomain:
        return subdomain + '_' + domain + '_' + suffix
    else:
        return domain + '_' + suffix


def get_root_domain(fulldomain):
    '''
    返回类似 baidu.com.cn 的字符串
    :param fulldomain:
    :return:
    '''
    subdomain, domain, suffix = get_s_d_s(fulldomain)
    return domain + '.' + suffix


def get_chromedriver_path():
    '''
    返回 ChromeDriver 的路径
    :return:
    '''
    return "./tools/chromedriver.exe"


def set_options():
    '''
    模拟浏览器操作时，需要配置的一些选项
    :return:
    '''
    options = Options()
    prefs = {
        "profile.managed_default_content_settings.images": 2
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--disable-infobars')
    options.add_argument('--headless')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument(
        '--user-agent="Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"')
    return options


def filter_title(title):
    '''
    处理标题的多余代码
    :param title:
    :return:
    '''
    # 过滤标题所有的 HTML 标签
    rex = re.compile(r'<[^>]+>', flags=re.I | re.S)
    title = rex.sub('', title)
    # 把标题中的连续的多个空格替换成一个
    rex = re.compile(r'\s+', flags=re.I | re.S)
    title = rex.sub(' ', title)
    title = title.strip()
    return title


def filter_common_html(text):
    '''
    过滤常见的 HTML 标签，一般用于内容的正文部分
    :param text:
    :return:
    '''

    text = text.replace('<div', '<p').replace('</div', '</p')

    re_rule = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', flags=re.I | re.S)  # 匹配 Script
    text = re_rule.sub('', text)  # 去掉 Script

    re_rule = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', flags=re.I | re.S)  # 匹配 style
    text = re_rule.sub('', text)  # 去掉 style

    re_rule = re.compile('<!?-[^>]*->')  # 过滤掉 HTML 注释
    text = re_rule.sub('', text)

    re_rule = re.compile('style=[\'\"].*?[\'\"]', flags=re.I | re.S)  # 匹配 style
    text = re_rule.sub('', text)  # 去掉 style

    re_rule = re.compile('<p[^>]*>', flags=re.I | re.S)  # 过滤 p 标签的所有属性
    text = re_rule.sub('<p>', text)  # 过滤 p 标签的所有属性

    re_rule = re.compile('</p[^>]*>', flags=re.I | re.S)  # 过滤 p 标签的所有属性
    text = re_rule.sub('</p>', text)  # 过滤 p 标签的所有属性

    # 过滤所有HTML标签的属性除了 src 和 alt 属性，同时把值的长度为零的属性也删除
    # re_rule = re.compile('\s(?!src|alt)[a-zA-Z]+=[\'\"]{1}[^\'\"]+[\'\"]{1}', re.I)
    re_rule = re.compile('\s(?!src)[a-zA-Z0-9|\-|:]+=[\'\"]{1}[^\'\"]*[\'\"]{1}', flags=re.I | re.S)
    text = re_rule.sub("", text)

    # # 在 img 前后加 div 标签，并使图片居中显示
    # text = re.sub(r'(</?img[^>]*>)', r'<p class ="yrkj" style="display:block;text-align:center;">\1</p>', text,
    #               re.I | re.S)

    re_rule = re.compile('//<!\[CDATA\[[^>]*//\]\]>', flags=re.I | re.S)  # 匹配 CDATA
    text = re_rule.sub('', text)  # 去掉 CDATA

    # re_rule = re.compile('<br\s*?/?>')  # 处理换行 , 一般 <br/> 标签可以留着
    # text = re_rule.sub('', text)

    # 过滤 a div table tbody tr td font span 标签
    re_rule = re.compile('</?embed[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?a[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?div[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?table[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?tbody[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?tr[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?td[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?font[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?span[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?b[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?strong[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?hr[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?form[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?frame[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?iframe[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?sub[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)
    re_rule = re.compile('</?sup[^>]*>', flags=re.I | re.S)
    text = re_rule.sub("", text)

    # 过滤<__("<"号后面带空格)
    re_rule = re.compile('<\s+', flags=re.I | re.S)
    text = re_rule.sub("<", text)

    # 过滤__>(">"号前面带空格)
    re_rule = re.compile('\s+>', flags=re.I | re.S)
    text = re_rule.sub(">", text)

    # 把标签外部的连续多个空格替换成零个，主要用于内容正文部分
    # 比如:
    # <p>   这个是什么时候的事情？
    # 爱学习的孩子是我们学习的好榜样！   </p>

    rex = re.compile(r'>\s+', flags=re.I | re.S)
    text = rex.sub('>', text)
    rex = re.compile(r'\s+<', flags=re.I | re.S)
    text = rex.sub('<', text)

    text = text.replace("\r", "").replace("\n", "").replace("\t", "").replace('<p><br/></p>', '').replace('<p><br></p>',
                                                                                                          '')

    # 替换连续的标签
    text = more_to_one(
        ['<div>', '</div>', '<script>', '</script>', '<font>', '</font>', '<span>', '</span>', '<p>', '</p>', '<br>',
         '<br/>'],
        text)

    # 循环处理没有内容的标签对，比如 p 标签的开始和结束之间只有空格
    # 直到处理前和处理后的字符串的长度相同为止
    # 注意 img 和 br 标签不能过滤掉，所以需要加上 (?!img|br) 表示不能以 img 或者 br 开头
    # :param text:
    # :return:
    # 举例：
    # <p> </p>
    # <p> <p>
    rex = re.compile(r'<(?!img|br)[a-zA-Z0-9]+[^>]*>\s*<[/]{0,1}[a-zA-Z0-9]+>', flags=re.I | re.S)
    while True:
        temp = rex.sub('', text)
        if len(text) == len(temp):
            break
        else:
            text = temp

    text = text.strip()

    return text


def del_nosave_dir(table_name, name):
    '''
    根据数据库表结构存在的数据来把硬盘中不存在的目录删除掉
    :param table_name: 表名
    :param name: 文件夹名
    :return:
    '''
    return_ = False
    conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, charset=MYSQL_CHARSET,
                           db=MYSQL_DBNAME)
    cursor = conn.cursor()

    # 获取数据库数据
    fetch_sql = "SELECT urlhash FROM `{0}`;".format(table_name)
    cursor.execute(fetch_sql)
    fetch_result = cursor.fetchall()
    urlhash_list = []
    for result in fetch_result:
        urlhash = result[0]
        urlhash_list.append(urlhash)

    # 扫描文件夹名
    name_path = IMAGES_STORE + name + '/'
    for dirpath, sub_dirs, filenames in os.walk(name_path):
        for sub_dir in sub_dirs:
            # 判断文件夹名是否在数据库数据中
            if sub_dir not in urlhash_list:
                # 删除文件夹
                full_sub_dir = dirpath + sub_dir + '/'
                try:
                    shutil.rmtree(full_sub_dir)
                    print("成功删除 " + full_sub_dir + " 文件夹！")
                except Exception as e:
                    print("删除 " + full_sub_dir + " 文件夹有异常！")
                    return_ = False
                else:
                    return_ = True
    return return_


def more_to_one(str_arr, content):
    '''
    把连续的 HTML 标签替换成一个
    比如 <br/><br/><br/>
         </p></p>
    :param str_arr:
    :param content:
    :return:
    '''
    if len(str_arr) > 0:
        for str in str_arr:
            re_sub = '(' + str + ')+'
            content = re.sub(re_sub, str, content, flags=re.I | re.S)
    return content


def moreReplace(str, arr_source, arr_target):
    '''
    应该匹配每个词在源字符串中的位置
    :param str: 源字符串
    :param arr_source: 查找的关键词数组
    :param arr_target: 替换的关键词数组
    :return:替换后的字符串
    '''
    place_holder = 'ん'  # 占位符
    word_arr = {}  # 保存关键词的位置和该关键词
    new_list = []

    # 查找每个关键词在源字符串中出现的所有位置以及该关键词，并保存到字典中
    for source in arr_source:
        posi = [i.start() for i in re.finditer(source, str)]
        for p in posi:
            word_arr[p] = source

    # 把每个关键词所有出现的位置全部替换为 占位符 ん
    for source in arr_source:
        reg = re.compile(source)
        str = reg.sub(place_holder, str)

    # 对字典按照键进行排序，把排序后的键对应的关键词保存到列表
    for key in sorted(word_arr):
        new_list.append(word_arr[key])

    # 把列表的关键词依次替换字符串中的 ん 完成关键词数组的替换过程
    for word in new_list:
        str = str.replace(place_holder, "<strong>" + word + "</strong>", 1)

    # 返回替换后的字符串
    return str


def completed_img_src(domain, src):
    '''
    补全 img 的 src 的值: 一般 src 有如下三种格式, 需要针对每种格式做出判断
    1、  /uploads/allimg/domop1706/14b34141b0I0-193C0.jpg → 补上当前域名
    2、  //cms-bucket.nosdn.127.net/catchpic/2/2a/2afa08aa008857ecf3acd13211eae696.jpg → 补上 http
    3、  http://cms-bucket.nosdn.127.net/dfbdecac29024d1ca63ddab6ffc975ae20171128104642.jpeg
    :param domain: 当前采集站的域名
    :param src: img 的 src 属性
    :return:
    '''
    full_src = ''

    if src.startswith('http'):
        full_src = src
    elif src.startswith('//'):  # 第二种和第三种情况的顺序不能对换
        full_src = 'http:' + src
    elif src.startswith('/'):  # 第三种和第二种情况的顺序不能对换
        full_src = domain + src
    else:
        pass
    return full_src


def completed_http_url(domain, url):
    '''
    补全 内容页 的 url 的值: 一般 url 有如下三种格式, 需要针对每种格式做出判断

    1、  http://www.baidu.com/guonei/9999.html
    2、  //www.baidu.com/guonei/9999.html → 补上 http
    3、  /guonei/9999.html → 补上当前域名

    :param domain: 当前采集站的域名
    :param url: 内容页 的 url 地址
    :return:
    '''
    full_url = ''

    if url.startswith('http'):
        full_url = url
    elif url.startswith('//'):  # 第二种和第三种情况的顺序不能对换
        if domain.startswith('https'):
            full_url = 'https:' + url
        else:
            full_url = 'http:' + url
    elif url.startswith('/'):  # 第三种和第二种情况的顺序不能对换
        full_url = domain + url
    else:
        pass
    return full_url


def last_filter_image(content):
    '''
    发布正文的时候，首先是进行图片上传的操作的
    如果图片上传失败，则需要把正文中的图片过滤掉，本函数就是干这个事情的，
    只有把上传失败的图片过滤掉，才能把过滤后的文本发布到网站上。
    :return:
    '''
    rex_1 = re.compile(r'<p><span class ="yrkj"[^>]*><img[^>]*></span></p>', flags=re.I | re.S)
    content = rex_1.sub('', content)

    rex_2 = re.compile(r'<span class ="yrkj"[^>]*><img[^>]*></span>', flags=re.I | re.S)
    content = rex_2.sub('', content)
    return content


def file_uploads_path(pubdate):
    '''
    生成文件上传路径的字符串 /uploads/allimg/ 开始

    pubdate 的格式为 %Y-%m-%d %H:%M:%S
    如果不是该格式，则要凑成该格式
    根据 pubdate 生成上传文件的局部路径
    分别取 pubdate 的 year month day 的值
    :param pubdate:
    :return: part_path 返回完整的图片路径
    '''
    date_time = time.strptime(pubdate, SQL_DATETIME_FORMAT)
    year = date_time.tm_year
    month = date_time.tm_mon
    day = date_time.tm_mday

    part_path = str(year) + "/" + str(month) + "/" + str(day) + "/"

    uploads_path = "/uploads/allimg/" + part_path
    return uploads_path


def filter_more_imgs(text):
    '''
    过滤正文多余的图片：
    判断正文是否有图片，如果有则判断是否为一张以上，
    如果是则只保留最后一张图片，其他多余的图片全部删除
    :param text:
    :return:
        text 正文
        imgsrc 图片 URL 地址
        imgbq 图片的 <img> 标签

    # 以后根据需要可以使用 Python 图片裁剪、压缩 相关库
    # 参考 https://blog.csdn.net/qingyuanluofeng/article/details/50483812
    # https://blog.csdn.net/luolinll1212/article/details/82970978
    '''
    imgsrc = ''
    imgbq = ''
    soup = BeautifulSoup(text, "html5lib")
    img_arr = soup.select("img")
    if img_arr:
        imgsrc = img_arr[-1].get("src")
        # 上面的 get 操作会自动把 &amp; 转换成 & 所以需要替换回来
        imgsrc = imgsrc.replace('&', '&amp;')
        imgbq = img_arr[-1]
        if len(img_arr) > 1:
            for _ in img_arr[1:]:
                re_sub = "<img[^>]*>"
                text = re.sub(re_sub, "", text, count=1)

    else:
        print("没有图片")
    return text, imgsrc, imgbq


def post_dede(c_title, c_pubdate, c_content, domain, litpic="", tags="", keywords=""):
    '''
    DEDECMS POST 提交
    :param c_title: 标题
    :param c_pubdate: 发布日期
    :param c_content: 正文
    :param domain: 域名
    :param litpic: 缩略图
    :return:
    '''
    data = {
        # "channelid": 1, # 临时定义一个频道ID
        # "typeid": 4, # 临时定义一个栏目ID
        "title": c_title,
        "pubdate": c_pubdate,
        "body": c_content,
        "tags": tags,  # 标签
        "keywords": keywords,  # 关键词
        "litpic": litpic,
        "dopost": "save",
        "weight": 13,
        "autokey": 0,
        "remote": 0,
        "autolitpic": 0,
        "needwatermark": 1,
        "sptype": "hand",
        "spsize": 5,
        "notpost": 0,
        "click": random.randint(1000, 10000),  # 可使用随机数
        "sortup": 0,
        "arcrank": 0,
        "money": 0,
        "ishtml": 0,
        "imageField.x": 38,
        "imageField.y": 11,
        "dellink": 1
    }
    url = "http://" + domain + "/zlslhxpost/post_article.php?pw=a5s7sh4u"
    resp = requests.post(url, data=data)
    # print(resp.text)
    if "成功发布文章" in resp.text:
        pub_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        print("标题为： " + c_title + " 的文章成功发布到 " + domain + " 站点！", pub_time)
        return True
    else:
        print("标题为： " + c_title + " 的文章发布失败咯！！！")
        return False


def filter_pubdate(pubdate):
    '''
    过滤日期字符串两边的空字符
    :param pubdate:
    :return:
    '''
    pubdate = pubdate.strip()
    return pubdate


def merge_multiple_files(dirpath):
    """
    把目录中的多个文件合并到一个文件中。
    示例:
    "D:/WorkSpace/采集数据/百度相关搜索/组图/"
    "D:/WorkSpace/采集数据/百度相关搜索/朋友圈/"
    """
    kewords = []
    for root, sub_dirs, files in os.walk(dirpath):
        for file in files:
            file_path = dirpath + file
            with open(file_path, 'r', encoding='utf-8') as rf:
                lines = rf.readlines()
                for line in lines:
                    line = line.strip()
                    if line and (line not in kewords):
                        kewords.append(line)

    with open(dirpath + 'final.txt', 'a+', encoding='utf-8') as wf:
        kewords.sort()
        kdstr = "\n".join(kewords)
        wf.write(kdstr)


def parse_params(url, param_name):
    """
    本程序用于实现提取 URL 中的参数和值的功能
    url = "http://download.pinyin.sogou.com/dict/download_cell.php?id=1237&name=%E8%8D%AF%E5%93%81%E5%90%8D%E7%A7%B0%2B%E5%95%86%E5%93%81%E5%90%8D"
    """
    params = parse.urlparse(url).query
    param_arr = parse.parse_qs(params)
    param_value = param_arr[param_name]
    return param_value


# 指定子数组个数的方式分割数组
def list_split_num(arr, num):
    """

    :param arr: 待分割的数组
    :param num: 分成几个子数组
    :return:
    """
    arr_size = len(arr)  # 数组大小
    avg_len = math.ceil(arr_size / num)  # 子数组长度
    new_arr = [arr[i * avg_len:(i + 1) * avg_len] for i in range(0, num)]
    return new_arr


# 指定子数组长度的方式分割数组
def list_split(items, n):
    """
    :param items: 待分割的数组
    :param n: 每份子数组的数据长度
    :return:

    """
    return [items[i:i + n] for i in range(0, len(items), n)]


def arr_size(arr, size):
    """
    将数组 arr 分割成若干个数组块
    每个数组块的长度不超过 size 的大小
    :param arr: 要分割的数组
    :param size: 数组块的长度
    :return: 返回值是一个二维数组
    """
    arr_arr = []
    for i in range(0, int(len(arr)) + 1, size):
        temp = arr[i:i + size]
        if len(temp) > 0:
            arr_arr.append(temp)
    return arr_arr


def generator_file_one(filepath):
    '''
    读取大型文件，采用生成器的方式
    :param filepath: 文本路径
    :return i: 返回每行关键词
    '''
    with open(filepath, 'r', encoding='utf-8') as f:
        for i in f:
            i = i.replace("\r", '').replace("\n", '').strip()
            if i:
                yield i


def generator_file_arr(filepath, ncache=10000):
    """
    读取大型文件，采用生成器的方式
    :param filepath: 文本路径
    :param ncache: 缓存的大小
    :return caches: 返回缓存的数据
    """
    count = 0
    caches = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for i in f:
            count += 1
            if count % (ncache) != 0:
                i = i.replace("\r", '').replace("\n", '').strip()
                if i:
                    caches.append(i)
            else:
                yield caches
                caches = []
                count = 0
        yield caches


def filter_same_word(source_path, target_path):
    """
    去重文件中重复的词语或者关键词
    :param source_path: 需要去重的文本路径
    :param target_path: 去重后保存的文本路径
    :return: 无返回值
    """
    # 记录不重复的数据
    keywords = []
    # 分段打印数据
    clock = 0
    gfr = generator_file_arr(source_path, 20000)
    with open(target_path, 'a+', encoding='utf-8') as fw:
        for keyword_list in gfr:
            for keyword in keyword_list:
                if keyword in keywords:
                    continue
                else:
                    fw.write(keyword + '\n')
                    fw.flush()
                    keywords.append(keyword)
                clock += 1
                if clock % 5000 == 0:
                    print('>>> 已经处理了 {} 行的数据了！'.format(clock))
            print('>>> 已经处理了 {} 行的数据了！'.format(clock))


def get_md5(url):
    """
    计算 url 的 md5 值
    :param url: url 地址
    :return:
    """
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


pc_user_agent_arr = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    # 'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2', '',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
]

m_user_agent_arr = [
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'NOKIA5700/ UCWEB7.0.2.37/28/999',
    'Openwave/ UCWEB7.0.2.37/28/999',
    'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
]


def returnBaseConf():
    """
    返回对象的基本属性
    :return:
    """
    repeat_max = 100  # 设置连续重复网址的最大值 100
    repeat_num = 0  # 记录连续重复网址的数量
    post_success_num = 0  # 记录每次采集后发布成功的数量
    return repeat_max, repeat_num, post_success_num


# 发布内容到 SingleAllWebs 版本的蜘蛛池
def post_SingleAllWebs(c_keyword, fixed_title, changed_title, c_pubdate, c_content, domain):
    '''
    DEDECMS POST 提交
    :param c_title: 标题
    :param c_pubdate: 发布日期
    :param c_content: 正文
    :param domain: 域名
    :return:
    '''
    data = {
        # "channelid": 1, # 临时定义一个频道ID
        # "typeid": 4, # 临时定义一个栏目ID
        "keyword": c_keyword,
        "fixed_title": fixed_title,
        "changed_title": changed_title,
        "pubdate": c_pubdate,
        "body": c_content,
    }
    url = "http://" + domain + "/12_PostArticle.php?zlspw=Zls0592ZZC"
    resp = requests.post(url, data=data)
    # print(resp.text)
    if "蜘蛛池文章发布成功" in resp.text:
        pub_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        print("标题为： " + fixed_title + " 的文章成功发布到 " + domain + " 站点！", pub_time)
        return True
    else:
        print("标题为： " + fixed_title + " 的文章发布失败咯！！！")
        return False


def filter_img_url_suffix(img_file_path):
    '''
    把图片保存路径中的 ?xxx 过滤掉
    有时候采集的图片末尾为 1e68ccb8b0ef3816b4316bfdc0ba03b9.jpeg?imageView&thumbnail=550x0
    因此在保存时，需要把 ?imageView&thumbnail=550x0 给过滤掉
    :param img_file_path:
    :return:
    '''
    pat = re.compile("\?.*")
    img_file_path = pat.sub('', img_file_path)
    return img_file_path


def filter_all_html(html):
    '''
    过滤标题和正文中的所有的 html 标签
    :param html:
    :return:
    '''
    rex = re.compile(r'<[^>]+>', flags=re.I | re.S)
    html = rex.sub('', html)
    return html


def returnDictPath(dict_name):
    '''
    返回 dictionaries 分词字典的目录
    :param dict_name:
    :return:
    '''
    base_dir = returnBaseDir()
    dict_path = (base_dir + "/dictionaries/" + dict_name + "/").replace("\\", "/")
    return dict_path


def del_dir(dir_path):
    '''
    删除指定时间段的 MD5 文件夹
    :param dir_path:
    :return:
    '''
    dirs = list(os.listdir(dir_path))
    print("开始删除 15 天前的目录", dir_path)
    print("目录删除开始时间：", datetime.datetime.now().strftime(SQL_DATETIME_FORMAT))
    for i in range(len(dirs)):
        url_dir = dir_path + dirs[i]
        old_date = os.path.getmtime(url_dir)
        old_date_stamp = datetime.datetime.fromtimestamp(old_date).strftime('%Y-%m-%d')
        now_date = time.time()
        expire_days = (now_date - old_date) / 60 / 60 / 24
        if expire_days >= 15:  # 大于 15 天就删除
            try:
                os.rmdir(url_dir)
                print(old_date_stamp + "--->" + dirs[i] + "---> 目录成功删除！")
            except Exception as e:
                print(e)
    else:
        print("目录删除结束时间：", datetime.datetime.now().strftime(SQL_DATETIME_FORMAT))


def is_number(str):
    '''
    判断字符串是否全部都是数字
    :param str:
    :return:
    '''
    try:
        float(str)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(str)
        return True
    except (TypeError, ValueError):
        pass
    return False


def replace_qihoo360(str):
    # 字符串替换
    str = str.replace("【", "").replace("】", "").replace("_", "").replace("-", "").replace("|", "")
    str = str.replace("...", "").replace("\r", '').replace("\n", '').replace("\t", '').replace(' ', '')
    str = str.replace('&nbsp;', '').replace("发贴时间：", '').replace("[图文]", '').replace("  ", " ").strip()

    # 正则替换
    re_sub = "</?[^>]*>"
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    re_sub = "[ ]+"
    str = re.sub(re_sub, " ", str, flags=re.S | re.I)
    re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日-'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    str = str.replace('...', choice(['。', '？', '！']))
    re_sub = '\d{1,4}-\d{1,2}-\d{1,2}'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)

    str = str.strip()
    return str


def filter_one_imgs(text):
    '''
    把字符串中的图片替换为空，只替换一次
    :param text:
    :return:
        text 正文
    '''
    re_sub = "<img[^>]*>"
    text = re.sub(re_sub, "", text, count=1)
    return text


def get_image_extension(url):
    '''
    获取图片扩展名
    :param url:
    :return:
    '''
    image_ext = ".jpeg"
    ext_list = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.psd', '.tiff', '.tga', '.eps']
    for ext in ext_list:
        if ext in url.lower():
            image_ext = ext
            break

    return image_ext


def filter_out_a(text, web_host):
    '''
    过滤外部链接锚文本
    :param text: 字符串
    :param web_host:
        格式为 http://www.localhost.com
        或者 www.localhost.com
    :return: 返回过滤后的文本内容
    举例:

    这是一个<a href="www.baidu.com">百度</a>和一段包含其他超链接<a href="https://www.sohu.com/">搜狐</a>的一段演示的文本段落。

    提取所有的 a 链接
    <a href="www.baidu.com">百度</a>
    <a href="https://www.sohu.com/">搜狐</a>

    '''
    domain = ''
    domain_arr = web_host.split("//")
    if len(domain_arr) == 1:
        domain = domain_arr[0]
    elif len(domain_arr) == 2:
        domain = domain_arr[1]

    soup = BeautifulSoup(text, "html5lib")
    a_text_arr = soup.select("a")  # 过滤出文本里面的所有的 a 链接
    for atext in a_text_arr:  # 遍历所有的 a 链接
        href = atext.get("href")  # 获取每个 a 链接的 href 属性值
        if href.startswith("http"):  # 以 http 开头，说明可能是站外链接，也可能是站内的完整链接等两种情况
            if domain not in href:  # 如果 href 不包含本站的域名，说明是站外链接
                text = text.replace(str(atext), "")  # 把站外链接的 a 节点文本替换为空
    return text


def returnFileName(file):
    """
    非全站采集时使用，用来保存数据和采集的网址
    :param file:
    :return:
        file_name   文件名，不包括后缀
        dir_path_url    保存内容页 URL 的目录
        dir_path_txt    保存内容 URL 的 TXT 文件目录
        un_published_txt 保存未发布的 TXT 文件路径
        published_txt   保存已发布的 TXT 文件路径
    """
    base_dir = returnBaseDir()
    file_name = os.path.basename(file).replace(".py", '')
    dir_path_url = (base_dir + "/../UploadImageData/" + file_name + "/_1_url/").replace("\\", "/")
    dir_path_txt = (base_dir + "/../UploadImageData/" + file_name + "/_2_txt/").replace("\\", "/")
    un_published_txt = dir_path_txt + "un_published.txt"  # 保存未发布的 URL 地址
    published_txt = dir_path_txt + "published.txt"  # 保存已发布的 URL 地址
    collect_url_txt = dir_path_txt + "collect_url.txt"  # 保存未采集内容的 URL 地址
    return file_name, dir_path_url, dir_path_txt, un_published_txt, published_txt, collect_url_txt


def returnFileNameForQiYe(file):
    """
    全站采集时使用，用来保存数据和网址
    :param file:
    :return:
        file_name   文件名，不包括后缀
        cont_dir_path_url    保存内容页 URL 的目录
        other_dir_path_url      保存非内容页 URL 的目录
        cont_dir_path_txt    保存内容 URL 的 TXT 文件目录
        un_published_txt 保存未发布的 TXT 文件路径
        published_txt   保存已发布的 TXT 文件路径
        collect_url_txt     保存未采集内容的 URL 地址
    """
    base_dir = returnBaseDir()
    file_name = os.path.basename(file).replace(".py", '')

    # 内页 URL
    cont_dir_path_url = (base_dir + "/../UploadImageData/" + file_name + "/_c_url/").replace("\\", "/")
    # 非内页 URL
    other_dir_path_url = (base_dir + "/../UploadImageData/" + file_name + "/_o_url/").replace("\\", "/")
    # 内页 TXT 目录
    cont_dir_path_txt = (base_dir + "/../UploadImageData/" + file_name + "/_c_txt/").replace("\\", "/")
    # 非内页 TXT 目录
    other_dir_path_txt = (base_dir + "/../UploadImageData/" + file_name + "/_o_txt/").replace("\\", "/")

    un_published_txt = cont_dir_path_txt + "un_published.txt"  # 保存未发布的 URL 地址
    published_txt = cont_dir_path_txt + "published.txt"  # 保存已发布的 URL 地址
    collect_url_txt = cont_dir_path_txt + "collect_url.txt"  # 保存未采集内容的 URL 地址

    other_collect_url_txt = other_dir_path_txt + "collect_url.txt"  # 保存非内页的 URL 地址

    return file_name, cont_dir_path_url, other_dir_path_url, cont_dir_path_txt, other_dir_path_txt, \
           un_published_txt, published_txt, collect_url_txt, other_collect_url_txt


def returnBaseDir():
    '''
    返回项目根目录
    :return:
    '''
    base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    base_dir = base_dir.replace("\\", "/")
    return base_dir


def read_keyword(old_file_path, new_file_path):
    '''
    大文件关键词过滤
    :param old_file_path: 需要去重的文本路径
    :param new_file_path: 去重后的文本保存路径
    :return:
    '''
    # 大型文件读取器
    gen = generator_file(old_file_path)
    # 记录是否重复
    count = []
    # 开始查找判断关键词是否在之前出现过
    clock = 0
    with open(new_file_path, 'a+', encoding='utf-8') as f:
        for keyword in gen:
            if keyword in count:
                continue
            else:
                f.write(keyword + '\n')
                f.flush()
                count.append(keyword)
            clock += 1

            if clock % 5000 == 0:
                print('>>>已经处理了{}行的数据了'.format(clock))

        print('>>>已经处理了{}行的数据了'.format(clock))


def generator_file(filepath, ncache=10000):
    '''读取大型文件，采用生成器的方式
    输入：
    @filepath：文本的路径, 比如：D:/WorkSpace/Python/ScrapyUploadImageData/818ps_com_result.txt
    输出：
    @i：每行的关键词
    '''
    count = 0
    caches = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for i in f:
            count += 1
            if count % (ncache) != 0:
                i = i.replace("\r", '').replace("\n", '').strip()
                if i:
                    caches.append(i)
            else:
                yield caches
                caches = []
                count = 0
        yield caches
    # with open(filepath, 'r', encoding='utf-8') as f:
    #     for i in f:
    #         # 每行替换 - 并过滤字符后，如果不为空，则产生生成器
    #         ist = i.replace('-', '').strip()
    #         if ist:
    #             yield ist


def produce_paging_url(url, pageid, sepa='_'):
    '''
    产生内容页的分页链接
    :param url: 内容页的首页
    :param pageid: 分页的 ID 值
    :param sepa: 内容页 ID 和 分页 ID 的分隔符
    :return:
    '''
    if url.endswith(".html"):
        houzhui = ".html"
    elif url.endswith(".shtml"):
        houzhui = ".shtml"
    elif url.endswith(".htm"):
        houzhui = ".htm"
    else:
        houzhui = ""
    if len(houzhui) > 0:
        url_prefix = url.replace(houzhui, "")
        page = pageid
        url_suffix = sepa + str(page) + houzhui
        url_new = url_prefix + url_suffix
        return url_new
    else:
        return ''


def raplace_domains(str):
    '''
    把正文中包含的网址都替换为空
    '''
    fix_str = "jpg|jpeg|png|gif|bmp|psd|tiff|tga|eps|JPG|JPEG|PNG|GIF|BMP|PSD|TIFF|TGA|EPS"
    re_sub = "(http:\/\/|https:\/\/){0,1}(www.){0,1}[0-9a-zA-Z\-]+\.((?!" + fix_str + ")[a-zA-Z\.])+[\/]{0,1}"
    str = re.sub(re_sub, "", str, flags=re.S)
    return str


def raplace_domains_2(content, domain):
    '''
    把正文中包含的网址都替换为空
    本函数不建议使用注释中的正则方式匹配，容易出问题
    :return:
    因为图片 md5 为 32 个字符，所以需要用 {,30} 限制长度，才不会把图片也替换为空
    '''
    # fix_str = "jpg|jpeg|png|gif|bmp|psd|tiff|tga|eps|JPG|JPEG|PNG|GIF|BMP|PSD|TIFF|TGA|EPS"
    # re_sub = "(http:\/\/|https:\/\/){0,1}(www.){0,1}[0-9a-zA-Z\-]+\.((?!" + fix_str + ")[a-zA-Z\.])+[\/]{0,1}"
    # content = re.sub(re_sub, "", content, flags=re.S)
    # return content

    # 代码重写如下:
    # domain 为根域名

    second_domain = 'www.' + domain
    content = content.replace(second_domain, '').replace(domain, '')
    return content


def replace_qihoo360(str):
    # 字符串替换
    str = str.replace("【", "").replace("】", "").replace("_", "").replace("-", "").replace("|", "")
    str = str.replace("...", "").replace("\r", '').replace("\n", '').replace("\t", '').replace(' ', '')
    str = str.replace('&nbsp;', '').replace("发贴时间：", '').replace("[图文]", '').replace("  ", " ").strip()

    # 正则替换
    re_sub = "</?[^>]*>"
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    re_sub = "[ ]+"
    str = re.sub(re_sub, " ", str, flags=re.S | re.I)
    re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日-'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    re_sub = '\d{1,4}年\d{1,2}月\d{1,2}日'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)
    str = str.replace('...', choice(['。', '？', '！']))
    re_sub = '\d{1,4}-\d{1,2}-\d{1,2}'
    str = re.sub(re_sub, '', str, flags=re.S | re.I)

    str = str.strip()
    return str



if __name__ == '__main__':
    fulldomain = "https://er.snaji.siji.bai-du.org.cn/"
    print(get_host(fulldomain))
    print(get_name(fulldomain))
    print(get_root_domain(fulldomain))