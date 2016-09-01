#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang



import urllib.request
import os
from bs4 import BeautifulSoup
from time import sleep
import random

# 创建爬取页面
def star_get():
    for i in range(1,1000):
        star_url='https://www.javbus2.com/star/'+str(i)
    return star_url

# 创建网站链接打开器
def url_open(links):
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
    user_agent=UserAgent[random.randint(0,len(UserAgent)-1)]

    head = {'User-Agent': user_agent}
    # 创建请求对象，并添加头标识
    req = urllib.request.Request(links, headers=head)
    # 打开url
    response = urllib.request.urlopen(req)
    # 获取内容，bytes
    sc = response.read()
    # print(sc)
    return sc
# 将打开的网页转换为bs4对象，方便网页内容的查找
def url_open_deal(links):
    sc=url_open(links)
    soup = BeautifulSoup(sc, 'lxml')
    return soup

    # print(dom_res)

# 获取页面信息列表
def get_mov_url(page_url):
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
    user_agent = UserAgent[random.randint(0, len(UserAgent)-1)]
    head = {'User-Agent': user_agent}
    # 创建请求对象，并添加头标识
    req = urllib.request.Request(page_url, headers=head)
    # 打开url
    response = urllib.request.urlopen(req)
    # 获取内容，bytes
    sc = response.read()
    soup = BeautifulSoup(sc, 'lxml')
    image_txt = soup.select('a.movie-box')
    introduce=soup.select('div.photo-info')
    pic_url=soup.select('div.photo-frame img')
    pic_urls = []


    for each_pic in range(len(pic_url)):

        # 获取图片封面地址
        each_pic_url = pic_url[each_pic].get('src')
        pic_urls.append(each_pic_url)

    # print(pic_urls)
    introduce_text=introduce[0].get_text()
    movie_urls=[]
    movie_urls.append(introduce_text)

    for i in range(len(image_txt)):
        # print(i)
    # 获取影片描述信息
        movie_url = image_txt[i].get_text()
        movie_urls.append(movie_url)
    return (movie_urls,pic_urls)

# """处理获得的信息列表"""
def message_process(movie_urls):
    text_container=[]
    for i in movie_urls:
        i=i.split('\n')

        for each_line in i:
            if each_line =='' or i==' / ':
                pass
            else:
                text_container.append(each_line)
    return text_container
# 页面信息文件保存
def message_store(text_container):
    dir=text_container[0]
    if len(dir)>10:
        dir=dir[:5]
    else:
        pass
    if os.path.exists(dir):
        os.chdir(dir)
    else:
        os.makedirs(dir)
        os.chdir(dir)
    with open(dir+'.txt','a+',encoding='utf-8') as file:
        for each_mes in text_container:
            file.write(each_mes+'\n')
# 页面图片保存
def pic_url_get(page_url):
    soup=url_open_deal(page_url)
    dom_res = soup.select('a')



if __name__=='__main__':
    list=get_mov_url('https://www.javbus2.com/star/92l')
    text=list[0]
    pic=list[1]
    # print(text)
    # print(pic)

    result=message_process(text)

    message_store(result)
    for url in pic:
        pic_res=url_open(url)
        with open(url[-7:],'wb+') as file:
            file.write(pic_res)
            print('下载'+url+'成功')
        sleep(2)
    # url_open_deal('http://wwww.baidu.com')

