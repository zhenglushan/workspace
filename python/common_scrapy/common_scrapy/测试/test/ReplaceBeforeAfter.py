# -*- coding:utf-8 -*-
import re

test_str = '''
<div class="wen_article">
          <br />
<span style="font-size:14px;"><span style="font-family:微软雅黑;">&nbsp; &nbsp; &nbsp; &nbsp;</span></span><span style="font-size: 14px;"><span style="font-family: 微软雅黑;">=====推荐阅读=====</span></span>
<p><span style="font-size: 14px;"><span style="font-family: 微软雅黑;"><span style="color: rgb(255, 0, 0);">　　</span></span></span><span style="font-size:14px;"><span style="font-family:微软雅黑;"><a href="//www.zhicheng.com/n/20170215/123302.html" style="text-decoration: none; color: rgb(68, 68, 68); font-family: tahoma, arial, 宋体, sans-serif; line-height: 18px;" target="_blank"><span style="color:#ff0000;"><span style="background-color:#ffffff;">禽流感最新消息各地感染情况汇总 概念股一览</span></span></a></span></span></p>
<p><span style="font-size:14px;"><span style="font-family:微软雅黑;"><span style="color:#ff0000;"><span style="background-color:#ffffff;">　　</span></span><a href="http://news.zhicheng.com/n/20170216/123694.html" style="text-decoration: none; color: rgb(68, 68, 68); font-family: tahoma, arial, 宋体, sans-serif; line-height: 18px;" target="_blank"><span style="color:#ff0000;"><span style="background-color:#ffffff;">禽流感最新消息：2017年1月H7N9致79人死(预防知识)</span></span></a></span></span></p>
<p><span style="font-size:14px;"><span style="font-family:微软雅黑;"><span style="color:#ff0000;"><span style="background-color:#ffffff;">　　</span></span><a href="//www.zhicheng.com/n/20170217/123820.html" style="text-decoration: none; color: rgb(68, 68, 68); font-family: tahoma, arial, 宋体, sans-serif; line-height: 18px; background-color: rgb(251, 255, 228);" target="_blank"><span style="color:#ff0000;"><span class="hs0"><span style="background-color:#ffffff;">2017禽流感猛烈袭击！这些H7N9概念股又火了一把</span></span></span></a></span></span></p>
<p><span style="font-size: 14px;"><span style="font-family: 微软雅黑;">　　=====全文阅读=====</span></span></p>
<p><span style="font-size: 14px;"><span style="font-family: 微软雅黑;">　　<a href="http://www.zhicheng.com" target="_blank">至诚财经网</a>(<a href="http://www.zhicheng.com" target="_blank">www.zhicheng.com</a>)02月17日讯</span></span></p>
<p><span style="font-size:14px;"><span style="font-family:微软雅黑;">　　2月福建9例H7N9一人死亡 这些防范知识要记牢</span></span></p>
<center>
	<span style="font-size:14px;"><span style="font-family:微软雅黑;"><img alt="禽流感最新消息2017" border="1" height="258" src="//www.zhicheng.com/uploadfile/2017/0217/20170217021639962.png" width="500" /></span></span></center>
<p><span style="font-size:14px;"><span style="font-family:微软雅黑;">　　昨日中午，福建省卫计委通过官方网站公布：当前我省仍然处于人感染H7N9流感疫情的高发季节，进入2月以来，我省报告人感染H7N9流感病例9例，其中死亡病例1例。</span></span></p>
<p><span style="font-size:14px;"><span style="font-family:微软雅黑;">　　记者从昨日召开的福建省卫生计生会议上获悉，我省目前疫情平稳。目前，我省正采取落实源头管控、强化病例救治、加强监测预警等措施防控H7N9流感。</span></span></p>
<p><span style="font-size:14px;"><span style="font-family:微软雅黑;">　　群众预防人感染H7N9流感应尽量避免接触活禽，更不要接触病、死禽，远离活禽交易场所，注意个人卫生。</span></span></p>
<p><br />
          <div class="sf_1"><span id="10" class="tyTestPos"></span></div>
          <div class="page"><a class="a1" href="//news.zhicheng.com/n/20170217/123875.html">上一页</a> <span>1</span> <a href="//news.zhicheng.com/n/20170217/123875_2.html">2</a> <a href="//news.zhicheng.com/n/20170217/123875_3.html">3</a> <a href="//news.zhicheng.com/n/20170217/123875_4.html">4</a> <a href="//news.zhicheng.com/n/20170217/123875_5.html">5</a> <a href="//news.zhicheng.com/n/20170217/123875_6.html">6</a> <a href="//news.zhicheng.com/n/20170217/123875_7.html">7</a> <a class="a1" href="//news.zhicheng.com/n/20170217/123875_2.html">下一页</a></div>        </div>
              </div>
'''

re_sub = ".*日讯</span></span>"
test_str = re.sub(re_sub, "", test_str, flags=re.I | re.S)
re_sub = '<div class="sf_1">.*'
test_str = re.sub(re_sub, "", test_str, flags=re.I | re.S)

print(test_str)
