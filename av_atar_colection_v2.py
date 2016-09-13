#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

"""
required:
requests
bs4
time
os

脚本尝试爬取url：https://www.javbus2.com/
尝试做一个查询脚本，并自动将获取的信息保存下来
功能描述
1.输入女优名字可以进行查询，如果错误将返回没有查到
2.输入番号，可以进行番号查询，查询结果，包括该女优的信息，作品信息
3.选着作品会将对应的磁力链接下载下来，对应会创建一个用于保存的文件夹
4.第一步查询到的结果，包含女优的详细信息，和所有的作品信息


"""

import requests
import re
import os
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from random import randint
from time import time
from multiprocessing.dummy import Pool as ThreadPool


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

def url_open(links):

    user_agent=choice(UserAgent)

    head = {'User-Agent': user_agent}
    # 创建请求对象，并添加头标识
    req = requests.post(links, headers=head,timeout=1000)
    # 打开url
    response = req.content
    # 获取内容，bytes
    return response

# 将打开的网页转换为bs4对象，方便网页内容的查找
def url_open_deal(links):
    response=url_open(links)
    soup = BeautifulSoup(response, 'lxml')
    return soup


def search_star(film_about):
    """
    根据输入的关键词查询并返回查询结果
    各个视屏的url地址
    :param film_about:
    :return:
    """
    search_url="https://www.javbus2.com/search/"+film_about

    soup=url_open_deal(search_url)
    # 进入查询入口
    image_txt = soup.select('a.movie-box')
    # introduce = soup.select('div.photo-info')
    # pic_url = soup.select('div.photo-frame img')

    # 判断查询结果，如果关键字是番号那么结果就是一个片子
    # 根据这个片子提取片子女神，然后在查询，获得查询结果的第一页链接
    if len(image_txt)==1:
        star_urls = []
        enter_url=image_txt[0].get('href')
        soup2=url_open_deal(enter_url)
        image_txt2 = soup2.select('div.col-md-3 p a')
        for i in image_txt2:
            url=i.get('href')
            name = i.get_text()
            try:
                if re.match('^https://www.javbus2.com/star/.', url):
                    star=url

                    break
                    # print(star)
            except Exception as e:
                continue
        # print(name)
        soup3 = url_open_deal(url)
        image_txt3 = soup3.select('a.movie-box')
        avstar_introduce=soup3.select('div.photo-info')[0].get_text()
        print(avstar_introduce)
        for item in image_txt3:
            each_url = item.get('href')
            star_urls.append(each_url)
        # url_get=image_txt2[]
        # print(star_urls)
    #    如果关键字是女神名字，那么直接返回查询结果的第一页
    else:
        name=film_about
        star_urls=[]

        enter_url = image_txt[0].get('href')
        soup2 = url_open_deal(enter_url)
        image_txt2 = soup2.select('div.col-md-3 p a')
        for i in image_txt2:
            url = i.get('href')
            name = i.get_text()
            try:
                if re.match('^https://www.javbus2.com/star/.', url):
                    star = url

                    break
                    # print(star)
            except Exception as e:
                continue
        # print(name)
        soup3 = url_open_deal(url)
        image_txt3 = soup3.select('a.movie-box')
        avstar_introduce = soup3.select('div.photo-info')[0].get_text()
        print(avstar_introduce)
        for item in image_txt3:
            each_url = item.get('href')
            star_urls.append(each_url)

    # print(len(image_txt))
    return [star_urls,name,avstar_introduce]




def star_each_film(url):
    # star_urls=star_urls_result[0]
    # star_name=star_urls_result[1]
    # print(star_name)
    # for url in star_urls:
    # sleep(1)
    soup = url_open_deal(url)
    title=soup.select('h3')[0].get_text()
    film_info=soup.select('div.col-md-3')[0].get_text()
    film_pic_url=soup.select('div.col-md-9 a.bigImage')[0].get('href')

    # 获取磁力链接的相关参数，用于构造请求url
    magnent_str= soup.select('script')[8].get_text()
    magnent_str_list=magnent_str.split(' ')
    gid=magnent_str_list[3].split(';')[0]
    # lang='zh'
    img=magnent_str_list[9].split(';')[0][1:-1]
    # print(img)
    uc='0'
    floor=str(randint(99,1000))

    # 构造magnent磁力链接的请求url
    # url = 'https://www.javbus2.com/ajax/uncledatoolsbyajax.php?gid=31588090853&lang=zh&img=https://pics.javbus.info/cover/5jgu_b.jpg&uc=0&floor=791'
    magnent_url="https://www.javbus2.com/ajax/uncledatoolsbyajax.php?"+"gid="+gid+"&lang=zh&img="+img+"&uc=0&floor="+floor
    # print(type(magnent_url))
    def open_mag_url(magnent_url,url):
        agent=choice(UserAgent)

        headers = {
            "authority": "www.javbus2.com",
            "method": "GET",
            "referer": url,
            "user-agent": agent,
        }

        req = requests.get(magnent_url, headers=headers).content
        soup = BeautifulSoup(req, 'lxml')
        mag = soup.select('tr')
        # print(mag)
        magnent_container = []
        for i in mag:
            magnent = i.td.a.get('href')
            magnent_info = i.get_text().split()
            # magnent_info=magnent_info[0]+'_'+magnent_info[1]+'_'+magnent_info[2]
            magnent_info.append(magnent)
            magnent_container.append(magnent_info)
        return magnent_container

        # 获取磁力链接列表信息
    magnent_container=open_mag_url(magnent_url,url)
    # print(magnent_container)

    sample_images=soup.select('div#sample-waterfall a.sample-box')
    sample_images_urls=[]
    for image in sample_images:
        image_url=image.get('href')
        sample_images_urls.append(image_url)
    # print(sample_images_urls)
    return [title,film_info,film_pic_url,magnent_container,sample_images_urls]

# 获取单个页面的磁力链接，他是js加载的
# 通过开发者工具分析，要构造好请求的url，和headers
# 请求返回的才是一段html，包含磁力链接
def parse_films_infomation(item):
    title = item[0]
    title_deal = ''.join(title.split('*'))
    os.mkdir(title_deal)

    os.chdir(title_deal)
    film_info = item[1]
    with open('film_tag.txt', 'w+', encoding='utf-8') as file:
        for i in film_info:
            file.write(i)

    magnent_container = item[3]
    with open('magnent.txt', 'w+', encoding='utf-8') as file2:
        for per_list in magnent_container:
            strings = ''.join(i + '   ' for i in per_list)
            file2.write(strings + '\n')

    # os.mkdir('sample_img')
    # os.chdir('sample_img')

    film_pic_url = item[2]
    sample_images_urls = item[4]
    print(film_pic_url)
    print(type(sample_images_urls))
    # sample_images_urls.append(film_pic_url)
    # 设置线程池
    child_pool = ThreadPool(16)
    result = child_pool.map(download, sample_images_urls)
    print('下载完成')
    child_pool.close()
    child_pool.join()
    os.chdir('../')


def download(url):
    req=requests.get(url).content
    with open(url.split('/',6)[-1],'wb') as file:
        file.write(req)

def main():
    film_about=input('请输入女盆友相关信息(番号或是名字)：')
    star_urls_and_name=search_star(film_about)
    # print(star_urls_and_name)
    # 影片数量
    number=len(star_urls_and_name[0])
    time_start=time()
    star_urls=star_urls_and_name[0]
    # for url in star_urls:
    #
    #     info_list=star_each_film(url)
    #     print(info_list)

    # 用map函数代替for循环
    # 经过调试16个线程获取时间最短
    pool=ThreadPool(16)
    results=pool.map(star_each_film,star_urls)
    pool.close()
    pool.join()

    for infomation in results:
        parse_films_infomation(infomation)
    # print(results)
    time_end = time()
    print('共耗时：%.2f秒,共找到：%d部' % (time_end-time_start,number))


    # url='https://www.javbus2.com/SNIS-642'
    # star_each_page(url)


if __name__=='__main__':
    main()