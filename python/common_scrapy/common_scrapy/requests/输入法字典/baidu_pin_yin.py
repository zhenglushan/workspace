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


class BaiduPinYinDict:
    cate_indexs = [
        'https://shurufa.baidu.com/dict_list?cid=157',  # 城市区划
        'https://shurufa.baidu.com/dict_list?cid=158',  # 理工行业
        'https://shurufa.baidu.com/dict_list?cid=317',  # 人文社会
        'https://shurufa.baidu.com/dict_list?cid=162',  # 电子游戏
        'https://shurufa.baidu.com/dict_list?cid=159',  # 生活百科
        'https://shurufa.baidu.com/dict_list?cid=163',  # 娱乐休闲
        'https://shurufa.baidu.com/dict_list?cid=165',  # 人名专区
        'https://shurufa.baidu.com/dict_list?cid=160',  # 文化艺术
        'https://shurufa.baidu.com/dict_list?cid=161',  # 体育运动
    ]

    dict_urls = []

    def __init__(self):
        resp = requests.get(self.cate_indexs[0], headers=headers)
        resp.encoding = 'UTF-8'
        response = HtmlResponse(url=self.cate_indexs[0], body=resp.text, encoding=resp.encoding)
        cate_index_arr = response.css('div.tag_ul.popup_list a::attr(href)')
        if cate_index_arr:
            for city_cate_index in cate_index_arr:
                city_cate_index = city_cate_index.extract().strip()
                city_cate_index = "https://shurufa.baidu.com" + city_cate_index
                self.cate_indexs.append(city_cate_index)
                sleep(1)

    def getDictUrl(self):
        for cate_index in self.cate_indexs:
            start = 1
            while True:
                cate_index_temp = cate_index + "&page=" + str(start)
                resp = requests.get(cate_index_temp, headers=headers)
                resp.encoding = 'UTF-8'
                response = HtmlResponse(url=cate_index_temp, body=resp.text, encoding=resp.encoding)
                # 匹配下一页 next_page
                if "分类没有找到相应词库" in resp.text:
                    break
                else:
                    # 输出当前采集的页面
                    print("当前采集分页为： " + cate_index_temp)
                    # 匹配 dict_url
                    dict_innerid_arr = response.css('a.dict-down.dictClick::attr(dict-innerid)')
                    if dict_innerid_arr:
                        for dict_innerid in dict_innerid_arr:
                            dict_innerid = dict_innerid.extract().strip()
                            dict_url = "https://shurufa.baidu.com/dict_innerid_download?innerid={}".format(dict_innerid)
                            if dict_url not in self.dict_urls:
                                self.dict_urls.append(dict_url)
                    start = start + 1
                sleep(1)
            sleep(1)
        # 把字典的地址都保存到 dict_url.txt 文件中
        with open("./baidu_dicts.txt", 'a+', encoding='utf-8') as dictf:
            dictf.write("\n".join(self.dict_urls))

    @staticmethod
    def downloadDictFile():
        with open("./baidu_dicts.txt", 'r', encoding='utf-8') as dictf:
            lines = dictf.readlines()
            lines_arr = arr_size(lines, 20)
            for temp_arr in lines_arr:
                line_thread = []
                for line in temp_arr:
                    line = line.strip("\n")
                    th = threading.Thread(target=BaiduPinYinDict.downloadDictFileReal, args=(line,))
                    line_thread.append(th)
                for th in line_thread:
                    th.start()
                    th.join()

    @staticmethod
    def downloadDictFileReal(line):
        # 提取文件名称
        params = parse.urlparse(line).query
        param_arr = parse.parse_qs(params)
        name = param_arr['innerid'][0].replace(' ', '+').replace(' ', '+')

        # 下载数据
        resp = requests.get(line, headers=headers)

        # 保存数据
        scel_path = "D:/WorkSpace/采集数据/输入法词库/百度拼音/bdict/" + name + ".bdict"
        if not os.path.exists(scel_path):
            with open(scel_path, 'wb') as dcf:
                print("当前正在保存 {}.bdict 文件……".format(name))
                dcf.write(resp.content)
        else:
            print("文件 {}.scel 已经采集过了！".format(name))


if __name__ == '__main__':
    # bpyd = BaiduPinYinDict()
    # bpyd.getDictUrl()
    BaiduPinYinDict.downloadDictFile()
