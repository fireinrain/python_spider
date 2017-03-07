#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com
import re
import lxml
import random
import datetime
from urllib.request import urlopen,urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# url = "https://baike.baidu.com/皇上"
# parse_url = urlparse(url)
# print(parse_url)
#解析url成为各个部分

# 随机数种子
random_seed = random.seed(datetime.datetime.now())

def get_page(url):
    try:
        html = urlopen("http://en.wikipedia.org"+url)
        bsobj = BeautifulSoup(html,"lxml")
    except HTTPError as e:
        print("无法连接")
    #获取该页面所有指向其他词条的链接
    # for link in bsobj.find("div",{"id":"bodyContent"}).findAll("a",{"href":re.compile("^(/wiki/)((?!:).)*$")}):
    #     if "href" in link.attrs:
    #         print(link.attrs['href'])
    return bsobj.find("div",{"id":"bodyContent"}).findAll("a",{"href":re.compile("^(/wiki/)((?!:).)*$")})




if __name__ == "__main__":
    url = "/wiki/Kevin_Bacon"
    urls = get_page(url)
    while(len(urls)>0):
        new_page = random.choice(urls).attrs["href"]
        print(new_page)
        urls = get_page(new_page)