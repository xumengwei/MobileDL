#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import urllib
import math
import json
import atexit
import time
import random
import os

@atexit.register
def exit_before():
    with open("./data/details.json",'w') as fp:
        json.dump(details, fp)

    with open("./data/res_parser.json", "w") as fp:
        json.dump(res_parser,fp)

    with open("./data/error_link.json", "w") as fp:
        json.dump(error_links,fp)

headers = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
           "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
           "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"
    ]

def parser_apks(count, details, res_parser):
    '''小米应用市场'''
    _root_url="http://app.mi.com" #应用市场主页网址
    page_num=1 #设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    if count==-1:
        count = 200000
    _num = 0
    while count:
        #获取排行榜页面的网页内容
        wbdata = requests.get("http://app.mi.com/topList?page="+str(page_num),headers={"User-Agent":headers[random.randint(0,len(headers)-1)]}).text

        print("开始爬取第"+str(page_num)+"页")
        #解析页面内容获取 应用下载的 界面连接
        soup=BeautifulSoup(wbdata,"html.parser")
        links=soup.body.find("ul",attrs={"class":"applist"}).find_all("a",href=re.compile("/details?"), class_ ="", alt="") #BeautifullSoup的具体用法请百度一下吧。。。
        print(len(links))
        if len(links)==0:
            return res_parser, details
        for link in links:
            detail_link=urllib.parse.urljoin(_root_url, str(link["href"]))
            # print(detail_link)
            package_name=detail_link.split("=")[1]
            _num+=1
            if res_parser.get(package_name):
                continue
            #在下载页面中获取 apk下载的地址
            time.sleep(1)
            download_page=requests.get(detail_link, headers={"User-Agent":headers[random.randint(0,len(headers)-1)]}).text
            soup1=BeautifulSoup(download_page,"html.parser")
            detail = {}

            if soup1 is None:
                print(detail_link)
                continue
            print(detail_link)
            print(soup1.text)
            while True:
                if soup1.text.strip()[:1]=="您":
                    print(soup1.text)
                    time.sleep(1)
                    download_page=requests.get(detail_link, headers={"User-Agent":headers[random.randint(0,len(headers)-1)]}).text
                    soup1=BeautifulSoup(download_page,"html.parser")
                else:
                    print("chneggong")
                    break
            # print(soup1.find(class_="intro-titles"))
            if soup1.find(class_="intro-titles") is None:
                continue
            detail["name"] = soup1.find(class_="intro-titles").contents[0].text
            catory = soup1.find(class_="intro-titles").contents[1].text.split("|")[0].split("：")[1]

            detail["type"]=catory
            detail["rate"] = _num

            score_times = soup1.find(class_="app-intro-comment").text
            score_times="".join(list(filter(str.isdigit, score_times)))
            detail["score_times"]=score_times
            info_left = soup1.find_all(class_="float-left")
            # print(detail)
            for i in range(len(info_left)):
                detail[info_left[i].contents[0].text]=info_left[i].contents[1].text
            info_right = soup1.find_all(class_="float-right")
            for i in range(2):
                detail[info_right[i].contents[0].text]=info_right[i].contents[1].text

            download_link=soup1.find(class_="download")["href"]
            download_url=urllib.parse.urljoin(_root_url, str(download_link))
            #解析后会有重复的结果，下面通过判断去重
            detail["appid"]=package_name
            detail["url"]=download_url
            detail["text"] = soup1.find(class_="pslide").text
            details[package_name]=detail
            if download_url not in res_parser.values():
                res_parser[package_name]=[catory,download_url]
                count=count-1
            if count==0:
                break
        if count >0:
            page_num=page_num+1
    print("爬取apk数量为: "+str(len(res_parser)))
    return res_parser,details

if __name__ == '__main__':
    global details
    details = {}
    global res_parser
    res_parser = {}

    global error_links
    error_links = {}
    if os.path.exists("./data/details.json"):

        with open("./data/details.json") as fp:
            details = json.load(fp)

        with open("./data/res_parser.json") as fp:
            res_parser = json.load(fp)
    res_parser, details = parser_apks(1, details, res_parser)
    print(details)

