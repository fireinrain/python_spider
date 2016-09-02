#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang

"""
required:
requests
bs4
time
os

脚本尝试爬取url：https://www.javbus2.com/
尝试做一个查询脚本，并自动将获取的信息保存下来
功能描述
1.输入女优名字可以进行查询，如果错误将返回没有查到
2.输入番号，可以进行番号查询，查询结果，包括该女优的信息，作品信息
3.选着作品会将对应的磁力链接下载下来，对应会创建一个用于保存的文件夹
4.第一步查询到的结果，包含女优的详细信息，和所有的作品信息


"""
