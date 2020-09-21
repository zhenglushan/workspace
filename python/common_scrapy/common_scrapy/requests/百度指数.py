# -*- coding:utf-8 -*-
'''
http://index.baidu.com/v2/index.html#/
13459282910
a5s7sh4u
'''

import requests
import random
import math


def get_idx(i):
    if i != 'x' and i != 'y':
        return i
    t = random.randint(0, 16)
    if 'x' == i:
        n = t
    else:
        n = (3 & t) if 3 & t else 8
    return hex(n).replace('0x', '')


def guideRandom():
    guide = [get_idx(i) for i in "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"]
    return "".join(guide).upper()


def baseN(num, b):
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def get_callback(prefix):
    ran_num = math.floor(2147483648 * random.random())
    print(prefix + baseN(ran_num, 36))
    return prefix + baseN(ran_num, 36)


url = "https://passport.baidu.com/v2/api/?login"
method = "post"
host = "passport.baidu.com"
origin = "http://index.baidu.com"
referer = "http://index.baidu.com/v2/index.html"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"

headers = {
    'User-Agent': user_agent,
    'Host': host,
    'Referer': referer,
}

form_data = {
    'staticpage': 'http://index.baidu.com/v2/static/passport/v3Jump.html',
    'charset': 'utf-8',
    'token': '27de0c7cdd3e3fa18eb5994dbe928528',
    'tpl': 'nx',
    'subpro': '',
    'apiver': 'v3',
    'tt': '1567154340421',
    'codestring': '',
    'safeflg': '0',
    'u': 'http://index.baidu.com/?tpl=login&redirect=http%3A%2F%2Findex.baidu.com%2Fv2%2Findex.html%23%2F',
    'isPhone': 'false',
    'detect': '1',
    'gid': guideRandom(),
    'quick_user': '0',
    'logintype': 'basicLogin',
    'logLoginType': 'pc_loginBasic',
    'idc': '',
    'mkey': '',
    'loginmerge': 'true',
    'username': '13459282910',
    'password': 'vDruE+78Q8bLQQ03Mx6TlGzXxFvV4SccxFBwcMyu79y8gFQLigcvzlVFwtLvTaA1k1KwJy9qxW0f4yjXXjFeAd/zQUBl8Gy/TgxVH6unWZM3sY3nYsvQDLnLVhJjBPEw6MNBynxIbX3I1jKa2ja7kp+xTJnC5FsVV/i8/KOBxDw=',
    'mem_pass': 'on',
    'rsakey': '2IFGf76WQMJ0DMPw7QhS0D2JflpmUGfk',
    'crypttype': '12',
    'ppui_logintime': '4430',
    'countrycode': '',
    'fp_uid': '',
    'fp_info': '',
    'ds': 'dAGvU5mvTDBRyUsaUtyT5Tt33EVmzS8hc7JwL2O8OC9P3uwsT/anpqEH4or/jsOeQNsTWXx4jZcL8+twAKbjU0lyJ2lgd+O/HdBcrUr2tRXPvQSX7eHvWliP85ESjyes/pMbmJVokKwiGXQlcAwHGBXWwxVTcap1m5z5vG9V+U3vvAJxnw2pOnPUCv2TyRFtnd2Ff6gWLG12IoYFzzHIwtOCdzBAftKvg3gAnpbiztpXCEmXd2A5KU2GTnTPYlMszHsjMh0oPt/3eODI45lRZDSBqfZgh1Fw1Lrqy61gkMdsJa8RQdtq4+82sNddiyJaavZwgwP5d4F5+vp3zV6grpa2Xc8EdBKlTv7X1O1sP72w1e5HTBNWdSZHaubvJS2EtxHfoX4nA5rze6NdrW3OtrBiWTxuaNe8Z0/3FUrTyQet+jhn7QEwvCIoR8oxlEH/oHlbklKhrwOJVy53H2O/LbaveGfYFljuUFmhsptXirE1k7sSpQXibmmaQ2R1y+LlhWKJjCnJkQdJ7JmMCQ2q3dTUWY7kpy6b1lS+ldOio/55pWRICpgullz0d6DLdTypo+wdyw5dWOpp9pALJseS3jaADCVoC1cvIxH44x6BZ5zVuXpdMHWqldAVtJ3iV0GpTzRdwo9AsoQ9Uc1vTe8gqmBk674CFVkUKt3WpD15hEd15GH8phJMs48fcrBx0LS5PamyVGqoaqzURaMx+VNIBSO1yuKyZW6q98uFVOI6tsMX4DDhtFJCuA/ztjOUhc81u8qcbzM/FGR4p3CdCBoJGONLXpAzt6hdzwJfMRWcG4oCXxJ68BMH+xfHWiSk05wxpQGagHEU3BqoCdN/a2QWX58WbNYQ5Nnt02z6w/6GcJbDKC7tkbWkWK6Dgn7nZ9zZABJdcBxdhDuzP08M8vi+PyxSLJ0AQyslvIRiN+6jK/LKnak6uAuuCkAPrXacjjknTfXDyFJl7v8bVBzclp+OCyXJTJboVa/yroKvDOu8Epi8sPARwZ9fP15CI3kYlIStnnYoSOoOjLbdMqztJKioaWMxIVUc/mIC6irDKATtZYa1scgMw2XeafE1vHIQQ4EPeyzJdGZXaf9TmanwI+TJebqDZl9kAGVr7SDe9zDUoxowk8leKYqKD5RbdHG+krcEapY05+0Qw3zDOa8kQmMSAU6MOfEtltUFS7/g7gqX1duol9LZvkqxDGgfsS28OGs4QO2doZ37/8rboWJHufRKoju4EBC58sjoF9fe1s7nFj5TzVE6vfQNiH6r69nBxr/StZRgb7vHUGS0Qe3x4DgKcw==',
    'tk': '55111+2MxAQZiFuvi2v5VR6eK+BmfLP2Mwb9e6k/7hJ0ZL5gFpjCyEdyi1ruE4mmzcutIV2Q98oJivIJDp6KmFDJ1A==',
    'dv': 'tk0.67819786569773971567154336263@rrk0Ir4kqbCst8pw5hGCyT7tBFJzpTJYhQRYBYHY534kFxBngbrmUwK~w2H-wPH-ZPKDB2HYCiMmgxBkMl4kqbMDBzHmwgKJBzM-y~LmwVLuVx4kFxBYg_ek0hIBzv-4kvYrmgxB2sbCst8pw5hGCyT7tBFJzpTJYCzLJ58KDwVTkKw8mgzr2rbrGqg8EU7F7jn73tBJwyF7whTBtyTRutzRYMfRNpl8G7U4kr-r1gUBkqj4uViLuCZ4DUfL-Vi4D5bH-Bd4D5ATkSgrmgwBGSbrzqjB1UlBzs~4kFzrmgzBGSZ4tphG3MEF7wTJwhG7tlxJwyzMD5P0JpJRNtgRuC~Tq__Iaa0~awSm80MhwkhrEg~4kRwxklMubg42KY8ksjBzS-BGKjBzRz8GRUBGKYrG7xrzr-r2Kzhk0Ga0npxRkOf4-ViLuCZ4N5Q0Dpw4NBfHEy-r1yIHNpVomjOMuwbv~lbMDj3LDLIHNC3Fkqrmgg4kKj8mgYrk7brG7zB1gZB2FbrG7zB1gUBGr-4kS~Bq__',
    'extrajson': '',
    'fuid': 'FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGnZAhwisb/DW3Ufqwui3XLg2CamKHdEkDjYNDrb+XjhVXefldEnw4+7qfVzNX7X7ZsZJZzighlRXCrosRimj6n4e15QciDfeM6IdZCd4dWIn8p25O4QwV1is+aaimMSBP0xg3XduDu1LQGcI8Qah4c9Ks5+Bm57DHOG4XwLtn1ztTGqoX0xdvnMY1yFYpkLxX0ZaGhxes+nljx68Dx7ernR3BLhoNACSIWjkgKwIzw9ZVt7XCZp60hW5gi37o9+NH72j6dwZ3uap/GZsMywRhybd5M2RtLZ6XQnb6lvKhclvZGL6O+yR7LfUChkqfvQtd6p+HBavJhpxl858h16cMtKQmxzisHOxsE/KMoDNYYE7t1dbxUobcSUILU9d9FlnvJAJLcm4YSsYUXkaPI2Tl66J246cmjWQDTahAOINR5rXR5r/7VVI1RMZ8gb40q7az7vCK56XLooKT5a+rsFrf5Zu0yyCiiagElhrTEOtNdBJJq8eHwEHuFBni9ahSwpC7n3B66nwmuQ05Ex8xMb1rcWdkL8k48VzHCbwwxHtzHCMnBxW2ZmxGPS090blrEo4o+RyHigMXgiUcykJoia7djX5roz5kr8MHLIy/exrPPaUWBNU0dy3SzL7bpW1hARWZingXDSzOSO2CUOV8/cBkrYf6tbkJ/VbAYwZizULGJ8Il9Yt/c0BNfUxsm686qzNaSUlvZRW39n3pF7k2addR8m2mbGLlCIQned0uMuLwwx/c7K43D8j65vNkorob4eoOocdLaJXUNu3pqVmRtfPj+wRHelTudApmj/iQ/1fJwiv8NU9AmVqiBt+iHOuihygJ7MtWDWXUQSgqR6q9uoj/KJuzH8X+tb0PV+Xnu3NL1fmqLIh+XcF6fnyPFPUxteQtbtLyi+gq5zowg1oFj8O/L9oVsoK22a9qUmM/HrJMRsLi1+J9aSd42+X78fDIZgkPh3epzLLvwRmnAbs5z/V+jl3P3gVnlwm9bfwhaFtnhFN2dHYAw7i4QhrXdzc77isXj52D/0YTMZ89WPyrtxig2OkIl81Iase/C16XVPKOj9XA==',
    'traceid': 'C6E2C501',
    'callback': 'parent.bd__pcbs__ya1e5m',
}

resp = requests.post(url, headers=headers, data=form_data)
print(resp.text)
