import os 
import config
from basic_func import iterate_dir
import json
# use suffix to detect DL models: this approach may have false negative
def find_model_via_suffix(pkg_list, suffix_list, dl_lib):
    def filter(path):
        for su in suffix_list:
            if path.endswith(su):
                pathSplited = path.split('.')
                # bin file not find from style
                if '/style/' in path and dl_lib=='ncnn' and len(pathSplited)>1 and path.split('.')[-1]=='bin':
                    continue
                # textures
                if 'textures' in path and dl_lib=='dlib':
                    continue
                return True
        return False
    ret = {}
    for pkg in pkg_list:
        decomposed_pkg_path = os.path.join(config.DECOMPOSED_APK_PATH, pkg)
        models = iterate_dir(decomposed_pkg_path, filter)
        if len(models)>0:
            ret[pkg] = models
    # print (ret)
    DL_MODELS[dl_lib] = ret

config.SECTION_DATA_PATH="/data/mwx/section_data/"
config.DECOMPOSED_APK_PATH = "/data/mwx/decomposed_apks/"
catorys = os.listdir(config.DECOMPOSED_APK_PATH)
DL_MODELS = {}
for cat in catorys:
    # config.RAW_APK_PATH = "/data/mobileDL/raw_apks/"+cat
    print (cat)
    DL_MODELS = {}
    config.DECOMPOSED_APK_PATH="/data/mwx/decomposed_apks/"+cat
    config.SECTION_DATA_PATH="/data/mwx/section_data/" +cat
    # print(config.RAW_APK_PATH)
    for k in config.magic_str_all.keys():
        print("==============="+k+"================")
        DLname = k
        find_model_via_suffix(os.listdir(os.path.join(config.DECOMPOSED_APK_PATH)), config.suffix_list_all[DLname], DLname)
        
    with open("./output/05_15/DL_MODELS_half"+ cat + ".json", "w") as dump_f:
        json.dump(DL_MODELS, dump_f)

