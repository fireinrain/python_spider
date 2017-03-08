#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import datetime
import lxml


# 获取页面中的所有内链的列表
def get_inter_links(bsobj,include_url):
    inter_links = []
    # 找出所有以/为开头的链接
    for link in bsobj.findAll("a",href=re.compile("^(/|.*"+include_url+")")):
        if link.attrs['href'] is not None:
            inner_link = link.attrs['href']
            if inner_link not in include_url:
                include_url.append(inner_link)
    return inter_links


# 获取页面的所有外链的列表
def get_external_links(bsobj,external_url):
    external_links = []
    for link in bsobj.findAll("a",href=re.compile("^(http|www)((?!"+external_url+").)*$")):
        if link.attrs['href'] is not None:
            inner_link = link.attrs['href']
            if inner_link not in external_links:
                external_links.append(inner_link)
    return external_links


# 分割地址
def split_address(address):
    address_parts = address.replace("http://","").split("/")
    return address_parts


# 获取随机外链
def get_random_external_link(start_page):
    html = urlopen(start_page)
    bsobj = BeautifulSoup(html.read(),"lxml")
    # print(html.read())
    external_links = get_external_links(bsobj,split_address(start_page)[0])
    if len(external_links) == 0:
        inter_links = get_inter_links(start_page)
        return get_external_links(random.choice(inter_links))
    else:
        return random.choice(external_links)


def follow_external_only(start_site):
    external_link = get_random_external_link("http://oreilly.com")
    print("随机外链："+external_link)
    follow_external_only(external_link)



if __name__ == "__main__":
    # strs = "http://www.baidu.com/music"
    # sss = split_address(strs)
    # print(sss)
    # get_random_external_link(strs)
    follow_external_only("http://oreilly.com")