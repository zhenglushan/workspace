# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 抓取网易音乐评论.py
# @DATETime   : 2020/5/19 10:50
# @Author     : 笑看风云


import requests, os
from pyquery import PyQuery as pq
import html

baseurl = 'https://music.163.com/discover/playlist'
headers_play = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'music.163.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


def get_all_comments(song_id):
    # 评论和赞的数量
    comments_likedCounts = {}
    limit = 30
    offset = 0
    url = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + str(song_id) + "?offset={0}&limit={1}"
    index = 0
    while True:
        url_req = url.format(offset, limit)
        response = requests.get(url_req, headers=headers_play)
        json_text = response.json()
        is_more = json_text['more']
        com_total = json_text['total']
        if is_more and (com_total > offset):
            print("当前采集的页面地址为：" + url_req)
            comments_list = json_text['comments']
            for comment in comments_list:
                content = comment['content']  # 评论内容
                time = comment['time']  # 评论时间
                likedCount = comment['likedCount']  # 评论点赞数量
                new_comment = {
                    "content": html.escape(content),
                    "time": time,
                    "likedCount": likedCount
                }
                comments_likedCounts[str(index)] = new_comment
                index = index + 1
            offset = offset + limit
        else:
            # print("没有更多内容采集了！")
            break
    # print("打印所有评论")
    # for key, value in comments_likedCounts.items():
    #     print(key, ' ： ', value)
    return comments_likedCounts


if __name__ == "__main__":
    response = requests.get(baseurl, headers=headers_play)

    if response.status_code == 200:
        # 定义保存所有歌单 ID 的列表
        playlist_ids = []
        content = response.content.decode()
        # print(content)
        doc = pq(content)
        page_area = doc('a.zpgi')
        total_page_num = int(page_area.eq(-1).text())
        # 获取歌单列表的总页码
        print('歌单分页的总页码为：', total_page_num)
        # 歌单的分页链接格式
        page_link_format = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={0}"
        for i in range(total_page_num):
            offset = 35 * i
            # 歌单分页链接地址
            page_link = page_link_format.format(offset)
            print('歌单分页的当前分页地址为：' + page_link)
            play_list_page_resp = requests.get(page_link, headers=headers_play)
            play_list_doc = pq(play_list_page_resp.content.decode())
            # 解析分页中的歌单 ID 值
            playlist_area = play_list_doc('a.tit.f-thide.s-fc0')
            # print(len(playlist_area))
            playlist_ids_temp = [x.attr('href').split('?id=')[-1] for x in playlist_area.items()]
            print("歌单分页的当前分页中的歌单 ID 列表为：")
            print(playlist_ids_temp)
            # 把歌单 ID 保存到 歌单 ID 列表变量
            playlist_ids = playlist_ids + playlist_ids_temp

        if playlist_ids:
            # 循环解析歌单页面
            for playlist_id in playlist_ids:
                one_playlist_url = 'https://music.163.com/playlist?id=' + str(playlist_id)
                print("当前正在解析的歌单详情页面为：" + one_playlist_url)
                one_playlist_resp = requests.get(one_playlist_url, headers=headers_play)
                one_playlist_doc = pq(one_playlist_resp.content.decode())
                songid_area = one_playlist_doc('div#song-list-pre-cache ul.f-hide a')
                all_song_ids = [x.attr('href').split('?id=')[-1] for x in songid_area.items()]
                if all_song_ids:
                    # 循环解析歌曲详细页面
                    for song_id in all_song_ids:
                        song_url_format = "https://music.163.com/song?id={0}"
                        song_url = song_url_format.format(song_id)
                        print("当前正在解析的歌曲详情页地址为：" + song_url)
                        song_resp = requests.get(song_url, headers=headers_play)
                        song_resp_doc = pq(song_resp.content.decode())
                        song_info = {}
                        desc_meta = song_resp_doc('meta[property="og:description"]').attr.content
                        song_info["description"] = html.escape(html.unescape(desc_meta) + '。')
                        # print(meta)
                        # exit()
                        # for x in meta.items():
                        #     if x.attr.name == '':
                        #         description = x.attr.content
                        #         # print(description)
                        #         song_info['description'] = description.split('所属专辑：')[-1] if '所属专辑：' in description else description
                        name, singer, *_ = song_resp_doc('title').text().split(' - ')
                        song_info["singer"] = html.escape(singer)
                        song_info["song_name"] = html.escape(name)
                        song_info["comments_likedCounts"] = [get_all_comments(song_id)]
                        song_file_path = 'D:/WorkSpace/采集数据/music_163_com_comments/' + str(song_id) + '.json'
                        with open(song_file_path, 'w+', encoding='utf-8') as songf:
                            song_info = str(song_info)
                            song_info = song_info.replace("'", '"')
                            songf.write(song_info)
