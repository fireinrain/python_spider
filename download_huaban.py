#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

# 下载花瓣网的素材
# 功能
# 1.查询关键词
# 2.自定义下载张数

import re
import os
import requests
from time import sleep,time
from random import choice
from multiprocessing.dummy import Pool as ThreadPool

global photo_number
global page_count
global image_data
image_data=[]
page_count = 0
photo_number = 0


UserAgent = [
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
]


TimeOut = 30
user_agent = choice(UserAgent)
head = {'User-Agent': user_agent}




def downfile(down_data):
    print("开始下载：", down_data[2])
    image_url=down_data[1]

    # 处理传传进来的参数
    # 文件名有的不符合规范，所以要处理
    name_string=down_data[0]
    # name=[''.join(i) for i in name_list if i in '?、\*" <>|']
    # 还没有解决文件名过滤问题
    # for i in ['?', '、', '\\', '*', '\"', '<', '>', '|']:
    #     name_string = name_string.strip(i)
    # print(name_string)
    try:
        resource = requests.get(image_url, stream=True, headers=head).content
        with open(name_string, 'wb') as file:
            file.write(resource)
    except Exception as e:
        # print("下载失败", e)
        with open(down_data[2]+ '.jpg', 'wb') as file:
            file.write(resource)


def request_page_text(url):
    try:
        Page = requests.session().get(url, headers=head, timeout=TimeOut)
        Page.encoding='utf-8'
        return Page.text
    except Exception as e:
        print("请求失败了...重试中(5s)", e)
        sleep(5)
        print("暂停结束")
        request_page_text(url)


def request_url_download(url):
    global page_count
    global image_data
    page_count += 1
    global photo_number
    # print("请求网址：", url)
    text = request_page_text(url)
    pattern = re.compile('{"pin_id":(\d*?),.*?"key":"(.*?)",.*?"raw_text":"(.*?)",.*?"like_count":(\d*?),.*?"repin_count":(\d*?),.*?"username":"(.*?)".*?}', re.S)
    # 参数re.S 是正则表达式，编译参数标识re.DOTALL，即.匹配除、\n 所有字符
    img_query_items = re.findall(pattern, text)
    # print(img_query_items)
    max_pin_id = 0


    for url_items in img_query_items:
        max_pin_id = url_items[0]
        x_key = url_items[1]
        # 图片标题
        x_file_title = url_items[2]
        x_like_count = int(url_items[3])
        x_repin_count = int(url_items[4])
        # 图片收集地址
        x_author = url_items[5]
        # if (x_repin_count > 10 and x_like_count > 10) or x_repin_count > 100 or x_like_count > 20:
        print("开始获取第{0}张图片".format(photo_number))
        url_item = url_image + x_key
        filename = x_file_title + ".jpg"
        if os.path.isfile(filename):
            print("文件存在：", filename)
            continue
        if photo_number >= image_numbers:
            # 结束函数
            return image_data
        image_data.append([filename, url_item, str(max_pin_id)])
        # downfile(filename, url_item)
        photo_number += 1
    sleep(1)
    request_url_download(url_query+str(page_count))
    return image_data



if __name__=='__main__':
    url_image = 'http://hbimg.b0.upaiyun.com/'

    query_string=input('请输入要查询的关键词：')
    global url
    url = "http://huaban.com/search/?q="+query_string+"&sort=all"
    global image_numbers
    image_numbers=int(input('下载多少张：'))
    down_dir = query_string


    url_query = "http://huaban.com/search/?q="+query_string+"&per_page=20&wfl=1&page="

    if not os.path.exists(down_dir):
        os.makedirs(down_dir)
        os.chdir(down_dir)
    start_time=time()
    down_data=request_url_download(url + str(page_count))
    # 开启线程池去下载图片
    pool=ThreadPool(5)
    result=pool.map(downfile,down_data)
    pool.close()
    pool.join()
    print(len(down_data))
    end_time=time()
    print('共下载%s张素材，耗时%.2fs' %(image_numbers,end_time-start_time))



