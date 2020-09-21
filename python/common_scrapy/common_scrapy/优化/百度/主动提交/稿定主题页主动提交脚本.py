# -*- coding:utf-8 -*-
# @ProjectName: scrapy_mongodb_for_search
# @Email	  : 276517382@qq.com
# @FileName   : 稿定搜索关键词.py
# @DATETime   : 2020/4/15 16:40
# @Author     : 笑看风云


import re, requests, json, time, os
from ScrapyMongoDBForSearch.工具.通用工具 import arr_size

save_file_path = "./static.txt"


def crawl_urls():
    result_urls = []
    webpage_for = 'https://www.gaoding.com/static/templates/quanbu-{}.html'
    for i in range(1, 173):
        webpage = webpage_for.format(i)
        print(webpage + "\t正在抓取……")
        content_first = requests.get(webpage).text
        pattern = '(/statics/\d+.html)'  # 匹配的正则表达式
        sm_index_file_arr = re.findall(pattern, content_first, flags=re.I | re.S)
        if sm_index_file_arr:
            for static_url in sm_index_file_arr:
                static_url = "https://www.gaoding.com" + static_url
                result_urls.append(static_url)
        time.sleep(3)
    with open(save_file_path, mode="a+", encoding="utf8") as sf:
        sf.write("\n".join(result_urls))


def post_urls():
    result_urls = []
    with open(save_file_path, mode="r", encoding="utf8") as sf:
        for line in sf:
            result_urls.append(line.strip())
    avg_num = 1500
    urls_res_arr = arr_size(result_urls, avg_num)
    week_conf = {
        'site': 'www.gaoding.com',
        'token': 'ZTrx6cSp619A0SYM'
    }
    postUrl = 'http://data.zz.baidu.com/urls?site={}&token={}'

    headers = {'Content-Type': 'text/plain'}
    postUrl = postUrl.format(week_conf['site'], week_conf['token'])
    if urls_res_arr:
        for urls in urls_res_arr:
            print(urls)
            result = requests.post(postUrl, data="\n".join(urls), headers=headers)
            reText = result.text
            if 'error' in reText:
                if 'site error' in reText:
                    print("站点未在站长平台验证")
                elif 'empty content' in reText:
                    print("post内容为空")
                elif 'only 2000 urls are allowed once' in reText:
                    print("每次最多只能提交2000条链接")
                elif 'over quota' in reText:
                    print("超过每日配额了，超配额后再提交都是无效的")
                elif 'token is not valid' in reText:
                    print("token错误")
                elif 'not found' in reText:
                    print("接口地址填写错误")
                elif 'internal error, please try later' in reText:
                    print("服务器偶然异常，通常重试就会成功")
                break
            else:
                print(reText)
                jsonStr = json.loads(reText)
                remain = jsonStr['remain']
                success = jsonStr['success']
                if remain < avg_num:
                    break
            print('---------------------------------------------------------')
            time.sleep(3)


if __name__ == "__main__":
    if not os.path.exists(save_file_path):
        crawl_urls()
    post_urls()
