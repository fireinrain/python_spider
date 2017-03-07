#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

import lxml
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup



# 导入相关的库类
# 包含请求，错误，解析

def get_title(url):
    try:
        html = urlopen(url)  # html返回的是字节流
    except HTTPError as e:
        return None
    try:
        bsobj = BeautifulSoup(html.read(), "lxml")  # 需要读取
        title = bsobj.head.title
        # print(bsobj)
    except AttributeError as e:
        return None
    return title


# 测试
title = get_title("http://www.baidu.com")
if title == None:
    print("title can not be found")
else:
    print(title)

# 测试bs4类里面的一些实用方法
test_url = "https://baike.baidu.com/"


def test_bs4_find(test_url):
    link_list = []
    try:
        html = urlopen(test_url)  # html返回的是字节流
    except HTTPError as e:
        return None
    try:
        bsobj = BeautifulSoup(html.read(), "lxml")  # 需要读取
        print(bsobj)
        tags = bsobj.findAll("a")
        for i in tags:
            link_list.append(i.get_text().strip().replace("\n", ""))

    except AttributeError as e:
        return None
    return link_list


# 测试属性查找
def test_bs4_attri(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsobj = BeautifulSoup(html, "lxml")
        fenlei = bsobj.findAll("div", {"class": "column"})
        for i in fenlei:
            print(i)
    except AttributeError as e:
        return None


# 测试bs4中的re查找
def test_bs4_re(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsobj = BeautifulSoup(html, "lxml")
        fenlei_urls = bsobj.findAll("a", {"href": re.compile("/[a-z]+/.")})
        for i in fenlei_urls:
            print(i)
    except AttributeError as e:
        return None
if __name__ == "__main__":
    # link_list = test_bs4_find(test_url)
    # print(link_list)

    # test_bs4_attri(test_url)

    test_bs4_re(test_url)
