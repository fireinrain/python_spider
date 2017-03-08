#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com
import re
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup

pages = set()


def get_links(page_url):
    global pages
    html = urlopen("http://en.wikipedia.org" + page_url)
    bsobj = BeautifulSoup(html.read(), "lxml")
    try:
        print(bsobj.h1.get_text())
        print(bsobj.find(id="mw-content-text").findAll("p")[0])
        print(bsobj.find(id="ca-edit").find("span").find("a").attrs["href"])
    except AttributeError as e:
        print("页面缺少查询的属性")
    for link in bsobj.findAll("a", {"href": re.compile("^(/wiki/)((?!:).)*$")}):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                # 遇到新页面
                new_page = link.attrs['href']
                print("------\n" + new_page)
                pages.add(new_page)
                get_links(new_page)


get_links("")
