import json
import sys
import shutil
import os

white_lists = {}
DECOMPOSED_APK_PATH=sys.argv[1] 

with open("./var/white_lists.json", "r") as fp:
	global white_lists
	white_lists =  json.loads(fp.read())

cats = os.listdir(DECOMPOSED_APK_PATH)
for cat in cats:
    cat_path = os.path.join(DECOMPOSED_APK_PATH, cat)
    apks = os.listdir(cat_path)
    for apk in apks:
        in_f = os.path.join(cat_path, apk)
        if white_lists.has_key(apk+".apk") and white_lists[apk+".apk"]==True:
            print("repeat "+apk)
            if os.path.exists(in_f):
                shutil.rmtree(in_f)
        elif white_lists.has_key(apk+".apk"):
             white_lists[apk+".apk"]=True

with open("./white_lists_state.json", "w") as dump_f:
    json.dump(white_lists, dump_f)
