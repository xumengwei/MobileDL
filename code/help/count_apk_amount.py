# Extract apk files using *apktool*
import os
import sys
import subprocess
import json
import pandas as pd

dfs = {}
RAW_APK_PATH = sys.argv[1]

def decompose_apks(in_dir):
	apks = os.listdir(in_dir)
	for apk in apks:
		if dfs.has_key(apk):
			dfs[apk]+=1
		else:
			dfs[apk]=1
	# print (str(cnt) + ' apks successfully decomposed')

def decompose_apks_category(in_dir):

	cats = os.listdir(in_dir)
	for cat in cats:
		cat_path = os.path.join(in_dir, cat)
		if not os.path.isdir(cat_path):
			print("no a path : ",cat_path)
			continue
		decompose_apks(cat_path)


decompose_apks_category(RAW_APK_PATH)
# print(dfs)
print(len(dfs))

