# -*- coding:utf-8 -*-

import re
import jieba
import os
import datetime
from random import randint, choice, sample, shuffle
from ScrapyMongoDBForSearch.工具.通用工具 import post_dede
from ScrapyMongoDBForSearch.settings import SQL_DATETIME_FORMAT
from ScrapyMongoDBForSearch.工具.分词工具 import FenCi
from ScrapyMongoDBForSearch.工具.数据库工具 import get_MongoDB_DataBase


# 上传正文中的全部图片
class PublishSuperMorePic():

    def __init__(self, keyword, webs):
        self.keyword = keyword

        # 选择图片数据
        image_url_arr = self.do_select_image()

        # 选择一定量的数据
        # results 的大小就是下面 for 循环发布的次数
        results = self.do_select(randint(100, 120))  # randint(10, 20) randint(4, 8)

        if results:
            for result in results:
                # 图片数据随机排序
                shuffle(image_url_arr)
                # 处理每条数据
                word = result[0]
                titles = result[1]
                jianjies = result[2]

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

                # 组成 changed_title 标题
                if len(title_arr) >= 10:
                    changed_title_arr = sample(title_arr, 10)
                else:
                    changed_title_arr = title_arr
                changed_title = "".join(changed_title_arr)
                if len(title_arr) >= 10:
                    changed_title = title + changed_title
                changed_title = changed_title.replace('.', '').replace(':', '').replace('：', '').replace('|', '') \
                    .replace('-', '').replace('_', '').replace(';', '')
                changed_title = changed_title.replace("\\", '')
                changed_title_arr_temp = []
                result = jieba.cut(changed_title)
                for item in result:
                    item = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", item)
                    if len(item.strip()) > 0:
                        changed_title_arr_temp.append(item)
                changed_title = "|".join(changed_title_arr_temp)  # 使用普通分词

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
                        ins_img = '/uploads/allimg/' + ins_img
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
                keywords = tags
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
                        # def post_dede(c_title, c_pubdate, c_content, domain, litpic="", tags="", keywords="")
                        result = post_dede(title, pub_date, paragraph_final, rand_web, lit_pic_path, tags,
                                           keywords)  # 发布操作
                        # result = post_SingleAllWebs(
                        #     c_keyword=word,
                        #     fixed_title=,
                        #     changed_title=changed_title,
                        #     c_pubdate=,
                        #     c_content=,
                        #     domain=
                        # )  # 发布操作
                    except Exception as e:
                        print(title + " 文章因为异常而导致发布失败！" + "\n")
                    else:
                        if result:
                            pass
                        else:
                            print(title + " 文章提交后发布失败！" + "\n")

    def get_mongodb_connection(self):
        mg_database = get_MongoDB_DataBase()
        return mg_database

    def do_select_image(self):
        '''
        选择图片
        :return:
        '''
        image_urls_dir = "D:/WorkSpace/又拍云/keywords/" + self.keyword + "/"
        image_urls = os.listdir(image_urls_dir)
        return image_urls

    def do_select(self, size):
        '''
        选择内容
        :param size:
        :return:
        '''
        doc_arr = []
        mg_database = self.get_mongodb_connection()
        mg_collec = mg_database[self.keyword + "_" + self.keyword + "长尾词"]
        doc_part = mg_collec.aggregate([
            {'$match': {'bd_body': {'$exists': True}, 'bd_title': {'$exists': True}}},
            {'$sample': {'size': size}}
        ])
        for doc in doc_part:
            doc_temp = []
            keyword = doc['keyword'].strip()
            bd_title = doc['bd_title'].strip()
            bd_body = doc['bd_body'].strip()
            # print(str(id) + "~~~~~~" + keyword + "~~~~~~" + bd_title[0:20] + "~~~~~~" + bd_body[0:20])
            doc_temp.append(keyword)
            doc_temp.append(bd_title)
            doc_temp.append(bd_body)
            doc_arr.append(doc_temp)
        return doc_arr


if __name__ == '__main__':

    # 发布地址为： http://www.singleallwebs.com/12_PostArticle.php?pw=a5s7sh4u

    web_sites = {
        '壮阳': [
            'www.sylfx.com',
        ],
        '伴游': [
            'www.xfwdg.com',
        ],
        '试管婴儿': [
            'www.hczgc.com',
        ],
        '月子中心': [
            'www.bfhsf.com',
        ],
        '婚纱摄影': [
            'www.ahfxo.com',
        ],
    }

    is_publish = True  # 控制是否发布 True False

    if is_publish:  # 控制是否发布
        all_time_start = "关键词站点发布开始时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
        for keyword in web_sites.keys():
            webs = web_sites[keyword]
            webs_num = len(webs)
            print("开始给 -> " + keyword + " <- 的所有站点 " + str(webs) + " 进行内容发布： ")
            for _ in range(webs_num * 3):
                PublishSuperMorePic(keyword, webs)
        all_time_end = "关键词站点发布结束时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
        print(all_time_start)
        print(all_time_end)
