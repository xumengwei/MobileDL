import pandas as pd
import numpy as np
import json
import os
import sys
sys.path.append("..")
import config

def get_FileSize(filePath):

    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)

    return round(fsize, 2)

with open("../result/apk_size/merge_apks_models.json") as fp:
    all_models = json.load(fp)
# config.suffix_list_all
model_size_all_apks = {}
for dl in all_models:
    suffix_dl = config.suffix_list_all[dl]
    one_dl_suffix_size = [[] for i in range(len(suffix_dl))]
    model_size_one_dl =dict(zip(suffix_dl,one_dl_suffix_size))
    for apk in all_models[dl]:
        for model in all_models[dl][apk]:
            # print(model)
            model_size = get_FileSize(model)
            for suffix in suffix_dl:
                
                if model.endswith(suffix):
                    model_size_one_dl[str(suffix)].append(model_size)
                    break
    model_size_all_apks[str(dl)] = model_size_one_dl
print (model_size_all_apks)
with open("../result/apk_size/model_size_of_all_dl.json","w") as fp:
    json.dump(fp,model_size_all_apks)

