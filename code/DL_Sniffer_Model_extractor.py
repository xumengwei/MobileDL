# Detecting DL usage
# What apps are using DL?
# Where are their model files?
import os
import sys
import array
# import tensorflow as tf
import csv
# from tensorflow.python.platform import gfile
from extract_zip import extract_file, get_zips
from basic_func import iterate_dir, get_pkg_list,run_cmd
import json
import yaml
import config

import atexit

# @atexit.register
# def f():
#     print('process exit!')

#     with open("./DL_PKGS_half_error.json", "w") as dump_f:
#         json.dump(DL_PKGS, dump_f)
#     with open("./DL_MODELS_half_error", "w") as dump_f:
#         json.dump(DL_MODELS, dump_f)

DL_PKGS = {}
DL_MODELS = {}

#true = 1
#false = 0
FalseTrue = 2
ROOT_PATH = "/home/edodor/mbdir/MobileDL/data/"
#RES_PATH = "/home/edodor/mbdir/MobileDL/code/result/yingyongbao/"
#NEW_PATH="/home/edodor/mbdir/MobileDL/code/result/"
def iterate_rodata(pkg_list, detector, dl_lib, suffix_list,sec_path,magicStr):
    ret = {}
    for pkg in pkg_list:
        pkg_path = sec_path
        if not os.path.exists(pkg_path):
            continue
        for lib in os.listdir(pkg_path):
            if detector(os.path.join(pkg_path, lib),magicStr):
                print("this is lit",lib,"#", pkg)
                ret[pkg] = lib+"                 "+ pkg_path
                break
    DL_PKGS[dl_lib] = ret
    

# use suffix to detect DL models: this approach may have false negative
def find_model_via_suffix(pkg_list, suffix_list, dl_lib):
    def filter(path):
        print(path,  "    ht  " ,suffix_list)
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
        ret[pkg] = models
    
    DL_MODELS[dl_lib] = ret 
    
def straight_detector_rodata(lib_path,magic_str):
    with open(lib_path,encoding="utf8",errors='ignore') as f:
        
        lines= f.read()
        for stra in magic_str:
            if stra in lines:
                print("success yay", magic_str)
                return True
    return False

def extract_model(DLname):
    #print("******************************")
    # if not os.path.exists(config.RAW_APK_PATH):
    #     return 0
    global_pkgs = os.listdir(config.SECTION_DATA_PATH)
    iterate_rodata(global_pkgs, straight_detector_rodata, DLname,config.suffix_list_all[DLname],config.SECTION_DATA_PATH,config.magic_str_all[DLname])
    find_model_via_suffix(list(DL_PKGS[DLname].keys()), config.suffix_list_all[DLname], DLname)

def extract_models(cat):
    for k in list(config.magic_str_all.keys()):
        print(("==================="+k+"===================="))
        
        extract_model(k)
        print((json.dumps(DL_PKGS[k],indent=4,ensure_ascii=False)))
        print((json.dumps(DL_MODELS[k],indent=4,ensure_ascii=False)))
    for key, val in DL_MODELS.items():
        if val != {}:
            with open('/home/edodor/mbdir/MobileDL/code/configuration/modl.txt', "a") as myfile:
                myfile.write('%s:%s\n' % (key, val))
    for key, val in DL_PKGS.items():
        if val != {}:
            with open('/home/edodor/mbdir/MobileDL/code/configuration/pckgs.txt', "a") as myfile: 
                myfile.write('%s:%s\n' % (key, val))
    

def extract_models_all_type():
    config.SECTION_DATA_PATH=ROOT_PATH+"section_data/apks_4/"
    config.DECOMPOSED_APK_PATH = ROOT_PATH+"decomposed_apks/apks_4/"
    catorys = os.listdir(config.DECOMPOSED_APK_PATH)
    for cat in catorys:
        config.DECOMPOSED_APK_PATH=ROOT_PATH+"decomposed_apks/apks_4/"+cat+"/"
        config.SECTION_DATA_PATH=ROOT_PATH+"section_data/apks_4/" +cat

        if not os.path.exists(config.SECTION_DATA_PATH):
            continue
        extract_models(cat)

extract_models_all_type()
