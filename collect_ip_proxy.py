#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang


# step1  采集数据相关的函数
import urllib.request
import random
import time
from bs4 import BeautifulSoup

# 获取网站响应
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

# 将响应转换为soup对象
def soup_page_get(url):

    content=url_open(url)
    soup = BeautifulSoup(content, 'lxml')
    return soup



# 采集1
"""
采集西祠代理
"""
# # get the proxy
def get_xici():
    of = open('proxy.txt', 'w')
    for page in range(1, 10):
        url = 'http://www.xicidaili.com/nn/%s' % page

        soup = soup_page_get(url)
        trs = soup.find('table', {"id": "ip_list"}).findAll('tr')
        for tr in trs[1:]:
            tds = tr.findAll('td')
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            protocol = tds[5].text.strip()
            if protocol == 'HTTP' or protocol == 'HTTPS':
                of.write('%s=%s:%s\n' % (protocol, ip, port))
                print('%s://%s:%s' % (protocol, ip, port))
        time.sleep(2)


#  采集2          采集有代理
# -*- coding:utf8 -*-
# 该网站采取js动态加载文档
# 现阶段没办法实现模拟js动态加载
# 所以采集失败

def get_ydl():
    url='http://www.youdaili.net/Daili/http/'
    soup=soup_page_get()

    # 通过soup对象对网站文档数据进行提取
    def page_get_process(soup):
        ip_url = soup.select('ul.newslist_line li a')
        page=[]
        for i in ip_url:
            ip_page=i.get('href')
            page.append(ip_page)
        return page

    # 下载为文本
    def down_load(urls):
        soup=soup_page_get()
        of = open('proxy_ydl.txt', 'w')
        pass



# 采集3 采集ip巴士
def get_ip_bus():
    url='http://ip84.com/'
    content=url_open(url)
    soup = BeautifulSoup(content, 'lxml')

    def get_process(soup):
        ip_url = soup.select('table tr')
        page = []
        for i in ip_url[1:]:
            ip_page = i.get_text()
            ip_port=ip_page.split('\n')
            print(ip_port)
            if len(ip_port) < 5:
                continue
            else:
                if len(ip_port) > 11:
                    protocl = ip_port[8]

                    # print(ip_port[8])
                else:
                    protocl = ip_port[7]

                ip_port = ip_port[1:3]
                ip = protocl + '=' + ip_port[0] + ':' + ip_port[1]

                page.append(ip)
        # print(page)
        return page
    page=get_process(soup)
    def write_to_text(page):
        with open('ip_bus.txt','w',encoding='utf-8') as file:
            for line in page:
                file.write(line+'\n')
    write_to_text(page)
    print('采集成功')


# 采集4  采集秘密代理ip
def get_mimi_ip():
    url='http://www.mimiip.com/'
    content = url_open(url)
    soup = BeautifulSoup(content, 'lxml')

    def get_process(soup):
        ip_url = soup.select('div.widget tr')
        page = []
        for i in ip_url[1:]:
            ip_page = i.get_text()
            ip_port = ip_page.split('\n')
            if len(ip_port)<5:
                continue
            else:
                if len(ip_port)>14:
                    protocl = ip_port[8]
                    # print(ip_port)
                    # print(ip_port[8])
                else:
                    protocl = ip_port[7]

                ip_port = ip_port[1:3]
                ip = protocl+'='+ip_port[0] + ':' + ip_port[1]

                page.append(ip)
        # print(page)
        return page

    page = get_process(soup)

    def write_to_text(page):
        with open('mimi_ip.txt', 'w', encoding='utf-8') as file:
            for line in page:
                file.write(line + '\n')

    write_to_text(page)
    print('采集成功')

if __name__=='__main__':
    get_ip_bus()


#     table = soup.select('ul.newslist_line')
#     tr = table.findAll('tr')
#     for i in range(1,31):
#         td = tr[i].findAll('td')
#         proxy_ip = td[0].text.strip()
#         proxy_port = td[1].text.strip()
#         of.write('http=%s:%s\n' %(proxy_ip,proxy_port))
#         print ('http=%s:%s\n' %(proxy_ip,proxy_port))
#     time.sleep(2)
# of.closed
