import numpy as np
import os
import pandas as pd 

path = "/data/mwx/decomposed_apks"

def getDecomLists(path):
    catories = os.listdir(path)
    arr = []
    for catory in catories:
        pathcat = os.path.join(path,catory)
        apps = os.listdir(pathcat)
        for app in apps:
            arr.append([app,catory])
    return arr
arr = getDecomLists(path)
arr = pd.DataFrame(arr)
arr.to_csv("output/decomposed_apks_0523_before.csv")