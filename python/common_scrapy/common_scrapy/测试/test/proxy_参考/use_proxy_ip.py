# -*- coding:utf-8 -*-
import re
import requests
from ScrapyUploadImage.tools.commons import baidu_user_agent
from bs4 import BeautifulSoup
import random
import urllib3
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from threading import Thread

class UseProxyIP():
    pass