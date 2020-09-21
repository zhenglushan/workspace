# -*- coding:utf-8 -*-


keyword_list = [
    "私家侦探", "代孕", "代运营", "办户口", "半永久", "伴游", "试管婴儿", "婚姻调查", "比特币", "婴儿车", "月子中心", "丰胸",
    "婚纱摄影", "精油", "空调维修", "配资", "祛斑", "祛痘", "祛眼袋", "祛皱纹", "私服", "网赚", "整形", "种植牙", "注册公司", "壮阳",
]

# 被拦截的关键词: 刻章
# 没查询的关键词: 番号

BAIDU_SEARCH_KEYWORD = "D:/WorkSpace/数据采集/百度搜索结果/关键词/"

BAIDU_SEARCH_IMAGE_STORE = "D:/WorkSpace/数据采集/百度搜索结果/图片/"

web_sites = {
    '代运营': [
        'www.gencong.net',
    ],

    '半永久': [
        'www.jgzlzx.com',
    ],

    '私家侦探': [
        'www.syhrzc.com',
    ],

    '代孕': [
        'www.tztnet.com',
    ],

    '壮阳': [
        'www.sylfx.com',
    ],
    '伴游': [
        'www.xfwdg.com',
    ],
    '试管婴儿': [
        'www.hczgc.com',
    ],
    '月子中心': [
        'www.bfhsf.com',
    ],
    '婚纱摄影': [
        'www.ahfxo.com',
    ],
    '网赚': [
        'www.jjboai.com',
    ],
}

web_sites_mongdb = {
    '词根一': ['集合一', 'www.baidu.com', 'www.google.com', '集合二', 'www.sina.com.cn', '集合三', 'www.163.com', '关键词四'],
    '词根二': ['集合五', 'www.baidu22.com', 'www.google22.com', '集合二', 'www.sina22.com.cn', '集合三', 'www.16322.com', '关键词四'],
    '词根三': ['集合六', 'www.baiducn.com', 'www.googleheng.com', '集合二', 'www.sina99.com.cn', '集合三', 'www.16344.com', '关键词四'],
}
