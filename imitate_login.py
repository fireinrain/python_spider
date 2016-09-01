#! /usr/bin/python3
# encoding=utf-8
# Written by liuzhaoyang

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# '''
# Required
# - requests (必须)
# - pillow (可选)
# Info
# - author : "xchaoinfo"
# - email  : "xchaoinfo@qq.com"
# - date   : "2016.2.4"
# Update
# - name   : "wangmengcn"
# - email  : "eclipse_sv@163.com"
# - date   : "2016.4.21"
# '''
# import requests
# try:
#     import cookielib
# except:
#     import http.cookiejar as cookielib
# import re
# import time
# import os.path
# try:
#     from PIL import Image
# except:
#     pass
#
#
# # 构造 Request headers
# agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
# headers = {
#     "Host": "www.zhihu.com",
#     "Referer": "https://www.zhihu.com/",
#     'User-Agent': agent
# }
#
# # 使用登录cookie信息
# session = requests.session()
# session.cookies = cookielib.LWPCookieJar(filename='cookies')
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("Cookie 未能加载")
#
#
# def get_xsrf():
#     '''_xsrf 是一个动态变化的参数'''
#     index_url = 'http://www.zhihu.com'
#     # 获取登录时需要用到的_xsrf
#     index_page = session.get(index_url, headers=headers)
#     html = index_page.text
#     pattern = r'name="_xsrf" value="(.*?)"'
#     # 这里的_xsrf 返回的是一个list
#     _xsrf = re.findall(pattern, html)
#     return _xsrf[0]
#
#
# # 获取验证码
# def get_captcha():
#     t = str(int(time.time() * 1000))
#     captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
#     r = session.get(captcha_url, headers=headers)
#     with open('captcha.jpg', 'wb') as f:
#         f.write(r.content)
#         f.close()
#     # 用pillow 的 Image 显示验证码
#     # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
#     try:
#         im = Image.open('captcha.jpg')
#         im.show()
#         im.close()
#     except:
#         print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
#     captcha = input("please input the captcha\n>")
#     return captcha
#
#
# def isLogin():
#     # 通过查看用户个人信息来判断是否已经登录
#     url = "https://www.zhihu.com/settings/profile"
#     login_code = session.get(url, headers=headers, allow_redirects=False).status_code
#     if login_code == 200:
#         return True
#     else:
#         return False
#
#
# def login(secret, account):
#     # 通过输入的用户名判断是否是手机号
#     if re.match(r"^1\d{10}$", account):
#         print("手机号登录 \n")
#         post_url = 'http://www.zhihu.com/login/phone_num'
#         postdata = {
#             '_xsrf': get_xsrf(),
#             'password': secret,
#             'remember_me': 'true',
#             'phone_num': account,
#         }
#     else:
#         if "@" in account:
#             print("邮箱登录 \n")
#         else:
#             print("你的账号输入有问题，请重新登录")
#             return 0
#         post_url = 'http://www.zhihu.com/login/email'
#         postdata = {
#             '_xsrf': get_xsrf(),
#             'password': secret,
#             'remember_me': 'true',
#             'email': account,
#         }
#     try:
#         # 不需要验证码直接登录成功
#         login_page = session.post(post_url, data=postdata, headers=headers)
#         login_code = login_page.text
#         print(login_page.status_code)
#         print(login_code)
#     except:
#         # 需要输入验证码后才能登录成功
#         postdata["captcha"] = get_captcha()
#         login_page = session.post(post_url, data=postdata, headers=headers)
#         login_code = eval(login_page.text)
#         print(login_code['msg'])
#     session.cookies.save()
#
# try:
#     input = raw_input
# except:
#     pass
#
#
# if __name__ == '__main__':
#     if isLogin():
#         print('您已经登录')
#     else:
#         account = input('请输入你的用户名\n>  ')
#         secret = input("请输入你的密码\n>  ")
#         login(secret, account)

"""
修改上面的代码
"""



import re
from urllib import parse, request, error
import http.cookiejar
from PIL import Image
import time
import json

email_url = 'https://www.zhihu.com/login/email'
phone_url = 'http://www.zhihu.com/login/phone_num'
headers = ['User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0']
filename = 'cookie'
# 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
# 而MozillaCookieJar类是存为'/.txt'格式的文件
cookie = http.cookiejar.LWPCookieJar(filename)
# 若本地有cookie则不用再post数据了
try:
    cookie.load(filename=filename, ignore_discard=True)
except:
    print('Cookie未加载！')

opener = request.build_opener(request.HTTPCookieProcessor(cookie))
# 给openner添加headers, addheaders方法接受元组而非字典
opener.addheaders = headers


def get_xsrf():
    """
    获取参数_xsrf
    """
    req = opener.open('https://www.zhihu.com')
    html = req.read().decode('utf-8')
    get_xsrf_pattern = re.compile(r'<input type="hidden" name="_xsrf" value="(.*?)"')
    _xsrf = re.findall(get_xsrf_pattern, html)[0]
    return _xsrf


def get_captcha():
    """
    获取验证码本地显示
    返回你输入的验证码
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    request.urlretrieve(captcha_url, 'cptcha.gif')
    # image_data = request.urlopen(captcha_url).read()
    # with open('cptcha.gif', 'wb') as f:
    #     f.write(image_data)
    im = Image.open('cptcha.gif')
    im.show()
    captcha = input('本次登录需要输入验证码： ')
    return captcha


def login(username, password):
    """
    输入自己的账号密码，模拟登录知乎
    """
    # 检测到11位数字则是手机登录
    if re.match(r'\d{11}$', account):
        print('使用手机登录中...')
        url = phone_url
        data = {'_xsrf': get_xsrf(),
                'password': password,
                'remember_me': 'true',
                'phone_num': username
                }
    else:
        print('使用邮箱登录中...')
        url = email_url
        data = {'_xsrf': get_xsrf(),
                'password': password,
                'remember_me': 'true',
                'email': username
                }
    # 若不用验证码，直接登录
    try:
        post_data = parse.urlencode(data).encode('utf-8')
        r = opener.open(url, post_data)
        result = r.read().decode('utf-8')
        # 打印返回的响应，r = 1代表响应失败，msg里是失败的原因
        print((json.loads(result))['msg'])
        # 打印_xsrf验证确实获取到
        # print(get_xsrf())
    # 要用验证码，post后登录
    except:
        data['captcha'] = get_captcha()
        post_data = parse.urlencode(data).encode('utf-8')
        r = opener.open(url, post_data)
        result = r.read().decode('utf-8')
        print((json.loads(result))['msg'])
        # print(get_xsrf)
    # 保存cookie到本地
    cookie.save(ignore_discard=True, ignore_expires=True)


if __name__ == '__main__':
    account = input('输入账号：')
    secret = input('输入密码：')
    login(account, secret)

    # 设置里面的简介页面，登录后才能查看。以此来验证确实登录成功
    get_url = 'https://www.zhihu.com/settings/profile'
    try:
        get = opener.open(get_url)
        content = get.read().decode('utf-8')
        print(content)
    except error.HTTPError as e:
        print(e.reason)
    except error.URLError as e:
        print(e.reason)



