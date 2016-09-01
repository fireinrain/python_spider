#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
"""
本程序还没有调试完成
将采集到的代理ip使用多线程
来进行验证，并返回通过的ip代理列表
"""

import urllib2
import threading

inFile = open('proxy.txt', 'r')
outFile = open('available.txt', 'w')
url = 'http://www.lindenpat.com/search/detail/index?d=CN03819011@CN1675532A@20050928'
lock = threading.Lock()


def test():
    lock.acquire()
    line = inFile.readline().strip()
    lock.release()
    # if len(line) == 0: break
    protocol, proxy = line.split('=')
    cookie = "PHPSESSID=5f7mbqghvk1kt5n9illa0nr175; kmsign=56023b6880039; KMUID=ezsEg1YCOzxg97EwAwUXAg=="
    try:
        proxy_support = urllib2.ProxyHandler({protocol.lower(): '://'.join(line.split('='))})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        request.add_header("cookie", cookie)
        content = urllib2.urlopen(request, timeout=4).read()
        if len(content) >= 1000:
            lock.acquire()
            print
            'add proxy', proxy
            outFile.write('\"%s\",\n' % proxy)
            lock.release()
        else:
            print
            '出现验证码或IP被封杀'
    except Exception, error:
        print
        error


all_thread = []
for i in range(500):
    t = threading.Thread(target=test)
    all_thread.append(t)
    t.start()

for t in all_thread:
    t.join()

inFile.close()
outFile.close()