import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime,timedelta
import time

has_download = set()
out_path = "/data/mwx/apks_before/apks"
base_url = "https://apk-dl.com"
url = "/files/5a8957d3cc74f866bc20f67b"

def download(url,out_path):
    target_url = base_url+url
    # print(target_url)
    html = requests.get(target_url).text
    parse = BeautifulSoup(html)
    download_href = parse.find("a",attrs={"rel":"nofollow"}).attrs["href"]
    # print(download_href)
    r = requests.get(download_href+"&dl=2")
    open(out_path, 'wb').write(r.content)

# download(url)

_path = "/data/mwx/apks_before/apks_lists"
_apk_path = "/data/mwx/apks_before/raw_apks"
base_timestramp=time.mktime(time.strptime("2020-12-31", "%Y-%m-%d"))

for p in os.listdir(_path):
    path_cat = os.path.join(_path,p)
    print(path_cat)
    with open(path_cat,'r',encoding='UTF-8') as fp:
        content = json.loads(fp.read())
        # print(content)
        # i = 0
        for key in content:
            is_download = False
            for i in range(len(content[key]["date"])):
                date_time = time.mktime(time.strptime(content[key]["date"][i], "%Y_%m_%d"))
                if date_time<base_timestramp:
                    if content[key]["url"][i][:4]=="http":
                        print("[http] "+key)
                        is_download = True
                    else:
                        out_path = os.path.join(_apk_path,p.split('.')[0])
                        if not os.path.exists(out_path):
                            os.makedirs(out_path)
                        download(content[key]["url"][i],os.path.join(out_path,key+".apk"))
                        print("[download] "+key)
                        is_download = True
                    break

            if not is_download:
                print("[has not] "+key+" "+content[key]["date"][-1])
            
            # exit(0)