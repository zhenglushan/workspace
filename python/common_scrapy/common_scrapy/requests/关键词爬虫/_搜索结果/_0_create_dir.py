# -*- coding:utf-8 -*-
import os
import hashlib
import datetime
from threading import Thread
from scrapy_mongodb_for_search.settings import SQL_DATETIME_FORMAT

'''
D:/WorkSpace/Python/ScrapyUploadImageData
	/关键词
		/私家侦探
			/私家侦探
			/私人侦探
				/图片
				/采集
					/关键词MD5值
						/keyword.txt
						/baidu_title.txt
						/baidu_content.txt
						/qihoo_title.txt
						/qihoo_content.txt
						/sogou_title.txt
						/sogou_content.txt
			/商务调查
			/小三调查
		/代孕
			/词根:代孕
			/助孕
			/代怀孕
				/图片
				/采集
					/关键词MD5值
						/keyword.txt
						/baidu_title.txt
						/baidu_content.txt
						/qihoo_title.txt
						/qihoo_content.txt
						/sogou_title.txt
						/sogou_content.txt
'''
'''
未采集和未发布中，如果三个搜索引擎都采集了，则把未采集的当前文件夹设置为隐藏属性，
在未发布中的文件夹，在发布后的也设置为隐藏属性。
不读取隐藏属性的文件夹，只读取可见的文件夹。
采集时，先读取路径。
通过设置文件夹的隐藏和权限来过滤采集和发布的问题。
'''
read_dir = "D:/WorkSpace/Python/ScrapyUploadImage/ScrapyUploadImage/关键词文件/2、拆分指数/"
create_dir = "D:/WorkSpace/Python/ScrapyUploadImageData/关键词/"


def md5_utf8_str(str):
    '''
    把 utf8 字符串转换成 MD5 值
    :param str:
    :return:
    '''
    m = hashlib.md5()
    m.update(str.encode('utf8'))
    # print(m.hexdigest())
    return m.hexdigest()


def md5_gbk_str(str):
    '''
    把 gbk 字符串转换成 MD5 值
    :param str:
    :return:
    '''
    m = hashlib.md5(str.encode(encoding='gb2312'))
    # print(m.hexdigest())
    return m.hexdigest()


def create_level_one_dir():
    '''
    创建关键词目录
    :return:
    '''
    read_dir_arr = os.listdir(read_dir)
    for keyword in read_dir_arr:
        keyword = keyword.strip()
        create_keyword_dir = create_dir + keyword + "/"
        exist = os.path.exists(create_keyword_dir)
        if not exist:
            os.makedirs(create_keyword_dir, mode=0o777)
            print(keyword + " 关键词目录创建成功！")
        else:
            print(keyword + " 关键词目录已经存在，跳过创建！")
    return read_dir_arr


def create_level_two_dir():
    '''
    创建关键词子分类文件对应的目录,以及图片和采集的子目录
    :return:
    '''
    keyword_txt_file_paths = []  # 保存关键词子分类文件路径的数组
    create_keyword_txt_dirs = []  # 保存创建的子分类文件对应的目录的数组
    read_dir_arr = create_level_one_dir()
    for keyword in read_dir_arr:
        read_keyword_dir = read_dir + keyword + "/"
        keyword_txt_files = os.listdir(read_keyword_dir)
        for keyword_txt_file in keyword_txt_files:
            keyword_txt_file = keyword_txt_file.strip()
            # 关键词子分类文件路径
            keyword_txt_file_path = read_keyword_dir + keyword_txt_file
            keyword_file = keyword_txt_file.strip('.txt')
            create_keyword_txt_dir = create_dir + keyword + "/" + keyword_file + "/"
            exist = os.path.exists(create_keyword_txt_dir)
            if not exist:
                os.makedirs(create_keyword_txt_dir, mode=0o777)
                # 图片目录
                pic_dir = create_keyword_txt_dir + "图片/"
                os.makedirs(pic_dir, mode=0o777)
                # 采集目录
                caiji_dir = create_keyword_txt_dir + "采集/"
                os.makedirs(caiji_dir, mode=0o777)
                print(keyword + "---> 关键词子分类文件 " + keyword_txt_file + " 对应的目录创建成功！")
                keyword_txt_file_paths.append(keyword_txt_file_path)
                create_keyword_txt_dirs.append(create_keyword_txt_dir)
            else:
                print(keyword + "---> 关键词子分类文件 " + keyword_txt_file + " 对应的目录，跳过创建！")
    return keyword_txt_file_paths, create_keyword_txt_dirs


def create_level_three_dir_thread():
    '''
    创建关键词子分类文件中的关键词对应的目录 多线程
    :return:
    '''
    keyword_txt_file_paths, create_keyword_txt_dirs = create_level_two_dir()
    if len(keyword_txt_file_paths) > 0:
        line_threads = []
        for key, txt_file_path in enumerate(keyword_txt_file_paths):
            wordfile = open(txt_file_path, 'r', encoding='UTF-8')
            while True:
                lines = wordfile.readlines(10000)  # 每次读取 10000 行关键词
                if not lines:
                    break
                for line in lines:
                    line = line.strip()
                    if len(line) > 0:
                        line = filter_dot(line)
                        line = line.replace('-', '').replace('"', '').strip()
                        keyword_line_dir = create_keyword_txt_dirs[key] + "采集/" + md5_utf8_str(line) + "/"
                        line_thread = Thread(target=create_level_three_dir, args=(keyword_line_dir, line))
                        line_threads.append(line_thread)
                if line_threads:
                    for lt in line_threads:
                        lt.start()
                    for lt in line_threads:
                        lt.join()
                    line_threads = []


def filter_dot(word):
    '''
    处理类似于 直播足球比赛,4316,23400000,0,0,0,-,5,29,14 这样的字符串
    测试地址:
    ScrapyUploadImage.tools.test.nine_5119_dot.filter_dot
    :param word:
    :return:
    '''
    if len(word) > 0:
        word_split_arr = word.split(',')
        if len(word_split_arr) > 9:
            word_split_arr = word_split_arr[0:-9]
            final_str = ''.join(word_split_arr)
            return final_str
        else:
            return word


def create_level_three_dir(dir, keyword):
    '''
    创建关键词子分类文件中的关键词对应的目录
    :return:
    '''
    try:
        exist = os.path.exists(dir)
        if not exist:
            os.makedirs(dir, mode=0o777)
            print("关键词子分类文件中的关键词 " + keyword + " 对应的 md5 目录创建成功！")
            keyword_file_path = dir + "keyword.txt"
            if not os.path.exists(keyword_file_path):
                with open(keyword_file_path, mode='a', encoding='utf-8') as kf:
                    kf.write(keyword)
                    print("===》并创建 " + keyword + " 对应的 keyword.txt 文件！")
        else:
            print("关键词子分类文件中的关键词 " + keyword + " 对应的 md5 目录已存在！")
    except:
        print("关键词子分类文件中的关键词 " + keyword + " 对应的 md5 目录已存在！")


if __name__ == '__main__':
    all_time_start = "目录创建的开始时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    create_level_three_dir_thread()
    all_time_end = "目录创建的结束时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    print(all_time_start)
    print(all_time_end)
