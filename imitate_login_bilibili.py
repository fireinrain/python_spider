#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

"""
模拟登陆bilibili，应为前端对密码加密了所以
使用了密码明文
"""

import re
import requests
import http.cookiejar
from PIL import Image
import time
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}
filename = 'cookie'

# 建立一个会话，可以把同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
session = requests.Session()
# 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
# 而MozillaCookieJar类是存为'/.txt'格式的文件
session.cookies = http.cookiejar.LWPCookieJar(filename)
# 若本地有cookie则不用再post数据了
try:
    # 参数ignore_discard=True表示即使cookies将被丢弃也把它保存下来
    # 它还有另外一个参数igonre_expires表示当前数据覆盖（overwritten）原文件
    session.cookies.load(filename=filename, ignore_discard=True)
except:
    print('Cookie未加载！')



def get_captcha():
    """
    获取验证码本地显示
    返回你输入的验证码
    """
    # t = str(int(time.time() * 1000))
    captcha_url = 'https://passport.bilibili.com/captcha'
    response = session.get(captcha_url, headers=headers)
    with open('cptcha.gif', 'wb') as f:
        f.write(response.content)
    # Pillow显示验证码
    im = Image.open('cptcha.gif')
    im.show()
    # 提交表单是小写
    captcha = input('本次登录需要输入验证码： ').lower()
    return captcha


def login(username, password):
    """
    输入自己的账号密码，模拟登录bilibili
    """
    # 检测到11位数字则是手机登录
    if re.match(r'\d{11}$', account):
        print('使用手机登录中...')
        url = 'https://passport.bilibili.com/login'
        data = {'gourl':'http://www.bilibili.com/',
                'keeptime':259200,
                'pwd':password,
                'userid':account,
                'vdcode' : get_captcha(),
                # 验证码
                }
    else:
        print('使用邮箱登录中...')
        url = 'https://passport.bilibili.com/login'
        data = {'gourl': 'http://www.bilibili.com/',
                'keeptime': 259200,
                'pwd': password,
                'userid': account,
                'vdcode': get_captcha(),

                }
    # 若不用验证码，直接登录
    try:
        result = session.post(url, data=data, headers=headers)
        # print((result.text))
    # 要用验证码，post后登录
    except:
        data['vdcode'] = get_captcha()
        result = session.post(url, data=data, headers=headers)
        # print((result.text))
    # 保存cookie到本地
    session.cookies.save(ignore_discard=True, ignore_expires=True)


if __name__ == '__main__':
    account = input('输入账号：')
    secret = 730089615
    login(account, secret)
    # 设置里面的简介页面，登录后才能查看。以此来验证确实登录成功
    get_url = 'http://www.bilibili.com/account/dynamic'
    # allow_redirects=False 禁止重定向
    resp = session.get(get_url, headers=headers, allow_redirects=False)
    print(resp.text)

    # gourl='http://www.bilibili.com/'
    # keeptime=259200
    # pwd="Jq7VWWK+oPKRcmLWI2luu4R9L46KhteSm2I9Z1qYwFLyb3e1ES76XTypsl335vwxD8IKiJf3Hx0Ublfm9hHIVAH345PsKH/rXIKyTxaljCF2sT8ETBwmCfP0mOxe7vel+bFNxCWXMSixyklviqu4MM8CmCHwjuQ35M8WcJzePkw="
    # userid='575563079@qq.com'
    # vdcode='yd3mc'#验证码
