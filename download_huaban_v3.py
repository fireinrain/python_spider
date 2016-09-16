#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

#
#
# import re
# import os
# import requests
# from time import sleep,time
# from random import choice
# from multiprocessing.dummy import Pool as ThreadPool
#
# global photo_number
# global page_count
# page_count = 0
# photo_number = 0
#
#
# UserAgent = [
#     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
#     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
#     'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
#     'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
#     'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
#     'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
#     'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
#     'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
#     'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
#     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
#     'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
#     'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
# ]
#
# user_agent=choice(UserAgent)
# head = {'User-Agent': user_agent }
# TimeOut = 30
#
#
#
# def downfile(file, img_url):
#     print("开始下载：", file, img_url)
#     try:
#         resource = requests.get(img_url, stream=True,headers=head).content
#         with open(file, 'wb') as file:
#             file.write(resource)
#     except Exception as e:
#         print("下载失败了", e)
#
#
# def request_page_text(url):
#     try:
#         Page = requests.session().get(url, headers=head, timeout=TimeOut)
#         Page.encoding='utf-8'
#         return Page.text
#     except Exception as e:
#         print("请求失败了...重试中(5s)", e)
#         sleep(5)
#         print("暂停结束")
#         request_page_text(url)
#
#
# def request_url_download(url):
#     global page_count
#     page_count += 1
#     global photo_number
#     # print("请求网址：", url)
#     text = request_page_text(url)
#     pattern = re.compile('{"pin_id":(\d*?),.*?"key":"(.*?)",.*?"like_count":(\d*?),.*?"repin_count":(\d*?),.*?}', re.S)
#     # 参数re.S 是正则表达式，编译参数标识re.DOTALL，即.匹配除、\n 所有字符
#     img_query_items = re.findall(pattern, text)
#     # print(img_query_items)
#     max_pin_id = 0
#
#
#     for url_items in img_query_items:
#         max_pin_id = url_items[0]
#         x_key = url_items[1]
#         x_like_count = int(url_items[2])
#         x_repin_count = int(url_items[3])
#         if (x_repin_count > 10 and x_like_count > 10) or x_repin_count > 100 or x_like_count > 20:
#             print("开始下载第{0}张图片".format(photo_number))
#             url_item = url_image + x_key
#             filename = down_dir + str(max_pin_id) + ".jpg"
#             if os.path.isfile(filename):
#                 print("文件存在：", filename)
#                 continue
#             if photo_number >= image_numbers:
#                 # 结束函数
#                 return
#
#             downfile(filename, url_item)
#             photo_number += 1
#     sleep(1)
#     request_url_download(url_query+str(page_count))
#
#
#
#
# if __name__=='__main__':
#     url_image = 'http://hbimg.b0.upaiyun.com/'
#
#     query_string=input('请输入要查询的关键词：')
#     url = "http://huaban.com/search/?q="+query_string
#     global image_numbers
#     image_numbers=int(input('下载多少张：'))
#     down_dir = query_string
#
#     url_query = "http://huaban.com/search/?q="+query_string+"&per_page=20&wfl=1&page="
#
#     if not os.path.exists(down_dir):
#         os.makedirs(down_dir)
#         os.chdir(down_dir)
#     start_time=time()
#     request_url_download(url + str(page_count))
#     end_time=time()
#     print('共下载%s张素材，耗时%.2fs' %(image_numbers,end_time-start_time))


    # 爬取一个栏目的相关图片
# import requests
# import re
# import os
# import os.path
#
#
# class HuabanDownload():
#     """ 抓去花瓣网上的图片 """
#
#     def __init__(self,query,pattern):
#         """ 在当前文件夹下新建images文件夹存放抓取的图片 """
#         self.homeUrl = 'http://huaban.com/search/?q='+query+pattern
#         # self.homeUrl = "http://huaban.com/favorite/beauty/"
#         self.images = []
#         if not os.path.exists('./images'):
#             os.mkdir('./images')
#
#     def __load_homePage(self):
#         """ 加载主页面 """
#         return requests.get(url=self.homeUrl).text
#
#     def __make_ajax_url(self, No):
#         """ 返回ajax请求的url """
#         return self.homeUrl + "?i5p998kw&max=" + No + "&limit=20&wfl=1"
#
#     def __load_more(self, maxNo):
#         """ 刷新页面 """
#         return requests.get(url=self.__make_ajax_url(maxNo)).text
#
#     def __process_data(self, htmlPage):
#         """ 从html页面中提取图片的信息 """
#         prog = re.compile(r'app\.page\["pins"\].*')
#         appPins = prog.findall(htmlPage)
#         # 将js中的null定义为Python中的None
#         null = None
#         true = True
#         if appPins == []:
#             return None
#         result = eval(appPins[0][19:-1])
#         for i in result:
#             info = {}
#             info['id'] = str(i['pin_id'])
#             info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
#             if 'image' == i["file"]["type"][:5]:
#                 info['type'] = i["file"]["type"][6:]
#             else:
#                 info['type'] = 'NoName'
#             self.images.append(info)
#
#     def __save_image(self, imageName, content):
#         """ 保存图片 """
#         with open(imageName, 'wb') as fp:
#             fp.write(content)
#
#     def get_image_info(self, numbers):
#         """ 得到图片信息 """
#         self.__process_data(self.__load_homePage())
#         for i in range((numbers - 1) // numbers):
#             self.__process_data(self.__load_more(self.images[-1]['id']))
#         return self.images
#
#     def down_images(self):
#         """ 下载图片 """
#         print("{} image will be download".format(len(self.images)))
#         for key, image in enumerate(self.images):
#             print('download {0} ...'.format(key))
#             try:
#                 req = requests.get(image["url"])
#             except:
#                 print('error')
#             imageName = os.path.join("./images", image["id"] + "." + image["type"])
#             self.__save_image(imageName, req.content)
#
#
# if __name__ == '__main__':
#     query=input('请输入关键字：')
#     pattern=input('请选择搜索模式:(热门1)(综合2)(匹配度3)(时间4)')
#     numbers=int(input('下载张数：'))
#     if pattern==1:
#         pattern=''
#     elif pattern==2:
#         pattern='&sort=all'
#     elif pattern==3:
#         pattern='&sort=relative'
#     elif pattern==4:
#         pattern='&sort=created_at'
#     hc = HuabanDownload(query,pattern)
#     hc.get_image_info(100)
#     hc.down_images()



import requests
import re
import os
import os.path

class HuabanCrawler():
    """ 抓去花瓣网上的图片 """

    def __init__(self):
        """ 在当前文件夹下新建images文件夹存放抓取的图片 """
        self.homeUrl = "http://huaban.com/favorite/travel_places/"
        self.images = []
        if not os.path.exists('./images'):
            os.mkdir('./images')

    def __load_homePage(self):
        """ 加载主页面 """
        return requests.get(url = self.homeUrl).text

    def __make_ajax_url(self, No):
        """ 返回ajax请求的url """
        return self.homeUrl + "?i5p998kw&max=" + No + "&limit=20&wfl=1"

    def __load_more(self, maxNo):
        """ 刷新页面 """
        return requests.get(url = self.__make_ajax_url(maxNo)).text

    def __process_data(self, htmlPage):
        """ 从html页面中提取图片的信息 """
        prog = re.compile(r'app\.page\["pins"\].*')
        appPins = prog.findall(htmlPage)
        # 将js中的null定义为Python中的None
        null = None
        true = True
        if appPins == []:
            return None
        result = eval(appPins[0][19:-1])
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
            if 'image' == i["file"]["type"][:5]:
                info['type'] = i["file"]["type"][6:]
            else:
                info['type'] = 'NoName'
            self.images.append(info)

    def __save_image(self, imageName, content):
        """ 保存图片 """
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def get_image_info(self, num=20):
        """ 得到图片信息 """
        self.__process_data(self.__load_homePage())
        for i in range(int((num-1)/20)):
            self.__process_data(self.__load_more(self.images[-1]['id']))
        return self.images

    def down_images(self):
        """ 下载图片 """
        print ("{} image will be download".format(len(self.images)))
        for key, image in enumerate(self.images):
            print ('download {0} ...'.format(key))
            try:
                req = requests.get(image["url"])
            except :
                print('error')
            imageName = os.path.join("./images", image["id"] + "." + image["type"])
            self.__save_image(imageName, req.content)


if __name__ == '__main__':
    hc = HuabanCrawler()
    hc.get_image_info(20000)
    hc.down_images()


    ############################尝试登陆##############################
    # import re
    # import requests
    # import http.cookiejar
    # import time
    # import json
    #
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0',
    #            'Origin': 'http://huaban.com',
    #            "Referer": 'http://huaban.com/'}
    # filename = 'cookie'
    #
    # # 建立一个会话，可以把同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
    # session = requests.Session()
    # # 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
    # # 而MozillaCookieJar类是存为'/.txt'格式的文件
    # session.cookies = http.cookiejar.LWPCookieJar(filename)
    # # 若本地有cookie则不用再post数据了
    # try:
    #     # 参数ignore_discard=True表示即使cookies将被丢弃也把它保存下来
    #     # 它还有另外一个参数igonre_expires表示当前数据覆盖（overwritten）原文件
    #     session.cookies.load(filename=filename, ignore_discard=True)
    # except:
    #     print('Cookie未加载！')
    #
    #
    # def login(username, password):
    #     """
    #     输入自己的账号密码，模拟登录bilibili
    #     """
    #     # 检测到11位数字则是手机登录
    #     if re.match(r'\d{11}$', account):
    #         print('使用手机登录中...')
    #         url = 'https://huaban.com/auth/'
    #         data = {'_ref': 'frame',
    #                 'email': account,
    #                 'password': password,
    #
    #                 }
    #     else:
    #         print('使用邮箱登录中...')
    #         data = {'_ref': 'frame',
    #                 'email': account,
    #                 'password': password,
    #
    #                 }
    #     # 若不用验证码，直接登录
    #     try:
    #         result = session.post(url, data=data, headers=headers)
    #         # print((result.text))
    #     # 要用验证码，post后登录
    #     except:
    #         print('登入失败')
    #         result = session.post(url, data=data, headers=headers)
    #         # print((result.text))
    #     # 保存cookie到本地
    #     session.cookies.save(ignore_discard=True, ignore_expires=True)
    #
    #
    # if __name__ == '__main__':
    #     account = input('输入账号：')
    #     secret = input("输入密码：")
    #     login(account, secret)
    #     # 设置里面的简介页面，登录后才能查看。以此来验证确实登录成功
    #     get_url = 'http://huaban.com/'
    #     # allow_redirects=False 禁止重定向
    #     resp = session.get(get_url, headers=headers, allow_redirects=False)
    #     print(resp.text)