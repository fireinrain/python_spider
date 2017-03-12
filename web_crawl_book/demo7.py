#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

# 导入相关的包
import csv

csv_file = open("test.csv","w+")

try:
    file = csv.writer(csv_file)
    file.writerow(("xiaoqian","xiaomei","mayuyu"))

    file.writerow((i for i in range(10)if i%2==0))
except EOFError as e:
    pass
finally:
    csv_file.close()