# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 请求方式操作谷歌翻译.py
# @DATETime   : 2020/4/23 14:15
# @Author     : 笑看风云


import os
import re
from ScrapyMongoDBForSearch.spiders_requests.翻译.谷歌翻译非API import Return_tk, split_text
import time
import html


def translate_body(body):
    # body 翻译开始
    body_arr = body.split("\n")
    body_arr_temp = ["┯" + tmstr.strip() + "┷" for tmstr in body_arr]
    body_arr = split_text(body_arr_temp, xianchang=1500)
    result_text = ""
    print("正文\t中文到英文的翻译过程……")
    for i, ti in enumerate(body_arr):
        ti = html.unescape(ti.strip())
        js = Return_tk()
        result = ""
        try:
            tk = js.getTk(ti)
            result = js.zn_to_en_translate(ti, tk)
        except:
            print(file_path + "\t正文\t翻译出现异常情况，跳过去……")
            print("待翻译的\t正文\t内容为：\n")
            print(ti + "\n\n")
        print("第 " + str(i + 1) + " 次翻译……")
        result_text = result_text + result
        time.sleep(3)
    print(result_text)
    result_text = result_text.replace('┷', '┷\n')
    result_text_arr = result_text.split("\n")
    body_arr = result_text_arr[0:-1]
    body_arr = split_text(body_arr, xianchang=1500)
    result_text = ""
    print("正文\t英文到中文的翻译过程……")
    for i, ti in enumerate(body_arr):
        ti = html.unescape(ti.strip())
        js = Return_tk()
        result = ""
        try:
            tk = js.getTk(ti)
            result = js.en_to_zn_translate(ti, tk)
        except:
            print(file_path + "\t正文\t翻译出现异常情况，跳过去……")
            print("待翻译的\t正文\t内容为：\n")
            print(ti + "\n\n")
        print("第 " + str(i + 1) + " 次翻译……")
        result_text = result_text + result
        time.sleep(3)
    print(result_text)
    result_text = result_text.replace("┯", "").replace("┷", "\n")
    # body 翻译结束
    return result_text


def translate_title(title):
    # title 翻译开始
    title = html.unescape(title)  # 把 &;实体 转换成字符
    js = Return_tk()
    print("标题\t中文到英文的翻译过程……")
    try:
        tk = js.getTk(title)
        title = js.zn_to_en_translate(title, tk)
    except:
        print(file_path + "\t标题\t翻译出现异常情况，跳过去……")
        print("待翻译的\t标题\t内容为：\n")
        print(title + "\n\n")
        title = ""
    time.sleep(3)
    print("标题\t英文到中文的翻译过程……")
    try:
        tk = js.getTk(title)
        title = js.en_to_zn_translate(title, tk)
    except:
        print(file_path + "\t标题\t翻译出现异常情况，跳过去……")
        print("待翻译的\t标题\t内容为：\n")
        print(title + "\n\n")
        title = ""
    time.sleep(3)
    # title 翻译结束
    return title


if __name__ == "__main__":
    source_dir = "D:/WorkSpace/数据采集/鱼摆摆网/原文/"
    translate_dir = "D:/WorkSpace/数据采集/鱼摆摆网/译文/"

    list_files = os.listdir(source_dir)

    for file in list_files:
        file_path = source_dir + file
        translate_file_path = translate_dir + file
        if not os.path.exists(translate_file_path):
            with open(file_path, 'r', encoding='UTF-8') as f:
                txt_str = f.read().strip()
                re_sub = "\[ZLSLHX\]\n\[ZLSLHX\]"
                txt_str_arr = re.split(re_sub, txt_str)
                url = txt_str_arr[0]
                title = txt_str_arr[1]
                body = txt_str_arr[2]
                title = translate_title(title)  # 翻译标题
                body = translate_body(body)  # 翻译正文
                # 翻译结果写入文件
                with open(translate_file_path, mode="a+", encoding="UTF-8") as fw:
                    fw.write(url + "[ZLSLHX]\n[ZLSLHX]" + title.strip() + "[ZLSLHX]\n[ZLSLHX]" + body.strip())
            print(file_path + "\t翻译完成！")
            time.sleep(1)
        else:
            print("文件已经翻译过了……")
