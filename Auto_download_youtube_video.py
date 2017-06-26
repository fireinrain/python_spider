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

# 整个浏览器的当前用户配置
profile_dir = r"C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\mmuh2f5e.default"

profile = webdriver.FirefoxProfile(profile_dir)
# 加载插件
# profile.add_extension(r"D:\Firefox\browser\extensions\{972ce4c6-7e08-4474-a285-3208198ce6fd}.xpi")
# 激活插件
# profile.set_preference("extensions.firebug.allPagesActivation", "on")

browser = webdriver.Firefox(profile)
# 人为的设置一个播放列表
play_list = "https://www.youtube.com/playlist?list=PLRsbF2sD7JVqk90s0ogP_dcfM9T-y1DRm"

browser.get(play_list)

try:
    element_button = browser.find_element_by_xpath('//*[@id="pl-video-list"]/button')
    while True:
        if element_button:
            element_button.click()
            time.sleep(2)
        else:
            break

except Exception as e:
    print("加载完成")

table_list = browser.find_element_by_xpath('//*[@id="pl-video-table"]')
# table_list.find_element_by_xpath('//*[@id="pl-load-more-destination"]/tr[1]/td[4]')
link_list = table_list.find_elements_by_xpath('//*[@id="pl-load-more-destination"]/tr/td/a')
link_element_container = []
for i in link_list:
    link_element = i.get_attribute('href')
    link_element_container.append(link_element)
    # print(link_element)

# 把获得的链接转交给一个解析网页来解析
# 1.新建一个窗口，并打开解析网页
# 2.找到输入框，把视频地址提交进去
# 3.确认下载（需要设置下载的目录）
convert_video_url = 'http://keepvid.com/'
js = 'window.open(http://keepvid.com/);'
browser.execute_script(js)

print(browser.current_window_handle)  # 输出当前窗口句柄（百度）
handles = browser.window_handles  # 获取当前窗口句柄集合（列表类型）
print(handles)  # 输出句柄集合

for handle in handles:  # 切换窗口（切换到搜狗）
    if handle!=browser.current_window_handle:
        print('switch to ', handle)
        browser.switch_to_window(handle)
        print(browser.current_window_handle)  # 输出当前窗口句柄（搜狗）
        break


browser.close() #关闭当前窗口（搜狗）
browser.switch_to_window(handles[0]) #切换回百度窗口


input("打断")
