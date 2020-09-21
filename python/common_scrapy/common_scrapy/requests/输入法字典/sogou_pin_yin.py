# -*- coding:utf-8 -*-
# @ProjectName: ScrapyUploadImage
# @Email	  : 276517382@qq.com
# @FileName   : PinYin.py
# @DATETime   : 2019/12/15 16:00
# @Author     : 笑看风云

import re, os
from urllib import parse
import requests
import threading
from scrapy.http import HtmlResponse
from time import sleep
from scrapy_mongodb_for_search.my_tools.common import generator_file_arr,arr_size,get_md5

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


class SogouPinYinDict:
    cate_indexs = [
        'https://pinyin.sogou.com/dict/cate/index/360',  # 城市信息
        'https://pinyin.sogou.com/dict/cate/index/1',  # 自然科学
        'https://pinyin.sogou.com/dict/cate/index/76',  # 社会科学
        'https://pinyin.sogou.com/dict/cate/index/96',  # 工程应用
        'https://pinyin.sogou.com/dict/cate/index/127',  # 农林渔畜
        'https://pinyin.sogou.com/dict/cate/index/132',  # 医学医药
        'https://pinyin.sogou.com/dict/cate/index/436',  # 电子游戏
        'https://pinyin.sogou.com/dict/cate/index/154',  # 艺术设计
        'https://pinyin.sogou.com/dict/cate/index/389',  # 生活百科
        'https://pinyin.sogou.com/dict/cate/index/367',  # 运动休闲
        'https://pinyin.sogou.com/dict/cate/index/31',  # 人文科学
        'https://pinyin.sogou.com/dict/cate/index/403',  # 娱乐休闲
    ]

    dict_urls = []
    count = 1

    def __init__(self):
        resp = requests.get(self.cate_indexs[0], headers=headers)
        resp.encoding = 'UTF-8'
        response = HtmlResponse(url=self.cate_indexs[0], body=resp.text, encoding=resp.encoding)
        cate_index_arr = response.css('div.cate_no_child.citylistcate.no_select a.citylist::attr(href)')
        if cate_index_arr:
            for city_cate_index in cate_index_arr:
                city_cate_index = city_cate_index.extract().strip()
                city_cate_index = "https://pinyin.sogou.com" + city_cate_index
                self.cate_indexs.append(city_cate_index)
                sleep(1)

    def getDictUrl(self):
        for cate_index in self.cate_indexs:
            has_next_page = True
            start = 1
            while has_next_page:
                cate_index_temp = cate_index + "/default/" + str(start)
                resp = requests.get(cate_index_temp, headers=headers)
                resp.encoding = 'UTF-8'
                response = HtmlResponse(url=cate_index_temp, body=resp.text, encoding=resp.encoding)
                # 输出当前采集的页面
                print("当前采集分页为： " + cate_index_temp)
                # 匹配 dict_url
                dict_url_arr = response.css('div.dict_detail_show div.dict_dl_btn a::attr(href)')
                if dict_url_arr:
                    for dict_url in dict_url_arr:
                        dict_url = dict_url.extract().strip()
                        if dict_url not in self.dict_urls:
                            self.dict_urls.append(dict_url)
                # 匹配下一页 next_page
                if "下一页" in resp.text:
                    start = start + 1
                else:
                    has_next_page = False
                sleep(1)
            sleep(1)
        # 把字典的地址都保存到 dict_url.txt 文件中
        with open("./sogou_dicts.txt", 'a+', encoding='utf-8') as dictf:
            dictf.write("\n".join(self.dict_urls))

    @staticmethod
    def downloadDictFile_1():
        with open("./sogou_dicts.txt", 'r', encoding='utf-8') as dictf:
            lines = dictf.readlines()
            for line in lines:
                line = line.strip("\n")
                # 提取文件名称
                params = parse.urlparse(line).query
                param_arr = parse.parse_qs(params)
                name = param_arr['name'][0].replace(' ', '+').replace(' ', '+')
                # 下载数据
                resp = requests.get(line, headers=headers)
                # 保存数据
                with open("D:/WorkSpace/采集数据/输入法词库/搜狗拼音/scel/" + name + ".scel", 'wb') as dcf:
                    print("当前正在保存 {}.scel 文件……".format(name))
                    dcf.write(resp.content)
                sleep(1)

    @staticmethod
    def downloadDictFile_2():
        with open("./sogou_dicts.txt", 'r', encoding='utf-8') as dictf:
            lines = dictf.readlines()
            lines_arr = arr_size(lines, 20)
            for temp_arr in lines_arr:
                line_thread = []
                for line in temp_arr:
                    line = line.strip("\n")
                    th = threading.Thread(target=SogouPinYinDict.downloadDictFileReal, args=(line,))
                    line_thread.append(th)
                for th in line_thread:
                    th.start()
                    th.join()

    @staticmethod
    def downloadDictFileReal(line):
        # 提取文件名称
        name = get_md5(line)
        # params = parse.urlparse(line).query
        # param_arr = parse.parse_qs(params)
        # name = param_arr['name'][0].replace(' ', '+').replace(' ', '+')
        # name_new = str(SogouPinYinDict.count) + '_' + name
        # SogouPinYinDict.count = SogouPinYinDict.count + 1

        # 下载数据
        resp = requests.get(line, headers=headers)

        # 保存数据
        scel_path = "D:/WorkSpace/采集数据/输入法词库/搜狗拼音/scel/" + name + ".scel"
        if not os.path.exists(scel_path):
            with open(scel_path, 'wb') as dcf:
                print("当前正在保存 {}.scel 文件……".format(name))
                dcf.write(resp.content)
        else:
            print("文件 {}.scel 已经采集过了！".format(name))


if __name__ == '__main__':
    # sgpd = SogouPinYinDict()
    # sgpd.getDictUrl()
    SogouPinYinDict.downloadDictFile_2()
