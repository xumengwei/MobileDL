# Extract zip files
import os
import sys

from basic_func import run_cmd,iterate_dir

DECOMPOSED_APK_PATH='/storage2/echo/decomposed_apks/'

def extract_file(in_file, out_dir):
	if in_file.endswith('.gz'):
		cmd = 'zcat ' + in_file + ' > ' + out_dir
		run_cmd(cmd)
	elif in_file.endswith('.7z'):
		cmd = '7z e ' + in_file
		run_cmd(cmd)
	elif in_file.endswith('.zip'):
		cmd = 'unzip ' + in_file + ' -d ' + out_dir
		run_cmd(cmd)

def extract_filter(path):
	return path.split('.')[-1] in ['zip', 'gz', 'rar', 'tar', '7z']

def get_zips(pkgs):
	ret = []
	for pkg in pkgs:
		ret += iterate_dir(os.path.join(DECOMPOSED_APK_PATH, pkg), extract_filter)
	return ret