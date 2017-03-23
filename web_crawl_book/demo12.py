#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

import smtplib
import time
import lxml
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen


def send_mail(subject,body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "lzy575563079@sina.com"
    msg['To'] = "575563079@qq.com"

    server = smtplib.SMTP('smtp.sina.com')
    server.login(user="lzy575563079@sina.com",password="xxxxxxxx")
    server.send_message(msg)
    server.quit()

def is_day_right():
    # html = urlopen("https://isitchristmas.com/")
    html = urlopen("http://wannianrili.51240.com/")

    bsj = BeautifulSoup(html,"lxml")
    # print(bsj)
    is_dates = bsj.find_all("span",{"class":"wnrl_td_bzl wnrl_td_bzl_hong"})
    #is_dates 是一个结果的合集
    for i in is_dates:
        if i.get_text() == "春节":
            send_mail("春节","春节快到了")

    # yes_day = bsj.find("a",{"id":"answer"}).attrs['title']
    # while(yes_day == "NO"):
    #     print("还没有到圣诞")
    #     time.sleep(3600)
    #     is_day_right()



if __name__ == "__main__":
    is_day_right()
    # send_mail("圣诞节","现在是圣诞节")
