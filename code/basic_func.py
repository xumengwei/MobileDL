import os
import sys
import subprocess

#RAW_APK_PATH='../data/raw_apks/'
#DECOMPOSED_APK_PATH='../data/decomposed_apks/' 
#SECTION_DATA_PATH='../data/section_data/'  # .rodata files

# Some basic functions implemented
def run_cmd(cmd):
	ret = subprocess.call(cmd, shell=True)
	if ret != 0:
		print ('Exec cmd error: ' + cmd)

def run_cmd_with_output(cmd):
	return subprocess.check_output(cmd)

def getFileSize(path):
	return os.path.getsize(path)

def save_dict(data, out_path):
	with open(out_path, 'wb') as fp:
		pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)

def load_dict(in_path):
	with open(in_path, 'rb') as fp:
		return pickle.load(fp)

def get_pkg_list(path):
	pkgs = []
	c_list = os.listdir(path)
	for c in c_list:
		p_list = os.listdir(os.path.join(path, c))
		pkgs += [p[:-4] for p in p_list if p.endswith('apk')]
	return pkgs

def iterate_dir(root_dir, path_filter):
	ret = []
	for subdir, dirs, files in os.walk(root_dir):
		for file in files:
			filepath = os.path.join(subdir, file)
			if path_filter(filepath):
				ret.append(filepath)
	return ret

# get pkg_name, app_name and version of the app
def get_app_info(apk_path):
	cmd = ['/home/ubuntu/tools/aapt', 'd', 'badging', apk_path]
	ret = run_cmd_with_output(cmd)
	lines = ret.split('\\n')
	items = lines[0].strip().split()
	pkg_name = items[1].split('=')[1][1:-1]
	version = items[3].split('=')[1][1:-1]
	app_name = ''
	for line in lines:
		if line.find('application-label:') != -1:
			app_name = line.split(':')[1][1:-1]
	return pkg_name, app_name, version

def read_app_list(path):
	with open(path) as f:
		data = f.read()
		c_res = json.loads(data)
		res = reduce(lambda x, y: x + y, c_res.values())
		return c_res, res