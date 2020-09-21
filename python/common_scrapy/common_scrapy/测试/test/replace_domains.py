# -*- coding:utf-8 -*-
import re


def raplace_domains(content):
    '''
    把正文中包含的网址都替换为空
    :return:
    '''

    content = "5月16日，针对《交通http://www.hello.com.org.net/运输】http://www.CXDFFhwqdc.com进行了新业态s23d456h7893d4f56h7j89.jpg用户资d456b7.jpeg金管理办法(试行)》中有关“互联网租赁自行车押金最长退款周期不超过 2个工作日”的规定，ofo小黄车方面表示，ofo小黄车作为交通运输新业态的一份子，深知行业规范化道阻且长https://www.xxpp.com/。今日国家六部委联合发布的管理办法34cvb6n78m93c4v5b67n8.gif是维持共享单车行业稳定发展的关键举措，也是推动http://tyuio/yuiop/tyuiop.png行业继续向前的重要一步，“我们将尽最大努力，积https://www.ooxx.com极配合落实最新政策，为用户负责、为社会创造更大价值。”5月16日，交通运输部、人民银行、国家发展改革委、公安部、市场监管总局、银保监会6部门联合印发了《34g6h7j8k9l0.png交通运输新业态用户资金管理办法(试行)》(交运规〔2019〕5号，以下简称《管理办法》)。交通运输部表示，《http://keke.com管理办法》的出台，对从源头防范用www.91hkbb.com户资金风险、加强https://baidu.com用户权益保障、促进交通运输新业态健23456b7n8mmnbvc43c4v5b67n8.bmp康稳定发展http://www.xuexi.com具有积极意义。《管理办法》共5章27条，对用户资金收取、开立专www.lahoug.com用存款账户存管，以及建立联合工作机制强化监管等方面做出了具体规定。"

    re_sub = "(http:\/\/|https:\/\/){0,1}(www.){0,1}[0-9a-zA-Z\-]+\.((?!jpg|jpeg|png|gif|bmp|psd|tiff|tga|eps)[a-zA-Z\.])+[\/]{0,1}"

    content = re.sub(re_sub, "", content, flags=re.I | re.S)
    print("content : " + content)


if __name__ == "__main__":
    raplace_domains("")
