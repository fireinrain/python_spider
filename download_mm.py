#! /usr/bin/python3
# _*_encoding:utf-8_*_
# Written by liuzhaoyang
"""
爬取煎蛋网妹妹图片
输入要爬取的页数
"""

import urllib.request
import os
from bs4 import BeautifulSoup
from time import sleep


def page_url():
    pages=input("请输入下载页数：")
    pages=[i for i in range(int(pages))]
    page_urls=[]
    name_list=[]
    start_url='http://jandan.net/ooxx/page-2110#comments'
    for i in pages:

        urls='http://jandan.net/ooxx/page-'+str((2110-int(i)))+'#comments'
        page_urls.append(urls)
        name_list.append(str((2110-int(i))))
    return (page_urls,name_list)


def get_pic_url(page_url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    head = {'User-Agent': user_agent}
    # 创建请求对象，并添加头标识
    req = urllib.request.Request(page_url, headers=head)
    # 打开url
    response = urllib.request.urlopen(req)
    # 获取内容，bytes
    sc = response.read()
    soup = BeautifulSoup(sc, 'lxml')
    image = soup.select('img')
    image_urls=[]

    for i in range(len(image)-5):

    # 获取图片url地址
        image_url = image[i].get('src')
        image_urls.append(image_url)

    return image_urls


def image_down(img_url,name):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    head = {'User-Agent': user_agent}
    # 创建请求对象，并添加头标识
    req = urllib.request.Request(img_url, headers=head)
    # 打开url
    response = urllib.request.urlopen(req)
    # 获取内容，bytes
    sc = response.read()


    # 保存文件
    with open(name + '.jpg', 'wb') as file:
        file.write(sc)
        print('下载' + name + '.jpg' + '成功')

if __name__=='__main__':
    os.makedirs('MM_picture',exist_ok=True)
    os.chdir('MM_picture')
    list=page_url()
    page_list=list[0]
    name_list=list[1]
    print(list)
    for i in page_list:

        pic_res=get_pic_url(i)
        print(pic_res)
        i = 1
        for page in name_list:
            for n in pic_res:
                if i <= 22:
                    image_down(n,page+'_'+str(i+1))
                    i+=1
                    sleep(2)
                else:
                    continue

        sleep(1)
    print('下载完成')


