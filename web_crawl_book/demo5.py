#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

# 导入必要的包
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import datetime
import random
import re
import lxml
import json

# 随机种子
random.seed(datetime.datetime.now())


# 获取维基解密上页面的链接
def get_links(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)
    bsobj = BeautifulSoup(html, "lxml")
    return bsobj.find("div", {"id": "bodyContent"}).findAll(
        "a", {"href": re.compile("^(/wiki/)((?!:).)*$")}
    )


# 获取历史编辑页面，找出编辑过该页面的ip地址
def get_history_ips(page_url):
    # 编辑历史页面url链接的格式：
    # http://en.wikipedia.org/w/index.php?title="+page_url+"&action=history
    page_url = page_url.replace("/wiki/", "")
    history_url = "http://en.wikipedia.org/w/index.php?title=" + page_url + "&action=history"
    print("history url is:" + history_url)

    html = urlopen(history_url)
    bsobj = BeautifulSoup(html, "lxml")
    # 找到页面属性为mw-anouselink的链接
    # ip地址就是在那里
    ip_set = set()
    ip_address = bsobj.findAll("a", {"class": "mw-anonuserlink"})
    for ip in ip_address:
        ip_set.add(ip.get_text())
    return ip_set


# 将ip转换为国家的地址（借助已有的ip）
def get_country_with_ip(ip_address):
    try:
        response = urlopen("http://freegeoip.net/json/" + ip_address).read().decode("utf-8")  # 获取的页面是二进制码，需要读取，然后解码
    except HTTPError as e:
        print("ip转化失败")
        return None
    jsonto_response = json.loads(response)
    return jsonto_response.get("country_code")


links = get_links("/wiki/Python_(programming_language)")
# print(links)

while (len(links) > 0):
    for link in links:
        print("---------------")
        history_ip = get_history_ips(link.attrs["href"])
        # 获取ip集合
        for his_ip in history_ip:
            print(his_ip)
            country = get_country_with_ip(his_ip)
            if country is not None:
                print(his_ip + "is from:" + country)

    # 在获取了某个页面所有的词条的编辑页面ip后，在这中随机
    # 选取一个词条访问，重复该过程
    new_link = random.choice(links)
    links = get_links(new_link)

