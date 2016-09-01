#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

"""
本程序还没有完成
主要作用是开启多个线程爬取代理ip
使用多线程检测代理ip的可用性
"""

# !/usr/bin/env python
# coding:utf-8
import urllib2
import re
import threading
import time
import MySQLdb
import requests

rawProxyList = []
checkedProxyList = []
# 抓取代理网站
targets = []
for i in xrange(1, 50):
    # target = r"http://www.proxy.com.ru/list_%d.html" % i    #自己可换网址
    target = r"http://www.kuaidaili.com/free/inha/%d/" % i
    targets.append(target)
# 抓取代理服务器正则
# p = re.compile(r'''<tr><b><td>(\d+)</td><td>(.+?)</td><td>(\d+)</td><td>(.+?)</td><td>(.+?)</td></b></tr>''')   #换网址就要换正则
p = re.compile(r'<tr>[\s|\S]*?<td>(.+?)</td>[\s|\S]*?<td>(.+?)</td>[\s|\S]*?<td>高匿名</td>[\s|\S]*?<td>.*?</td>')


# 获取代理的类
class ProxyGet(threading.Thread):  # 继承threading.Thread类
    def __init__(self, target):
        threading.Thread.__init__(self)  # 语法就这么写的，不用想太多
        self.target = target

    def getProxy(self):
        print
        "代理服务器目标网站： " + self.target
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.kuaidaili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        }
        req = requests.post(url=self.target, headers=headers)
        result = req.content  # 上下两句最基础的爬虫了吧
        # print chardet.detect(result)
        matchs = p.findall(result)
        #       print matchs
        for row in matchs:
            ip = row[0]
            port = row[1]
            # addr = row[4].decode("cp936").encode("utf-8")
            proxy = [ip, port]
            print
            proxy
            rawProxyList.append(proxy)  # 把用正则提取到的内容append到列表

    def run(self):
        self.getProxy()


# 检验代理的类
class ProxyCheck(threading.Thread):  # 继承threading.Thread类
    def __init__(self, proxyList):
        threading.Thread.__init__(self)  # 语法就这么写的，不用想太多
        self.proxyList = proxyList  # 初始化
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        self.testStr = "030173"

    def checkProxy(self):
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            # 设置ProxyHandler代理
            proxyHandler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (proxy[0], proxy[1])})
            # print r'http://%s:%s' %(proxy[0],proxy[1])
            # 通过cookies和proxyHandler来构建opener，顺便说下urlopen不支持cookie，http代理等功能所以、、、
            opener = urllib2.build_opener(cookies, proxyHandler)
            # 构造头部信息中的ua
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            # urllib2.install_opener(opener)
            # 记录下时间
            t1 = time.time()
            try:
                # req = urllib2.urlopen("http://www.baidu.com", timeout=self.timeout)
                # 创建一个请求，原理同urllib2的urlopen
                req = opener.open(self.testUrl, timeout=self.timeout)
                # print "urlopen is ok...."
                result = req.read()
                # print "read html...."
                # 统计出代理请求连接花费时间timeused
                timeused = time.time() - t1
                pos = result.find(self.testStr)
                # print "pos is %s" %pos
                # 判断是否正常打开百度且连接速度在要求范围内
                if (pos > -1) and (timeused < 5) and baidu_title == '百度一下，你就知道':
                    checkedProxyList.append((proxy[0], proxy[1], proxy[2], timeused))
                    # print "ok ip: %s %s %s %s" %(proxy[0],proxy[1],proxy[2],timeused)
                else:
                    continue
            except Exception, e:
                # print e.message  #可以打印异常
                continue

    def run(self):
        self.checkProxy()


if __name__ == "__main__":
    getThreads = []
    checkThreads = []
    # 对每个目标网站开启一个线程负责抓取代理，这段更多的是固定语法可套用
    for i in range(len(targets)):
        t = ProxyGet(targets[i])
        getThreads.append(t)
    for i in range(len(getThreads)):
        getThreads[i].start()
    for i in range(len(getThreads)):
        getThreads[i].join()
    print
    '.' * 10 + "总共抓取了%s个代理" % len(rawProxyList) + '.' * 10

    # 先举个简单的例子，单独copy出来打印结果一下就懂，不懂可以直接套就是
    # 这段代码相当于把l这个列表分成5份
    # l=range(1,100)
    # for i in range(5):
    #     print l[((len(l)+4)/5) * i:((len(l)+4)/5) * (i+1)]

    # 开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
    for i in range(20):
        t = ProxyCheck(rawProxyList[((len(rawProxyList) + 19) / 20) * i:((len(rawProxyList) + 19) / 20) * (i + 1)])
        checkThreads.append(t)
    for i in range(len(checkThreads)):
        checkThreads[i].start()
    for i in range(len(checkThreads)):
        checkThreads[i].join()
    print
    '.' * 10 + "总共有%s个代理通过校验" % len(checkedProxyList) + '.' * 10
    # 插入数据库，表结构自己创建，四个字段ip,port,speed,address
    # 下面其实更多是mysql的东西了，直接导出到txt或者csv都行，下面导出到txt格式为例
    f = open("hege_daili.txt", 'w+')
    for proxy in checkedProxyList:
        print
        "qualified: %s\t%s" % (proxy[0], proxy[1])
        f.write(proxy[0] + "\n")  # 换行写入
    f.close()
    # def db_insert(insert_list):
    #     try:
    #         conn = MySQLdb.connect(host="localhost", user="root", passwd="admin",db="m_common",charset='utf8')
    #         cursor = conn.cursor()
    #         cursor.execute('delete from proxy')                  #删除表中的数据
    #         cursor.execute('alter table proxy AUTO_INCREMENT=1') #加入一条新数据时，id从1开始
    #         #批量插入到数据库
    #         cursor.executemany("INSERT INTO proxy(ip,port,speed,address) VALUES (%s,%s,%s,%s)",insert_list)
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #     except MySQLdb.Error,e:
    #         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    # #代理排序持久化
    # proxy_ok = []
    # f= open("proxy_list.txt",'w+')
    # for proxy in sorted(checkedProxyList,cmp=lambda x,y:cmp(x[3],y[3])):
    #     if proxy[3] < 8:
    #         #print "checked proxy is: %s:%s\t%s\t%s" %(proxy[0],proxy[1],proxy[2],proxy[3])
    #         proxy_ok.append((proxy[0],proxy[1],proxy[3],proxy[2]))
    #         f.write("%s:%s\t%s\t%s\n"%(proxy[0],proxy[1],proxy[2],proxy[3]))
    # f.close()
    # db_insert(proxy_ok)
