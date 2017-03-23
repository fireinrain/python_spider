#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

# 使用python发送邮件

import smtplib
from email.mime.text import MIMEText

msg = MIMEText("hello，this is from python")

msg['Subject'] = "这是标题"
msg['From'] = "lzy575563079@sina.com"
msg['To'] = "575563079@qq.com"

s = smtplib.SMTP("smtp.sina.com")
s.login(user="lzy575563079@sina.com",password="xxxxxxx")
s.send_message(msg)

print("发送成功")
s.quit()