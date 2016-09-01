#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang


"""
该模块为网页请求异常处理模块
"""
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError
req=Request(someurl)
try:
    response=urlopen(req)
except HTTPError as e:
    print('the server can\'t fulfill the request')
    print('Error code',e.code)
except URLError as e:
    print('we failed to reach a server')
    print('Reason',e.reason)
else:
    pass
# some code
