import requests
from bs4 import BeautifulSoup
import os
import json

base_url = "https://apk-dl.com/"
search_url = base_url+"search?q="
# appname = "bigvu.com.reporter"
lists_path = "..\others\lists"
out_path = "..\others\lists_before"
# res = {}
def download_condition_apk(apkname):
    html = requests.get(search_url+apkname).text
    # print(html)
    parse = BeautifulSoup(html)
    lists = parse.find("ul",class_="apks dlist")
    lists = lists.find_all("li")
    version_date = []
    for item in lists:
        version_date.append(item.attrs["data-versioncode"])
    # print(version_date)

    version_apks = parse.find_all("div",class_="download")
    version_url = []
    for item in version_apks:
        version_url.append(item.find("a").attrs["href"])
    # print(version_url)
    return version_date,version_url
    # res[apkname]["date"]=version_date
    # res[apkname]["url"]=version_url
if __name__ == '__main__':
    white_list = ["GAME_WORD.json","ANDROID_WEAR.json"]
    lists=[]
    for co_list in os.listdir(lists_path):
        co_list_path = os.path.join(lists_path,co_list)
        co_list_out_path = os.path.join(out_path,co_list)

        lists.append([co_list_path,co_list_out_path])

    for p in os.listdir(lists[0][0]):
        if os.path.exists(os.path.join(out_path,p)):
            continue
        elif p in white_list:
            continue
        res = {}
        for j in range(len(lists)):
            with open(os.path.join(lists[j][0],p),'r',encoding='UTF-8') as fp:
                content = json.loads(fp.read())
                lencontent = len(content)
                i = 0
                while i<lencontent:
                    appid = content[i]["appId"]

                    # print(res)
                    if not res.get(appid):
                        try:
                            version_date,version_url = download_condition_apk(appid)
                            res[appid]={}
                            res[appid]["date"]=version_date
                            res[appid]["url"]=version_url
                        except:
                            print("[error]"+appid)
                            pass
                    i+=1
                    # break
        with open(os.path.join(out_path,p),'w') as fp:
            json.dump(res,fp)
        # break

