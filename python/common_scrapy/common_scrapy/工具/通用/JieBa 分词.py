# -*- coding:utf-8 -*-
# @ProjectName: ScrapyMongoDBForSearch
# @Email	  : 276517382@qq.com
# @FileName   : 分词工具.py
# @DATETime   : 2020/5/18 15:16
# @Author     : 笑看风云

'''
JieBa 分词操作

千万级内链系统架构上
http://www.netconcepts.cn/detail-40408.html
千万级内链系统架构中
http://www.netconcepts.cn/detail-40536.html
千万级内链系统架构下
http://www.netconcepts.cn/detail-40655.html

a、 将需要内链的关键词，添加到词典内。添加到什么地方的词典？当然是添加到分词词典。目前的分词技术，主要还是基于词典的分词。我们把默认的词典保留最小化版本。再把我们的内链词，添加到自定义词典内。标记为一个特殊的词性。下面会有代码演示。
b、 使用分词技术对一篇文章进行分词切词处理。
c、 输出带指定词性（即我们添加的关键词词典）的关键词。即可得到本文的所有包含关键词信息。
d、 查询关键词的链接，添加替换文章内容即可。

中文分词的工具非常多。比如：结巴分词、IK分词、MMSeg、盘古分词等等
'''
import os
import random
import re

import jieba
import jieba.analyse
import jieba.posseg as pseg
from common_scrapy.工具.通用.方法库 import is_number, returnDictPath, filter_all_html


class FenCi():
    '''
    使用 JieBa 分词库来进行分词
    '''

    def __init__(self, content, dict_name=""):
        self.content = content
        if dict_name:
            self.dict_path = returnDictPath(dict_name)  # 指定关键词的网站的字典不为空
        else:
            self.dict_path = ""  # 普通的网站的字典为空

    def returnValues(self):
        '''
        返回值为 当前文档的 关键词、tags标签、以及做了内链标记的内容正文
        :param content: 要进行分词的内容
        :param dict_name: 默认为空，说明是普通新闻站，如果不为空，则是关键词站点
        :return:
        '''
        # 1、图片过滤操作
        self.replaceImg()

        # 2、提取关键词集合
        result = set()
        kw_list = []  # 保存 result 过滤后的关键词
        if self.dict_path:
            dict_path_arr = self.getDictPathArr()
            for dict_file_path in dict_path_arr:
                jieba.load_userdict(dict_file_path)
                result = self.parseContent(result)
                kw_list = list(result)
        else:
            allow_POS = ''
            if len(self.dict_path) > 0:
                allow_POS = "('n', 'nr', 'ns', 'v', 'a')"
            else:
                allow_POS = "('n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng')"
            result = jieba.analyse.extract_tags(self.temp_content, topK=10, withWeight=True,
                                                allowPOS=allow_POS)
            for item in result:
                if not is_number(item[0]):
                    kw_list.append(item[0])
        # print(kw_list)
        # 3、内链标志
        self.innerLinkMark(kw_list)
        # 4、以后可能考虑加上同义词替换
        # 5、图片还原操作
        self.recoveryImg()
        # print(self.content)
        # 6、准备要返回的值
        kw_list_temp = kw_list.copy()
        random.shuffle(kw_list_temp)
        kw_list_len = len(kw_list_temp) // 3  # 整除
        tags = ",".join(kw_list_temp[:kw_list_len])
        return tags, kw_list, self.content

    # 替换内链关键词标志
    # 关键词内容按照长度排序, 较短的词先替换, 因为字符串之间可能有互相包含的情况
    # 普通网站则按照权重高低进行替换
    def innerLinkMark(self, keywords):

        if self.dict_path:
            # 按照长度排序,由短到长
            keywords.sort(key=lambda i: len(i), reverse=False)

        for keyword in keywords:
            # 从左往右替换
            self.content = self.content.replace(keyword, "<span data-mark=\"zlsInternalLink\">" + keyword + "</span>",
                                                1)
            # 从右往左替换
            # self.content = self.r_replace(self.content, keyword, "<font color='red'>" + keyword + "</font>", 1)

    def r_replace(self, sourtr, oldstr, newstr, *max):
        """
        自定义一个右往左替换的函数
        :param sourtr: 源字符串
        :param old: 将被替换的子字符串
        :param new: 新字符串，用于替换 old 子字符串
        :param max: 可选字符串, 替换不超过 max 次
        :return:
        """
        count = len(sourtr)
        if max and str(max[0]).isdigit():
            count = max[0]
        return newstr.join(content.rsplit(oldstr, count))

    # 把 img 标签替换成临时占位符标签 ん
    # 并过滤所有的 html 标签
    def replaceImg(self):
        self.img_list = re.findall(r'(</?img[^>]*>)', self.content)
        if len(self.img_list) > 0:
            self.content = re.sub(pattern=r'(</?img[^>]*>)', repl=r'ん', string=self.content, flags=re.I | re.S)
        self.temp_content = filter_all_html(self.content)  # 过滤所有 html 标签

    # 还原 img 标签
    def recoveryImg(self):
        if len(self.img_list) > 0:
            for img in self.img_list:
                self.content = self.content.replace("ん", img, 1)

    def parseContent(self, result):
        '''
        分词并过滤出我们需要的关键词
        :param result:
        :return:
        '''
        words = pseg.cut(self.temp_content)
        for word, flag in words:
            if flag == "zlslhx":
                if not is_number(word):  # 判断字符串是否由数字组成
                    result.add(word)
        return result

    def getDictPathArr(self):
        '''
        获取字典目录下的所有字典文件的具体路径数组
        :return:
        '''
        dict_file_arr = os.listdir(self.dict_path)
        dict_file_arr.sort()
        dict_path_arr = []
        for df in dict_file_arr:
            dict_path = self.dict_path + df
            dict_path_arr.append(dict_path)
        return dict_path_arr


if __name__ == "__main__":
    content = '体重秤上的数字是很多MM都在意的问题，总是为体重增加而烦恼？其实不能瘦身可能与平日没有在意的行为有关，想成功减肥的人注意不要再犯以下这15种坏习惯哦！<br/><span class ="yrkj" style="display:block;text-align:center;"><img src="/uploads/allimg/2019/3/27/26804976a038d9db7ce8ad60a90c8cc2.png"/></span><strong>1. 不咀嚼进食</strong><br/>部分人可能不怎么咀嚼地快速进食，可是咀嚼次数减少会减低饱肚感，一不留神便会吸收过多卡路里！咀嚼能刺激饱肚感，也能使肠胃消化更顺畅。<br/><strong>2. 一边做其他事情一边进食</strong><br/>不管电视、手机或电脑，边看其他东西边进食会影响身体向大脑传递「进食」的讯息，散漫地进食也是导致肥胖的原因！<br/><strong>3. 肚子不饿仍然吃东西</strong><br/>新陈代谢会随年龄减慢，食量也会随年龄减少，因此1日3餐外给予肠胃休息时间是非常重要。即使要在空闲时间进食，也应该选择粥、冰沙、汤等有利消化的食物。<br/><strong>4. 偶尔极端节食</strong><br/>网上流传不同的节食方法，例如1日只吃某食物、3日不进食等，可是这些营养价值偏低的方法会破坏身体调节，如蛋白质不足难以形成肌肉，使身体容易肥胖，另外极端节食容易在日后引起反效果，因此最好不要尝试。<br/><strong>5. 经常吃外卖</strong><br/>煮食次数少，经常吃外卖的人容易因营养不均衡而造成肥胖。即使平日难以避免要在外面吃，假日时也尝试亲自煮蔬菜吃吧！<br/><strong>6. 没有全身镜</strong><br/>只看上半身会难以全面「检查」全身的肥胖状况，想维持身形全身镜绝对有帮助。<br/><strong>7. 只穿宽松的衣服</strong><br/>宽松的衣服会隐藏真实的身材，除了减低减肥的动力，即使肥胖了也难以发现。偶尔可以尝试穿紧身的衣服，维持正确的走路姿势，让肚子保持最佳状态对瘦身起正面作用。<br/><strong>8. 超级喜欢啤酒</strong><br/>1杯中型大小的啤酒已经等于1碗饭的卡路里，因此喜欢啤酒而每晚都喝的话，很容易吸收过多卡路里。建议可以喝1杯啤酒后再喝卡路里及糖分较低的酒类如威士忌。<br/><strong>9. 经常与同样的人在一起</strong><br/>经常与同一群朋友见面，即使身形有变化也难以察觉，偶尔也与其他人会面吧！<br/><strong>10. 当作奖励的甜品</strong><br/>工作后经常以甜品作奖励，瘦身便会变得遥遥无期。<br/><strong>11. 不理会便秘</strong><br/>持续便秘会使新陈代谢恶化，变成难以瘦下来的体质。便秘是蔬菜、水份、运动不足的警示！不理会的话肥胖便会一直维持。<br/><strong>12. 早上赶时间出门</strong><br/>为了可以睡更长时间，不少人会把起床时间调较至接近出门的时间，可是长期赶时间出门会使身体没有伸展、深呼吸的时间，甚至失去排泄的习惯。其实只要早一点起床，身体便会有整理的时间，更有利身体健康。<br/><strong>13. 驼背</strong><br/>这是容易肥胖的人经常出现的坏习惯！驼背会使脂肪容易在肚子积聚，而且骨盆歪斜容易引致下半身肥胖及新陈代谢下降。平日经常注意走路姿势，整个人的姿态看起来也会更美观。<br/><strong>14. 超级喜欢调味料</strong><br/>即使是素食，喜欢加调味料的人很容易因为调味料含有的高卡路里引致肥胖。不论什么食物也加调味料的人趁机戒掉这坏习惯吧！<br/><strong>15. 空闲时间过多</strong><br/>空闲时人很容易坐着又不断吃东西引致肥胖。空闲时不防投入兴趣或与朋友外出吧！出去走走更可以顺便消耗卡路里，有利瘦身！<br/><p>'
    fenci = FenCi(content, "")
    result = fenci.returnValues()
    print(result)
