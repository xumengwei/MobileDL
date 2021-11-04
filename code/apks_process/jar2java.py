import os
import sys
JAR_PATH = sys.argv[1]
sys.path.append("..")
from basic_func import run_cmd

WHILE_LIST=[]
for cat in os.listdir(JAR_PATH):
    if cat in WHILE_LIST:
        continue
    catpath=os.path.join(JAR_PATH, cat)
    for dir_path, dir_names, file_names in os.walk(catpath):
        for fileitem in file_names:
            if fileitem.endswith(".jar"):
                # print(dir_path,fileitem)
                filename = os.path.join(dir_path,fileitem)
                
                if not os.path.exists(filename[:-4]):
                    os.makedirs(filename[:-4])
                if os.listdir(filename[:-4]):
                    print(filename[:-4])
                    continue
                cmd_unzip = "unzip " + filename +" -d "+filename[:-4]
                run_cmd(cmd_unzip)
                print(cmd_unzip)
                # exit()