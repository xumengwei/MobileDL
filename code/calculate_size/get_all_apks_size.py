import os 
import sys
import json
def get_FileSize(filePath):
 
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
 
    return round(fsize, 2)

in_dir = sys.argv[1]

size_dict = {}
cats = os.listdir(in_dir)
for cat in cats:
    print (cat)
    cat_path = os.path.join(in_dir, cat)
    apks = os.listdir(cat_path)
    # print(apks)
    for apk in apks:
        sizea = get_FileSize(os.path.join(cat_path,apk))
        size_dict[apk[:-4]] = sizea


with open("../result/apk_size/apks_size.json", "w") as dump_f:
        json.dump(size_dict, dump_f)
