#! /usr/bin/python3
# _encoding:utf-8_
# Written by liuzhaoyang
# wcontact:liu575563079@gmail.com

import csv
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsobj = BeautifulSoup(html,"lxml")

# 获得表格
table = bsobj.findAll("table",{"class":"wikitable"})[0]
rows = table.findAll("tr")

csv_file = open("editor.csv","w",newline='',encoding="utf-8")
write = csv.writer(csv_file)
try:
    for row in rows:
        csv_row = []
        for cell in row.findAll(['td','tr']):
            csv_row.append(cell.get_text())
            write.writerow(csv_row)
finally:
    csv_file.close()