# -*- coding:utf-8 -*-
# @ProjectName: flutter_lesson
# @Email	  : 276517382@qq.com
# @FileName   : 使用浏览器模拟来翻译.py
# @DATETime   : 2020/4/22 15:24
# @Author     : 笑看风云
"""
常备特殊的不可见字符
♂ ♀ ¶ ♈ ♉ ♊ ♋ ♌ ♎ ♏ ♐ ♑ ♓ ♒ ♍
"""

from selenium import webdriver
import html
import time

text_arr = []
with open("./1.txt", mode='r', encoding='utf8') as rf:
    for line in rf:
        line = line.strip()
        line = line.replace('<p>', '[ZLS]').replace('<P>', '[ZLS]').replace('</p>', '[LHX]').replace('</P>', '[LHX]')
        text_arr.append(line)


# 参考地址
# https://blog.csdn.net/yunwubanjian/article/details/88354905
def google_translate(text, sl, tl):
    """
    :param text: 待翻译的文本
    :param sl: 当前语言
    :param tl: 目标语言
    :return:
    """
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(executable_path="D:/WorkSpace/web_driver/chromedriver.exe", options=options)
    browser.get("https://translate.google.com/#view=home&op=translate&sl=" + sl + "&tl=" + tl)
    text_dummy = browser.find_element_by_class_name('tlid-source-text-input')
    text_dummy.clear()
    text = html.unescape(text)  # 把 &;实体 转换成字符
    text_dummy.send_keys(text)
    time.sleep(3)
    # text_translation = browser.find_elements_by_xpath('//span[@class="tlid-translation translation"]/span')
    # for text_elem in text_translation:
    #     new_text = new_text + text_elem.text
    # browser.close()
    # return new_text
    text_translation = browser.find_element_by_xpath('//span[@class="tlid-translation translation"]')
    re_text = text_translation.text
    browser.close()
    return re_text


# 对字符串数组进行重新拼接
def split_text(text_arr, xianchang=4500):
    """
    :param text_arr: 文本数组
    :param xianchang: 限长
    :return:
    """
    wenben_len = len("".join(text_arr))
    new_text_arr = []
    # print(wenben_len)
    if wenben_len > xianchang:
        # print("需要分割数组")
        text_temp = ""
        for i, tex in enumerate(text_arr):
            if len(text_temp + tex) < xianchang:
                text_temp = text_temp + tex
                if i == len(text_arr) - 1:
                    new_text_arr.append(text_temp)
            else:
                new_text_arr.append(text_temp)
                text_temp = tex

        # len_arr = [len(te) for te in new_text_arr]
        # print(len_arr)
        # for ti in new_text_arr:
        #     print(ti)
    else:
        print("直接调用翻译")
        new_text_arr.append("".join(text_arr))
    return new_text_arr


new_text_arr = split_text(text_arr, 4000)
new_text = ""
len_arr = [len(te) for te in new_text_arr]
print(len_arr)
for i, ti in enumerate(new_text_arr):
    google_translate_result = google_translate(ti, "zh-CN", "en")
    print("第 " + str(i + 1) + " 次翻译……")
    # print(google_translate_result + "\n\n")
    new_text = new_text + google_translate_result
    time.sleep(1)
print(new_text)

new_text = new_text.replace('[LHX]', '[LHX]\n')
new_text_arr = new_text.split("\n")
new_text_arr = new_text_arr[0:-1]
new_text_arr = split_text(new_text_arr, 4000)
new_text = ""
len_arr = [len(te) for te in new_text_arr]
print(len_arr)
for i, ti in enumerate(new_text_arr):
    google_translate_result = google_translate(ti, "en", "zh-CN")
    print("第 " + str(i + 1) + " 次翻译……")
    # print(google_translate_result + "\n\n")
    new_text = new_text + google_translate_result
    time.sleep(1)
new_text = new_text.replace('[ZLS]', '<p>').replace('[LHX]', '</p>')
print(new_text)
