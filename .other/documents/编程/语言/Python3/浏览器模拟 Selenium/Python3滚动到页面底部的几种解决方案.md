# Python3 滚动到页面底部的几种解决方案

参考地址：
https://www.cnblogs.com/rumenz/p/11719630.html

在用selenium获取页面时,很多时候需要将滚动条拖到页面底部,下面总结了几种方法。

## location_once_scrolled_into_view

```python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


browser=webdriver.Chrome("G:/dj/chromedriver.exe")
wait=WebDriverWait(browser,10)
browser.set_window_size(1400,900)
import time

def search():
    try:
        browser.get("https://www.taobao.com") target=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(29)")))
        target.location_once_scrolled_into_view
    except TimeoutException:
        search()
search()
```

如果页面是ajax动态渲染的,页面的高度随时变化的,所以这个方法很有可能跳不到页面底部。

## ActionChains

```python
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

browser=webdriver.Chrome("G:/dj/chromedriver.exe")
wait=WebDriverWait(browser,10)
browser.set_window_size(1400,900)
import time

def search():
    try:
        browser.get("https://www.taobao.com")
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(29)")))
        target = browser.find_element_by_css_selector('body > div:nth-child(29)')
        actions = ActionChains(browser)
        actions.move_to_element(target)
        actions.perform()
    except TimeoutException:
        search()

search()
```

如果页面是ajax动态渲染的,页面的高度随时变化的,所以这个方法很有可能跳不到页面底部。

## js方法scrollIntoView

```python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


browser=webdriver.Chrome("G:/dj/chromedriver.exe")
wait=WebDriverWait(browser,10)
browser.set_window_size(1400,900)
import time

def search():
    try:
        browser.get("https://www.taobao.com") total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(29)")))

        browser.execute_script('arguments[0].scrollIntoView(true);', total)

    except TimeoutException:
        search()
search()
```

如果页面是ajax动态渲染的,页面的高度随时变化的,所以这个方法很有可能跳不到页面底部。

## js方法scrollBy

```python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


browser=webdriver.Chrome("G:/dj/chromedriver.exe")
wait=WebDriverWait(browser,10)
browser.set_window_size(1400,900)
import time

def search():
    try:
        browser.get("https://www.taobao.com")

        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(29)")))

        for i in range(15):
            browser.execute_script("window.scrollBy(0, 1000)")
            time.sleep(1)

    except TimeoutException:
        search()

search()
```

time.sleep必须要加，适合ajax动态渲染的页面，分多次跳到页面底部。

## send_keys(Keys.END)模拟向页面发送空格键

```python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


browser=webdriver.Chrome("G:/dj/chromedriver.exe")
wait=WebDriverWait(browser,10)
browser.set_window_size(1400,900)
import time

def search():
    try:
        browser.get("https://www.taobao.com")

        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(29)")))

        for i in range(5):
             browser.find_element_by_tag_name('body').send_keys(Keys.END)
             time.sleep(1)
    except TimeoutException:
        search()
search()
```

适合ajax动态渲染的页面，分多次跳到页面底部。

## 页面为ajax动态加载

```python
driver = webdriver.Chrome()

read_mores = driver.find_elements_by_xpath('//a[text()="加载更多"]')

for read_more in read_mores:
    driver.execute_script("arguments[0].scrollIntoView();", read_more)
    driver.execute_script("$(arguments[0]).click();", read_more)
```

