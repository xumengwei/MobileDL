# Extract apk files using *apktool*
import os
import sys
import subprocess
sys.path.append("..")
from basic_func import run_cmd

def mkdir(path):
	folder = os.path.exists(path)
	print(path)
	if not folder:
		os.mkdir(path)
		# print( "---  new folder...  ---")
		# print ("---  OK  ---"
	else:
		print ("---  There is this folder!  ---")

def decompose_single_apk(in_app, out_dir, with_res=True, with_src=False):
	if os.path.exists(out_dir):
		print(out_dir+" has exits!")
		# return
	cmd = 'apktool d ' + in_app + ' -o ' + out_dir
	if not with_res:
		cmd += ' --no-res'
	if not with_src:
		cmd += ' --no-src'
	run_cmd(cmd)

def iterate_dir_and_decompased(root_dir, path_filter):
	# ret = []
	for subdir, dirs, files in os.walk(root_dir):
		for filea in files:
			# print (filea)
			filepath = os.path.join(subdir,filea)
			# print(filepath)
			if path_filter(filepath):
				outpath2 = os.path.join(subdir,"twice")
				# mkdir(outpath2)
				decompose_single_apk(filepath,outpath2)
				# ret.append(filepath)
				print (outpath2+" success!")
	# return ret


def decoms_twice(DECOMPOSED_APK_PATH):
	def filter(path):
		# print(path)
		if path.endswith(".apk"):
			return True
		return False
	catories = os.listdir(DECOMPOSED_APK_PATH)
	for cat in catories:
		if cat == ".rodata":
			continue
		cat_path = os.path.join(DECOMPOSED_APK_PATH, cat)
		if not os.path.isdir(cat_path):
			print("no a path : ",cat_path)
			continue

		apks = os.listdir(cat_path)

		for apk in apks:
			apkpath = os.path.join(cat_path,apk)
			models = iterate_dir_and_decompased(apkpath, filter)

decoms_twice("/data/mobileDL/decompose_apps")