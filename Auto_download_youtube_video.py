#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

# 初期的目标
# 该脚本尝试使用selenium驱动浏览器获取youtube的视频，并下载

# 初期需要实现的是指定一个youtube的播放列表的所有视频

# 第二步是获取每个视频的英文机翻字幕

# 第四部是尝试将下载的视频进行上传处理


# 目前的困难
# 下载好的视频本身是没有内嵌字幕的，所以上传到视频是生肉
# 电脑比较垃圾所以在进行压制的时候需要大量的处理时间


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()  # Get local session of firefox
browser.get("http://www.yahoo.com")  # Load page

elem = browser.find_element_by_name("p")  # Find the query box
elem.send_keys("seleniumhq" + Keys.RETURN)
time.sleep(0.2)  # Let the page load, will be added to the API


