# -*- coding = utf-8 -*-
# Created by Menelaus on 2020/10/4 11:07
# File: new crawler.py

import requests
import json
import re
import xlsxwriter
from bs4 import BeautifulSoup

print("RUNNING……")


headers = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://www.zhihu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


def extract_answer(s):
    temp_list = re.compile('<[^>]*>').sub("", s).replace("\n", "").replace(" ","")
    return temp_list


def getAnswers(qid):

    start_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=content&limit=20&offset=0&platform=desktop&sort_by=default".format(qid, 0)

    next_url = [start_url]
    count = 0

    #打开xlsx文件
    workbook = xlsxwriter.Workbook("知乎回答%s.xlsx" % qid)
    worksheet = workbook.add_worksheet()

    #爬取知乎问题号为qid的所有回答
    for url in next_url:
        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, "lxml")
        content = str(soup.p).split("<p>")[1].split("</p>")[0]
        c = json.loads(content)

        if "data" not in c:
            print("获取数据失败，本 ip 可能已被限制。")
            print(c)
            break

        answers = [extract_answer(item["content"]) for item in c["data"] if extract_answer(item["content"]) != ""]

        for answer in answers:
            count = count + 1
            worksheet.write("A%s"%count, count)
            worksheet.write("B%s"%count, answer)

        next_url.append(c["paging"]["next"])
        if c["paging"]["is_end"]:
            break

    #关闭xlsx文件
    workbook.close()


#导入问题号的txt
file = open("D:\Desktop\知乎爬虫\qid.txt")
#写入txt文件的路径
for line in file:
    curline=line.strip().split(" ")
    getAnswers(int(curline[0]))
    #得到最终爬虫数据


print("END")
print("Please check your file QAQ")
