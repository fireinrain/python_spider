#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang


# 爬取拉勾网python招聘职位,信息

# 导入相关的模块
from time import sleep
from bs4 import BeautifulSoup
from random import choice
import requests

# 获取二进制页面
def html_get(url):
    filename='session'
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
    user_agent = choice(UserAgent)
    headers = {'User-Agent': user_agent}
    html = requests.get(url, headers=headers).content
    return html

# 获取职位页面网页
def html_parse(html):
    soup=BeautifulSoup(html,'lxml')
    item_get=soup.select('div.list_item_top a')
    urls=[]
    for i in item_get:
        url=i.get('href').strip('//')
        if "gongsi" in url:
            continue
        else:
            urls.append(url)
    return urls

# 提取页面信息
def get_page_info(page_html):
    soup = BeautifulSoup(page_html, 'lxml')
    job_info=soup.select('dd.job_bt p')
    detail=[]
    for i in job_info:
        word=i.get_text()
        detail.append(word)
    # company=soup.select('h1')[1].get_text()
    # print(a)
    return detail


def get_job_info(urls):
    pass

def get_last_page(url):
    pass

if __name__=="__main__":
    # html = html_get('http://www.lagou.com/lagouhtml/a44.html')
    # urls = html_parse(html)
    # print(urls)
    page=1
    item=0
    job_name=input('请输入职位名（如php）:').title()

    with open('lagou_job_java.txt', 'a+', encoding='utf-8') as file:
        while True:

            try:
                url='http://www.lagou.com/zhaopin/%s/%d' % (job_name,page)
                html = html_get(url)
                urls=html_parse(html)
                if urls:
                    print('正在采集第%d页' % page)
                    page += 1
                    for i in urls:
                        info_html = html_get("http://"+i)
                        detail = get_page_info(info_html)
                        for i in detail:
                            file.write(i.strip() + '\n')
                        # print('写入完成')
                        item+=1
                        sleep(1)
                else:
                    pass

            except Exception as e:
                print(e)
                print('共抓取%d页，%d个结果' % (page,item))
                break

