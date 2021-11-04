import json
import os
import urllib
import requests
with open("./res_parser.json") as fp:
    contents = json.load(fp)

_output = "/data/mwx/yingyongbao/apps"

for key in contents:
    url = contents[key][1]
    output_path = os.path.join(_output,contents[key][0])
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_path = os.path.join(output_path,key+".apk")

    if os.path.exists(output_path):
        continue
    print(output_path)
    r = requests.get(url)
    open(output_path,"wb").write(r.content)
    # exit(0)

