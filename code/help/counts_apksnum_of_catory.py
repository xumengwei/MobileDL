import numpy as np
import os

path = "/data/mwx/decomposed_apks"
pathapks = "/data/mwx/apks_data"

def getWholeCount(path):
    count = []
    catories = os.listdir(path)

    for catory in catories:
        pathcat = os.path.join(path,catory)
        count.append(len(os.listdir(pathcat)))
        print("|"+catory+"|"+str(len(os.listdir(pathcat)))+"|"+ str(len(os.listdir(os.path.join(pathapks,catory)))) +"|")
    return count
c = getWholeCount(path)

print(np.sum(np.array(c)))
