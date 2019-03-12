# Extract useful information from so libs using *readelf*
import os
import sys

from basic_func import run_cmd, get_pkg_list

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "python extract_so.py input_apk_path decomposed_apk_path output_dir"
		print "example : python extract_so.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/"
		exit(0)

RAW_APK_PATH=sys.argv[1]
DECOMPOSED_APK_PATH=sys.argv[2]  
SECTION_DATA_PATH=sys.argv[3]  # .rodata files

def get_so_libs(decomposed_apk_path, only_search_lib_dir=False):
	ret = []
	rootdir = decomposed_apk_path
	if only_search_lib_dir:
		rootdir = os.path.join(decomposed_apk_path, 'lib')
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			filepath = os.path.join(subdir, file)
			if filepath.endswith('.so') and 'armeabi' in filepath:
				ret.append(filepath)
	return ret

def extract_section_from_lib(lib_path, out_path, sec):
	cmd = 'greadelf -p %s %s > %s' % (sec, lib_path, out_path)
	# for mac users, use *greadelf* instead
	# readelf -p .rodata libxxx.so
	run_cmd(cmd)

# Where we really execute the code
pkgs = get_pkg_list(RAW_APK_PATH)
sec = '.rodata'
out_root_dir = os.path.join(SECTION_DATA_PATH, sec)
# for mac users, the directory name cannot start with '.', change the *sec* into 'rodata'
if not os.path.exists(out_root_dir):
	os.mkdir(out_root_dir)
for p in pkgs:
	decomposed_data_path = os.path.join(DECOMPOSED_APK_PATH, p)
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
