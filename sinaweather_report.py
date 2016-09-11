#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

"""
一个简陋的天气查询脚本，抓取的是新浪天气的数据
第一次尝试使用类来进行爬取，多有不足，多多努力。
"""

import requests
# from time import sleep
from bs4 import BeautifulSoup
from random import choice


class Query:
    def __init__(self,*args):
        self.city=input("请输入城市或地区(拼音或汉字)：")
        self.url='http://php.weather.sina.com.cn/search.php?c=1&city=%s' % self.city
        self.UserAgent = [
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
            'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
            'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
            'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
            'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
        ]
        self.user_agent =choice(self.UserAgent)
        self.headers= {'User-Agent': self.user_agent}
    def get_page(self):
        html=requests.post(self.url,headers=self.headers).content
        soup=BeautifulSoup(html,'lxml')
        weather = soup.select('div.m_left,div.weather_list')
        today=weather[0].get_text()
        # print(today)
        # # print(len(weather),type(weather))
        today_list=today.split('\n\n\n')
        today_info="今天白天：%s，\n今天晚上：%s" % (today_list[1],today_list[3])
        # print(today_info)
        the_next_4=weather[2].get_text()
        next_list=the_next_4.split('\n\n\n\n\n')
        content=[]
        for i in next_list:
            line=i.replace('\n'," ")
            content.append(line)
        return (today_info,content)
        # print(the_next_4)
    def list_process(self,*args):
        weather_line=Query.get_page(self)
        for each_message in weather_line:
            if isinstance(each_message,str):
                print(each_message)
            else:
                for msg in each_message:
                    print(msg)

def main():
    qu=Query()
    qu.list_process()
if __name__=='__main__':
    main()