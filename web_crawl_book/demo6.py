#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import lxml
import os

# 这是一个简单的例子
# html = urlopen("http://www.pythonscraping.com")
# bsobj = BeautifulSoup(html,"lxml")
# image_location = bsobj.find("a",{"id":"logo"}).find("img")["src"]
# urlretrieve(image_location,"logo.jpg")

download_dir = "downloaded"
base_url = "http://www.pythonscraping.com"


def get_absolute_url(base_url, source):
    if source.startswith("http://www."):
        url = "http://" + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "http://" + source
    else:
        url = base_url + "/" + source
    if base_url not in url:
        return None
    return url


def get_download_path(base_url, abs_url, download_dir):
    path = abs_url.replace("www", "")
    path = path.replace(base_url, "")
    path = download_dir + path
    dirs = os.path.dirname(path)

    if not os.path.exists(dirs):
        os.mkdir(dirs)

    return path

html = urlopen("http://www.pythonscraping.com")
bsobj = BeautifulSoup(html,"lxml")
download_list = bsobj.findAll(src=True)

for download in download_list:
    file_url = get_absolute_url(base_url,download["src"])
    if file_url is not None:
        print(file_url)

    urlretrieve(file_url,get_download_path(base_url,file_url,download_dir))