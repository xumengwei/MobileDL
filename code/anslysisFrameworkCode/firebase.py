import numpy as np
import os 
import sys
import json
sys.path.append("..")
from extract_zip import extract_file, get_zips
from basic_func import iterate_dir, get_pkg_list,run_cmd
DECOMPOSED_APK_PATH = "/data/mwx/decomposed_apks/"
if len(sys.argv)!=2:
    print("python firebase.py outpath")
    exit(0)
out_path = sys.argv[1]

res_filebase = {}
catorys = os.listdir(DECOMPOSED_APK_PATH)
for cat in catorys:
    decom_path = DECOMPOSED_APK_PATH+cat
    if os.path.isdir(decom_path):
        for apk in os.listdir(decom_path):
            if os.path.isdir(os.path.join(decom_path,apk)):
                for subdir, dirs, files in os.walk(os.path.join(decom_path,apk)):
                    for fileitem in files:
                        # ["libFirebaseCppAnalytics.so","libFirebaseCppAnalytics"]
                        if fileitem=="libFirebaseCppAnalytics.so" or "libFirebaseCppAnalytics" in fileitem:
                            filepath = os.path.join(subdir, fileitem)
                            if res_filebase.get(apk):
                                res_filebase[apk].append(filepath)
                            else:
                                res_filebase[apk] = [filepath]
                            print(filepath)

print(res_filebase)
with open(os.path.join(out_path,"filebase_use.json"),'w') as fp:
    json.dump(res_filebase,fp=fp)
