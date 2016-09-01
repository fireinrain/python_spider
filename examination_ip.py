#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

"""
用于检查抓取的代理ip可用的项目
没有使用多线程，所以效率比较低
"""
import urllib.request
import time
import random

from socket import timeout
from urllib.error import URLError,HTTPError
from http.client import RemoteDisconnected as remote

def check_ip_proxy(protocle,ip_port,test_url=''):
    # 显示目前的ip
    # test_url='http://1212.ip138.com/ic.asp'
    test_url = 'http://www.baidu.com'
    proxy_support=urllib.request.ProxyHandler({protocle:ip_port})
#     定制一个openner
    opener=urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
#     安装opener
    urllib.request.install_opener(opener)
#     添加头部

    req=urllib.request.urlopen(test_url,timeout=5).getcode()
    # req=urllib.request.urlopen(test_url,timeout=5)
    # response=req.read().decode('gb2312')
    # print(response)
#     测试状态码
    if req==200:
        print('验证通过')
        return [protocle,ip_port]

if __name__=='__main__':
    with open('ip_bus.txt','r') as file:
        # 这是一种写法
        # while True:
        #     a=file.readline()
        #     if a:
        #         b=a.split('=')
        #         protocle=b[0]
        #         ip_port=b[1]
        #         check_ip_proxy(protocle,ip_port)
        #         print(protocle,ip_port)
        #         time.sleep(1)
        #     else:
        #         break

    #     第二种写法，单个验证
    #     a=file.readlines()
    #     b=random.choice(a)
    #     c = b.split('=')
    #     protocle=c[0].lower()
    #     ip_port=c[1]
    #     check_ip_proxy(protocle,ip_port)

    # 第三种写法
            a=file.readlines()
            list=[]
            for i in a:
                c = i.split('=')
                protocle=c[0].lower()
                ip_port=c[1]
                try:
                    checked=check_ip_proxy(protocle,ip_port)
                    list.append(checked)
                except (HTTPError,URLError,timeout,remote, ConnectionResetError) as e:
                    # print(e)
                    continue
                time.sleep(1)

            # print(list)
    with open('can_used_ip.txt', 'w+') as file:
        for each_line in list:
            file.write(each_line[0]+'='+each_line[1])
            print('验证完成')

    # check_ip_proxy()





