
import time
from selenium import webdriver

wd = webdriver.Chrome('D:/bigdatastudy/chromedriver/chromedriver.exe') #파이썬 윈도우 intereter가 /를 \로 바꿔줌
wd.get('http://www.google.com')

time.sleep(5)
html = wd.page_source
print(html)

wd.quit()