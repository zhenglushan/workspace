# -*- coding:utf-8 -*-
import os, shutil


def arrange_keywords(file_dir):
    '''
    根据路径整理该路劲下所有目录里面的 keywords.txt 文件中的关键词
    keywords.txt 需要把第一行的 URL 过滤掉
    :param file_dir:
    :return:
    '''
    read_dir_arr = os.listdir(file_dir)
    for kw_dir in read_dir_arr:
        keywords_txt_path = file_dir + kw_dir + '/keywords.txt'
        # 判断关键词文件是否存在
        exist = os.path.exists(keywords_txt_path)
        if exist:
            kwfile = open(keywords_txt_path, "r")
            lines = kwfile.readlines()
            kwfile.close()
            if lines:
                lines.pop(0)
                lines_str = "\n".join(lines)
                lines_str = lines_str + "\n"
                with open("D:/WorkSpace/Python/ScrapyUploadImageData/818ps_com_result.txt", 'a+') as refile:
                    refile.write(lines_str)
            os.remove(keywords_txt_path)  # 删除文件
        shutil.rmtree(file_dir + kw_dir + '/')  # 删除文件夹


if __name__ == '__main__':
    file_dir = 'D:/WorkSpace/Python/ScrapyUploadImageData/818ps_com/'
    arrange_keywords(file_dir)
    print("关键词整理完成！")
