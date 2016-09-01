
# 导入相应的解析库
import urllib.parse
import urllib.request
import json
import time

while True:
    content=input("请输入要翻译的内容(q退出)：")
    if content=='q':
        break
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.google.co.jp/'
    # 添加头标识
    head={}
    head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
    data={}
    data['type']='AUTO'
    data['i']=content
    data['doctype']='json'
    data['xmlVersion']='1.8'
    data['keyfrom']='fanyi.web'
    data['ue']='UTF-8'
    data['typoResult']='true'
    data['action']="FY_BY_CLICKBUTTON"

    # 将提交的表格内容进行相应的格式化处理
    data=urllib.parse.urlencode(data).encode('utf-8')
    #生成一个request对象
    req=urllib.request.Request(url,data,head)

    response=urllib.request.urlopen(req)

    html=response.read().decode('utf-8')

    target=json.loads(html)

    print(target['translateResult'][0][0]['tgt'])
    # 休息两秒
    time.sleep(2)

