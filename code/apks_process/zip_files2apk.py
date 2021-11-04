import os
import sys
sys.path.append("..")
from basic_func import run_cmd

in_dir = sys.argv[1]
out_dir = sys.argv[2]
cats = os.listdir(in_dir)
for cat in cats:
    print (cat)
    cat_path = os.path.join(in_dir, cat)
    apks = os.listdir(cat_path)
    if not os.path.exists(os.path.join(out_dir,cat)):
        os.makedirs(os.path.join(out_dir,cat))
    for apk in apks:
        if os.path.exists(os.path.join(os.path.join(out_dir,cat),apk +".apk")):
            continue
        
        os.chdir(os.path.join(cat_path,apk))
        if not os.listdir("./"):
            continue
        print(os.path.join(cat_path,apk))
        cmd = "zip -r "+os.path.join(os.path.join(out_dir,cat),apk +".zip")+ " ./*"
        print(cmd)
        run_cmd(cmd)
        os.rename(os.path.join(os.path.join(out_dir,cat),apk +".zip"),os.path.join(os.path.join(out_dir,cat),apk +".apk"))
        # exit(0)