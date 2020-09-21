# -*- coding:utf-8 -*-
'''
使用百度搜索结果来发布内容
'''

'''
import sys
import os
在 VSCode 中运行 Scrapy Django 等项目时，以下三行代码是必须的，
每个执行文件中都需要增加如下三行代码
pro_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
pro_path = os.path.abspath(os.path.join(pro_path,".."))
pro_path = os.path.abspath(os.path.join(pro_path,".."))
sys.path.append(pro_path)
'''

import datetime

from random import randint, choice, sample, shuffle
from scrapy_mongodb_for_search.settings import SQL_DATETIME_FORMAT
from scrapy_mongodb_for_search.spiders_requests.search_result._step._0_search_result_config import web_sites_mongdb
from scrapy_mongodb_for_search.spiders_requests.search_result._step.MongoDBService import get_MongoDB_DataBase

from scrapy_mongodb_for_search.my_tools.tools.fenci import FenCi
from scrapy_mongodb_for_search.my_tools.tools.commons import post_dede

database = get_MongoDB_DataBase()


class SearchResultPublish():

    def __init__(self, keyword, webs):
        self.keyword = keyword
        self.coll_name = keyword + "_" + keyword + "长尾词"
        self.image_dir = keyword + '_' + 'images'  # 配置图片文件夹
        # 选择图片数据
        image_url_arr = self.do_select_image()  # 获得图片名称数组
        '''
        如下格式：
        比特币/5ad889b957f9b1b447cd79a5dca1c2c7.jpeg[ips]比特币/f4e275475fc2aa0fd3f3053d2b8caaa8.jpg[ips]比特币/5cf4267d8165db0f981ba9543b8e2658.jpg[ips]
        文件夹: D:\WorkSpace\又拍云\keywords\比特币
        '''

        # 选择一定量的数据
        keyword_arr, bd_title_arr, bd_body_arr = self.do_select(randint(20, 30))  # randint(10, 20) randint(4, 8)
        if bd_body_arr:
            results = bd_body_arr  # 继续完善
            for result in results:
                # 图片数据随机排序
                shuffle(image_url_arr)
                # 处理每条数据
                id = result[0]
                word = result[1]
                titles = result[2]
                jianjies = result[3]
                # 分割 titles 并对数组随机排序
                title_arr = titles.split('[tt]')
                title_arr_temp = [t for t in title_arr if len(t.strip()) > 5]
                title_arr = title_arr_temp
                shuffle(title_arr)
                # 分割 jianjies 并对数组随机排序
                jianjie_arr = jianjies.split('[bd]')
                jianjie_arr_temp = [t for t in jianjie_arr if len(t.strip()) > 5]
                jianjie_arr = jianjie_arr_temp
                shuffle(jianjie_arr)
                # 判断标题和正文是否正常, 不正常则跳过发布的步骤
                if len(titles.strip()) == 0 or len(title_arr) < 5:
                    continue
                if len(jianjies.strip()) == 0 or len(jianjie_arr) < 5:
                    continue
                # 组成标题, 随机取两个元素组成新的标题
                title_2_arr = sample(title_arr, 2)
                title = "".join(title_2_arr)
                title = title.replace('.', '').replace(':', '').replace('：', '').replace('|', '') \
                    .replace('-', '').replace('_', '').replace(';', '')
                title = title.replace("\\", '')
                # print(title[0:randint(15, 25)])
                # print(title)
                # 组成文章 paragraph_num 是指段落数量 包括内容和图片
                paragraph_num = randint(5, 10)
                paragraph_mark = []
                paragraph_arr = []
                one_num = 0  # 需要几个图片
                two_num = 0  # 需要几个段落的内容
                for _ in range(0, paragraph_num):
                    mark = randint(1, paragraph_num)
                    if mark == 1:
                        paragraph_mark.append(1)  # 为 1 则配置 图片
                        one_num = one_num + 1
                    else:
                        paragraph_mark.append(2)  # 为 2 则配置 内容
                        two_num = two_num + 1
                # 平均每个段落最多可以配置多少个句子
                ave_cent_num = len(jianjie_arr) // (paragraph_num * 2)
                images_for_one = sample(image_url_arr, one_num)
                # print(paragraph_mark)
                # 提取缩略图
                lit_pic_path = ''
                for mark in paragraph_mark:
                    if mark == 1:
                        ins_img = images_for_one.pop()
                        # 替换图片路径
                        ins_img = ins_img.replace(keyword, '/uploads/allimg')
                        lit_pic_path = ins_img
                        temp = '<p class="img-center"><img src="' + ins_img + '" /></p>'
                    else:
                        temp = ''
                        tem = ''
                        if ave_cent_num >= 3:
                            cent_num = randint(3, ave_cent_num)
                        else:
                            cent_num = randint(ave_cent_num, 3)
                        for _ in range(0, cent_num):
                            if len(jianjie_arr) > 0:
                                tem = tem + jianjie_arr.pop()
                                tem = tem.replace("\\", '')
                        if len(tem) > 0:
                            temp = '<p>' + tem + '</p>'
                    paragraph_arr.append(temp)
                paragraph_final = ''.join(paragraph_arr)
                # 输出 标题 和 段落
                # print(title)
                # print(paragraph_final)
                # print('------------------------------------')
                # 进行分词
                fenci = FenCi(paragraph_final, keyword)
                tags, kw_list, paragraph_final = fenci.returnValues()
                # 服务器免登陆提交文件需要提取 tags 和 keywords 字段的值
                # print(tags)
                # print(kw_list)
                # print(paragraph_final)
                # print('------------------------------------')
                # 随机选择站点发布
                pub_date = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
                rand_web = choice(webs)
                # print(rand_web)
                if len(title) > 0:
                    try:
                        result = post_dede(c_title=title, c_pubdate=pub_date, c_content=paragraph_final,
                                           domain=rand_web, litpic=lit_pic_path, tags='', keywords='')  # 发布操作
                    except Exception as e:
                        print(title + " 文章因为异常而导致发布失败！" + "\n")
                    else:
                        if result:
                            print(title + " 文章提交后发布成功！" + "\n")
                        else:
                            print(title + " 文章提交后发布失败！" + "\n")

    def do_select_image(self):
        '''
        将调整为通过 keyword 从对应的图片文件夹读取图片地址
        并把所有图片地址生成临时 txt 文件，方便使用。
        并返回图片数组,
        :param keyword:
        :return: image_url_arr
        '''
        image_url_arr = [self.keyword]
        return image_url_arr

    def do_select(self, size):
        '''
        获取 MongoDB 数据库中的内容
        :param size: 选择多少条记录
        :return:
        '''
        try:
            keyword_arr = []
            bd_title_arr = []
            bd_body_arr = []
            collcetion = database[self.coll_name]
            doc_part = collcetion.aggregate([
                {'$match': {'bd_body': {'$exists': True}}},
                {'$sample': {'size': size}}
            ])
            for doc in doc_part:
                keyword = doc['keyword'].strip()
                bd_title = doc['bd_title'].strip()
                bd_body = doc['bd_body'].strip()
                if bd_body:
                    keyword_arr.append(keyword)
                    bd_title_arr.append(bd_title)
                    bd_body_arr.append(bd_body)
        except:
            return None, None, None
        else:
            return keyword_arr, bd_title_arr, bd_body_arr


if __name__ == '__main__':
    all_time_start = "关键词站点发布开始时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    for data in web_sites_mongdb:
        coll_arr = []
        web_arr = []
        for param in data:
            if "." in param:
                web_arr.append(param)
            else:
                coll_arr.append(param)
        print(coll_arr)  # 可注释掉
        print(web_arr)  # 可注释掉

        print("------------------------")
    all_time_end = "关键词站点发布结束时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    print(all_time_start)
    print(all_time_end)

    #
    # for keyword in web_sites_mongdb.keys():
    #     webs = web_sites_mongdb[keyword]
    #     print("开始给 -> " + keyword + " <- 的所有站点 " + str(webs) + " 进行内容发布： ")
    #     SearchResultPublish(keyword, webs)
    #     break
