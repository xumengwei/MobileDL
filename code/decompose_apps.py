# Extract apk files using *apktool*
import os
import sys
import subprocess

from basic_func import run_cmd

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python decompose_apps.py input_apk_path output_dir"
		print "example : python decompose_apps.py ../data/raw_apks/ ../data/decomposed_apks/"
		exit(0)
# input path
RAW_APK_PATH=sys.argv[1]
# output path
DECOMPOSED_APK_PATH=sys.argv[2]  

def decompose_single_apk(in_app, out_dir, with_res=True, with_src=False):
	cmd = 'apktool d ' + in_app + ' -o ' + out_dir
	if not with_res:
		cmd += ' --no-res'
	if not with_src:
		cmd += ' --no-src'
	run_cmd(cmd)

def decompose_apks(in_dir, out_dir, with_res=True, with_src=False):
	apks = os.listdir(in_dir)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	cnt = 0
	for apk in apks:
		if not apk.endswith('.apk'):
			continue
		in_f = os.path.join(in_dir, apk)
		out_f = os.path.join(out_dir, apk[:-4])
		decompose_single_apk(in_f, out_f, with_res=with_res, with_src=with_src)
		cnt += 1
	print (str(cnt) + ' apks successfully decomposed')

def decompose_apks_category(in_dir, out_dir, with_res=True, with_src=False):
	cats = os.listdir(in_dir)
	for cat in cats:
		cat_path = os.path.join(in_dir, cat)
		if not os.path.isdir(cat_path):
			continue
		decompose_apks(cat_path, out_dir, with_res=with_res, with_src=with_src)

decompose_apks_category(RAW_APK_PATH, DECOMPOSED_APK_PATH, with_res=False)