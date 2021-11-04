import os 
import config
from basic_func import iterate_dir, get_pkg_list,run_cmd

config.RAW_APK_PATH="/data/mobileDL/raw_apks/"
config.DECOMPOSED_APK_PATH="/data/mobileDL/decompose_apps/"
config.SECTION_DATA_PATH="/data/mobileDL/section_data/"  # .rodata files

def deleteApksDecomposed():
    catorys = os.listdir(config.DECOMPOSED_APK_PATH)

    for cat in catorys:
        catDir = os.path.join(config.DECOMPOSED_APK_PATH,cat)
        lists = os.listdir(catDir)
        for item in lists:
            apkpath = os.path.join(os.path.join(config.RAW_APK_PATH,cat),item)
            
            if not os.path.exists(apkpath):
                # tar
                pass
            elif len(os.listdir(os.path.join(catDir,item)))<3:
                print("not have  : ",len(get_pkg_list(apkpath)))
            else:
                print("has : ",len(get_pkg_list(apkpath)))


deleteApksDecomposed()
