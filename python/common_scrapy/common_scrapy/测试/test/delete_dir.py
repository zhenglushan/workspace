# -*- coding:utf-8 -*-

import shutil
import os
from threading import Thread
import datetime
from ScrapyUploadImage.settings import SQL_DATETIME_FORMAT


def read_dir(dir):
    thread_arr = []
    one_level_kw = os.listdir(dir)
    for one_kw in one_level_kw:
        one_kw_dir = dir + one_kw + "/"
        two_level_kw = os.listdir(one_kw_dir)
        for two_kw in two_level_kw:
            two_kw_dir = one_kw_dir + two_kw + "/"
            caiji_dir = two_kw_dir + "采集/"
            tupian_dir = two_kw_dir + "图片/"
            line_thread = Thread(target=delete_dir, args=(caiji_dir,))
            thread_arr.append(line_thread)
            line_thread = Thread(target=delete_img, args=(tupian_dir,))
            thread_arr.append(line_thread)
    for td in thread_arr:
        td.start()
    for td in thread_arr:
        td.join()


def delete_img(dir):
    '''
    删除目录下的所有文件 和 当前目录
    :param dir:
    :return:
    '''
    shutil.rmtree(dir)


def delete_dir(dir):
    '''
    删除 关键词 这个目录及其里面的子目录和文件
    :return:
    '''
    cont_md5 = os.listdir(dir)
    for cont_dir in cont_md5:
        cont_dir_t = dir + cont_dir + "/"
        shutil.rmtree(cont_dir_t)
        # print("正在删除的目录为：" + cont_dir_t)
    shutil.rmtree(dir)


if __name__ == "__main__":
    top = "D:/WorkSpace/Python/ScrapyUploadImageData/关键词/"
    all_time_start = "目录删除的开始时间 ：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    read_dir(top)
    all_time_end = "目录删除的结束时间：" + datetime.datetime.now().strftime(SQL_DATETIME_FORMAT) + "\n"
    print(all_time_start)
    print(all_time_end)
