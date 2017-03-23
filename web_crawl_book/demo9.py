#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

import pymysql

# 获取链接
conn = pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='mysql',charset='utf8')
# 获取游标
cur = conn.cursor()
# 执行命令
query_str = "use scraping"
cur.execute(query_str)

# 执行查找
cur.execute("select * from pages")
# 获取结果
result_set = cur.fetchall()
for i in result_set:
    for j in i:
        print(str(j))
cur.close()
conn.close()