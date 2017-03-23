#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql
import lxml

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', charset='utf8', db='mysql')
# 获取游标
cur = conn.cursor()
cur.execute('use scraping')




# 将获取到的标题和内容存入数据库
def store(title, content):

    cur.execute("insert into pages (title,content) values (%s,%s)",(title, content))
    # 提交写入数据
    cur.connection.commit()


def getLinks(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)

    bsj = BeautifulSoup(html, "lxml")
    # print(bsj)
    title = bsj.find("title").get_text()
    # print(title)
    content = bsj.find("div",{"id":"mw-content-text"}).find("p").get_text()
    # print(content)
    store(title,content)
    print("写入{1}",title)

    return bsj.find("div",{"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))




if __name__ == "__main__":
    # 设置随机数种子
    random.seed(datetime.datetime.now())

    links = getLinks('/wiki/Kevin_Bacon')

    try:
        while len(links)> 0:
            new_article = random.choice(links).attrs['href']
            print(new_article)
            links = getLinks(new_article)
    finally:

        cur.close()
        conn.close()