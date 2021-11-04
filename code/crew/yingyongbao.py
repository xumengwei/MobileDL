import requests
import parsel
import pandas as pd 
import os
import json

base_path = '/data/mwx/yingyongbao/apps'
def download(url,cat_path, title):
    out_path =  os.path.join(cat_path,title + '.apk')
    if os.path.exists(out_path):
        return
    print(out_path)
    response = requests.get(url=url, headers=headers)
    with open(out_path, mode='wb') as f:
        f.write(response.content)

# apks_info = []
for page in range(100, 123):
    pagesize=20
    begin=0
    cat_infos = []
    if os.path.exists(str(page)+".json"):
        with open(str(page)+".json") as fp:
            cat_infos = json.load(fp)
    while True:
         
        url = 'https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId={}&pageSize={}&pageContext={}'.format(page,pagesize,begin)
        # https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=110&pageSize=20&pageContext=110
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41'
        }
        
        response = requests.get(url=url, headers=headers).json()
        begin+=response["count"]
        print(url)
        objcontents = response["obj"]
        cat_infos=cat_infos+objcontents
        for i in range(len(objcontents)):
            cat_path = os.path.join(base_path,objcontents[i]["categoryName"])
            if not os.path.exists(cat_path):
                os.makedirs(cat_path)
            download(objcontents[i]["apkUrl"], cat_path, objcontents[i]["pkgName"])
        if response["count"]==0:
            break
        # print(response.json())
        # exit(0)
    with open(str(page)+".json",'w') as fp:
        json.dump(cat_infos,fp)
    # selector = parsel.Selector(response.text)
    # catory = selector.css('.menu-junior #cate-'+str(page)+' a::text').get()
    # if not catory:
    #     continue
    # cat_path = os.path.join(base_path,catory)
    # if not os.path.exists(cat_path):
    #     os.mkdir(cat_path)

    # lis = selector.css('.main ul li')
    # for li in lis:
    #     title = li.css('.app-info-desc a:nth-child(1)::text').get()
    #     app_detail_url = li.css('.app-info-desc a:nth-child(1)::attr(href)').get()
    #     # print(app_detail_url)
    #     app_size = li.css('.app-info-desc span:nth-child(2)::text').get().strip()
    #     # print(app_size)
    #     download_times = li.css('.app-info-desc span:nth-child(3)::text').get().strip()
    #     # print(download_times)
    #     apk_url = li.css('.app-info-desc a:nth-child(4)::attr(ex_url)').get()
    #     apk_id = li.css('.app-info-desc a:nth-child(4)::attr(apk)').get()
    #     # print(apk_url)
    #     print(apk_id)
    #     download(apk_url, cat_path, apk_id)
    #     # exit(0)
    #     apks_info.append([title,app_detail_url,app_size,download_times,apk_url,apk_id,catory])
        # break
    # break

# apks_info = pd.DataFrame(apks_info)

# apks_info.to_csv("yingyongbao_apks_info.csv")
