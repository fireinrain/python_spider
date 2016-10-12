#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com



import requests
import asyncio
import http.cookiejar

from random import choice
from bs4 import BeautifulSoup

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
user_agent=choice(UserAgent)

headers = {
        'Host':'btso.pw',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'AD_enterTime=1476235339; AD_jav_b_SM_T_728x90=0; AD_javu_b_SM_T_728x90=0; AD_wav_b_SM_T_728x90=0; AD_wwwp_b_SM_T_728x90=1; AD_jav_b_SM_B_728x90=1; AD_clic_b_POPUNDER=2; AD_exoc_b_SM_T_728x90=2; AD_adca_b_POPUNDER=2; _ga=GA1.2.934399783.1476235343; _gat=1',
        }

filename = 'cookie'

# 建立一个会话，可以把同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
session = requests.Session()
# 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
# 而MozillaCookieJar类是存为'/.txt'格式的文件
session.cookies = http.cookiejar.LWPCookieJar(filename)
# 若本地有cookie则不用再post数据了
try:
    # 参数ignore_discard=True表示即使cookies将被丢弃也把它保存下来
    # 它还有另外一个参数igonre_expires表示当前数据覆盖（overwritten）原文件
    session.cookies.load(filename=filename, ignore_discard=True)
except:
    print('Cookie未加载！')


def url_open(links):

    # 创建请求对象，并添加头标识
    req = session.get(links,headers=headers)
    # 打开url
    response = req.content
    # 获取内容，bytes
    return response

# 将打开的网页转换为bs4对象，方便网页内容的查找
def url_open_deal(links):
    response=url_open(links)
    soup = BeautifulSoup(response, 'lxml')
    return soup


if __name__=='__main__':
    # url='https://btso.pw/magnet/detail/hash/1CBF363D7BEE577305765655C388DA07AB3B292E'
    url='https://btso.pw/search/'
    query_str=input('请输入要查询的关键字：')
    soup=url_open_deal(url+query_str)
    print(soup)