#! /usr/bin/python3
# _*_encoding:utf-8_*_
# Written by liuzhaoyang

# """
# 实现下载bing每日壁纸，没有实现多线程下载
#存在的bug是爬取链接有的需要加载Google的东西所以
# 请求链接中断出现404
#可以下载7月和8月的
# """
# 导入相应的模块
import  urllib.request
from bs4 import BeautifulSoup
import os
from time import sleep


#入口url生成函数
def down_url():
    month=input('请输入月份(05)：')
    day=([i for i in range(1,31)])
    url_list=[]
    for i in day:
        if i <=9:
            i='0'+str(i)
        else:
            i=str(i)
        url='http://bingwallpaper.com/CN/'+str(2016)+month+i+'.html'
        url_list.append(url)
    return  url_list
# print([i[-13:-5] for i in url_list])

# 图片url生成并下载
def down_load(pic_url):
    # 添加浏览器头标识，防止被屏蔽
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    head={'User-Agent':user_agent}
    # 从传入的url截取图片日期
    pic_time=pic_url[-13:-5]
    # 创建请求对象，并添加头标识
    req = urllib.request.Request(pic_url, headers=head)
    # 打开url
    response = urllib.request.urlopen(req,timeout=5)
    # 获取内容，bytes
    sc = response.read()
    # 创建bs4对象
    soup = BeautifulSoup(sc,'lxml')
    # 找出所有的img标签
    image = soup.select('img')
    # 获取图片url地址
    image_url = image[1].get('src')[2:]
    down_pic_res=urllib.request.Request('http://'+image_url, headers=head)
    res = urllib.request.urlopen(down_pic_res).read()
    # 保存文件
    with open(pic_time+'.jpg','wb') as file:
        file.write(res)
        print('下载'+pic_time+'.jpg'+'成功')
if __name__=='__main__':
    # 创建文件夹
    os.makedirs('Bing', exist_ok=True)
    # 切换到创建的工作文件夹
    os.chdir('Bing')
    url_list=down_url()
    print(url_list)
    #循环下载
    for pic_url in url_list:
        down_load(pic_url)
        sleep(2)



