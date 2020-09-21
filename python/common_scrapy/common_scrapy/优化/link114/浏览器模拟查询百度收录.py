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


# 参考地址
# https://blog.csdn.net/yunwubanjian/article/details/88354905
def chaxun_baidu_shoulu(urls):
    """
    :param text: 待翻译的文本
    :param sl: 当前语言
    :param tl: 目标语言
    :return:
    """
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(executable_path="D:/WorkSpace/web_driver/chromedriver.exe", options=options)
    browser.get("http://www.link114.cn/")
    # print(browser.page_source)
    time.sleep(10)
    browser.find_element_by_id("chk_baidu_kz").click()  # 选中 百度快照日期 复选框
    time.sleep(1)
    url_websites = browser.find_element_by_id('ip_websites')  # 选中 url 输入框
    url_websites.send_keys(urls)  # 输入 url 地址
    time.sleep(1)
    browser.find_element_by_id('tj').click()
    time.sleep(10)

    result_text_node = browser.find_element_by_class_name('c')
    re_text = result_text_node.text
    browser.close()
    print(re_text)


if __name__ == '__main__':
    # url_path = "./article-urls.txt"
    # gfr = generator_file_arr(url_path, 500)
    # for url_list in gfr:
    #     urlstr = "|".join(url_list).replace("https://",'')
    #     cha_shou_lu(urlstr)
    #     sleep(10)
    #     exit()

    urls = "www.gaoding.com/article/3423\nwww.gaoding.com/article/10275\nwww.gaoding.com/article/10273\nwww.gaoding.com/article/10271\nwww.gaoding.com/article/10269\nwww.gaoding.com/article/10267\nwww.gaoding.com/article/10266\nwww.gaoding.com/article/10264\nwww.gaoding.com/article/10262\nwww.gaoding.com/article/10260\nwww.gaoding.com/article/10232\nwww.gaoding.com/article/10230\nwww.gaoding.com/article/10228\nwww.gaoding.com/article/10055\nwww.gaoding.com/article/10053\nwww.gaoding.com/article/10087\nwww.gaoding.com/article/10084\nwww.gaoding.com/article/10082\nwww.gaoding.com/article/10080\nwww.gaoding.com/article/10079\nwww.gaoding.com/article/10048\nwww.gaoding.com/article/10216\nwww.gaoding.com/article/10213\nwww.gaoding.com/article/10212\nwww.gaoding.com/article/10215\nwww.gaoding.com/article/10169\nwww.gaoding.com/article/10211\nwww.gaoding.com/article/10171\nwww.gaoding.com/article/10170\nwww.gaoding.com/article/10255"
    chaxun_baidu_shoulu(urls)
