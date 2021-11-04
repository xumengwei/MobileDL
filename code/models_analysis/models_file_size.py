'''
   获取tflite模型文件的大小，
   此出认定只有interpreter解析成功的才能被认定为合法的tflite文件
'''
import pandas as pd
import numpy as np
import json
import os
import sys
sys.path.append("..")

model_type = sys.argv[1]
def get_FileSize(filePath):

    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)

    return round(fsize, 2)
json_file_path = "model_files_info/"+model_type+".json"
if not os.path.exists(json_file_path):
    # interpreter_tflite_models.py
    print("=====please check every tfl model file is right model fiel of not====")
    print("python3 interpreter_tflite_models.py")
    exit(0)

with open(json_file_path) as fp:
    contents = json.load(fp)

sizes = []
for key in contents:
    if contents[key]["interpreter"]=="sucess":
        _size = get_FileSize(key)
        sizes.append(_size)
np.save("model_files_info/"+model_type+"_size",np.array(sizes))
