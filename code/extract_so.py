# Extract useful information from so libs using *readelf*
import os
import sys

from basic_func import run_cmd, get_pkg_list

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python extract_so.py input_apk_path decomposed_apk_path output_dir")
		print("example : python extract_so.py ../data/decomposed_apks/ ../data/section_data/")
		exit(0)

# RAW_APK_PATH=""
#DECOMPOSED_APK_PATH=""  
#SECTION_DATA_PATH=""  # .rodata files

def get_so_libs(decomposed_apk_path, only_search_lib_dir=False):
	ret = []
	rootdir = decomposed_apk_path
	if only_search_lib_dir:
		rootdir = decomposed_apk_path
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			filepath = os.path.join(subdir, file)
			if (filepath.endswith('.so') or len(filepath.split('.'))) and 'armeabi' in filepath:
				ret.append(filepath)
			elif (filepath.endswith('so') or len(filepath.split('.'))) and ('arm64-v8a' in filepath or 'arm64_v8a' in filepath):
				ret.append(filepath)
			elif (filepath.endswith('so') or len(filepath.split('.'))) and ('armeabi-v7a' in filepath or 'armeabi_v7a' in filepath):
				ret.append(filepath)
			# 

	return ret

def extract_section_from_lib(lib_path, out_path, sec):
	cmd = 'readelf -p %s %s > %s' % (sec, lib_path, out_path)
	# print(cmd)
	# for mac users, use *greadelf* instead
	# readelf -p .rodata libxxx.so
	run_cmd(cmd)

def extract_section_from_lib_of_all_type():
	# global RAW_APK_PATH
	# RAW_APK_PATH=sys.argv[1]

	global DECOMPOSED_APK_PATH
	DECOMPOSED_APK_PATH=sys.argv[1]  
	global SECTION_DATA_PATH
	SECTION_DATA_PATH=sys.argv[2]  # .rodata files
	cats = os.listdir(DECOMPOSED_APK_PATH)
	for cat in cats:
		cat_path = os.path.join(DECOMPOSED_APK_PATH, cat)
		# Where we really execute the code
		pkgs = os.listdir(cat_path)

		sec = '.rodata'
		# depath = DECOMPOSED_APK_PATH+cat
		# if not os.path.exists(depath):
		# 	continue
		out_root_dir = os.path.join(SECTION_DATA_PATH,cat)
		print(out_root_dir)
		
		# for mac users, the directory name cannot start with '.', change the *sec* into 'rodata'
		if not os.path.exists(out_root_dir):
			os.mkdir(out_root_dir)
			# print out_root_dir
		for p in pkgs:
			print(p)
			
			decomposed_data_path = os.path.join(cat_path, p)
			
			if not os.path.exists(decomposed_data_path):
				continue
			out_pkg_dir = os.path.join(out_root_dir, p)
			if not os.path.exists(out_pkg_dir):
				os.mkdir(out_pkg_dir)
			
			libs = get_so_libs(decomposed_data_path)
			for lib in libs:
				lib_name = lib.split('/')[-1][:-3]
				out_path = os.path.join(out_pkg_dir, lib_name + '.txt')
				extract_section_from_lib(lib, out_path, sec)


def extract_one(app_path,out_pkg_dir,sec):
	libs = get_so_libs(app_path)
	for lib in libs:
		lib_name = lib.split('/')[-1][:-3]
		out_path = os.path.join(out_pkg_dir, lib_name + '.txt')
		extract_section_from_lib(lib, out_path, sec)

def main():
	if len(sys.argv)==3:
		extract_section_from_lib_of_all_type()
	elif len(sys.argv)==2:
		sec = '.rodata'
		decom_path = sys.argv[1]
		sec_path = sys.argv[2]
		extract_one(decom_path,sec_path,sec)
	else:
		print("python extract_so.py input_apk_path decomposed_apk_path output_dir")
		print("example : python2.7 extract_so.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/")
		print("example : python2.7 extract_so.py test sec_test ")
main()