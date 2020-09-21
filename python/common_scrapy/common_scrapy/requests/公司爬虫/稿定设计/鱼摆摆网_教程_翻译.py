# -*- coding:utf-8 -*-
# @ProjectName: scrapy_mongodb_for_search
# @Email	  : 276517382@qq.com
# @FileName   : 鱼摆摆网_教程_翻译.py
# @DATETime   : 2020/4/16 17:58
# @Author     : 笑看风云
import os
import re
from scrapy_mongodb_for_search.spiders.公司爬虫.公共工具._google import Return_tk
import time

if __name__ == "__main__":
    source_dir = "D:/WorkSpace/数据采集/鱼摆摆网/原文/"
    translate_dir = "D:/WorkSpace/数据采集/鱼摆摆网/译文/"

    list_files = os.listdir(source_dir)

    for file in list_files:
        file_path = source_dir + file
        translate_file_path = translate_dir + file
        if not os.path.exists(translate_file_path):
            try:
                with open(file_path, 'r', encoding='UTF-8') as f:
                    txt_str = f.read().strip()
                    re_sub = "\[ZLSLHX\]\n\[ZLSLHX\]"
                    txt_str_arr = re.split(re_sub, txt_str)
                    url = txt_str_arr[0]
                    title = txt_str_arr[1]
                    # title 翻译开始
                    title = title.replace("&amp;", "&")
                    js = Return_tk()
                    tk = js.getTk(title)
                    title = js.zn_to_en_translate(title, tk)
                    time.sleep(2)
                    tk = js.getTk(title)
                    title = js.en_to_zn_translate(title, tk)
                    time.sleep(2)
                    # title 翻译结束
                    body = txt_str_arr[2]
                    body_arr = body.split("\n")
                    body_arr_new = []
                    for temp_body in body_arr:
                        temp_body = temp_body.replace("&amp;", "&")
                        js = Return_tk()
                        tk = js.getTk(temp_body)
                        temp_body = js.zn_to_en_translate(temp_body, tk)
                        time.sleep(2)
                        tk = js.getTk(temp_body)
                        temp_body = js.en_to_zn_translate(temp_body, tk)
                        time.sleep(2)
                        body_arr_new.append(temp_body)
                    body_new = "\n".join(body_arr_new)
                    with open(translate_file_path, mode="a+", encoding="UTF-8") as fw:
                        fw.write(url + "[ZLSLHX]\n[ZLSLHX]" + title + "[ZLSLHX]\n[ZLSLHX]" + body_new)
                print(file_path + "\t翻译完成！")
                time.sleep(2)
            except:
                print("出现异常情况，跳过去……")
        else:
            print("文件已经翻译过了……")
