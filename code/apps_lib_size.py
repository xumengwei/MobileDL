# DL-libs size
import os
import numpy as np

from basic_func import iterate_dir, getFileSize

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "python apps_lib_size.py decomposed_apk_path new_apk_path"
        print "example : python apps_lib_size.py ../data/decomposed_apks/ ../data/raw_apks_new/"
        exit(0)

DECOMPOSED_APK_PATH=sys.argv[1]
RAW_APK_PATH_NEW=sys.argv[2]

# all lib files extracted from DL-apps
# apk name \t lib name \t framework \n
raw_txt = '''com.artsonia.android\tlibcvextern.txt\tcaffe'''

raw_txt = raw_txt.strip().split('\n')
xsl_data = {x.split('\t')[0]: x.split('/\t')[1:] for x in raw_txt}
dl_size = {}
all_size = []
all_dl = []
for app in xsl_data.keys():
    decomposed_dir = os.path.join(DECOMPOSED_APK_PATH, app, 'lib')
    fmk = xsl_data[app][1]
    def get_dl_lib(x):
    	return x.endswith(xsl_data[app][0][:-4] + '.so')
    def get_all_lib(x):
    	return x.endswith('.so')
    dl_lib = iterate_dir(decomposed_dir, get_dl_lib)
    dl_lib_size = [1.0 * getFileSize(x) / 1024 / 1024 for x in dl_lib]
    all_lib = iterate_dir(decomposed_dir, get_all_lib)
    all_lib_size = [1.0 * getFileSize(x) / 1024 / 1024 for x in all_lib]

    if fmk not in dl_size: dl_size[fmk] = []
    dl_size[fmk] += dl_lib_size
    all_size += all_lib_size
    all_dl += dl_lib_size

for dl in dl_size:
    print dl, np.mean(dl_size[dl])
print np.mean(all_dl), np.mean(all_size)

size = []
dl_size = []
categories = os.listdir(RAW_APK_PATH_NEW)
for c in categories:
	c_apps = os.listdir(os.path.join(RAW_APK_PATH_NEW, c))
	for app in c_apps:
		apk_path = os.path.join(RAW_APK_PATH_NEW, c, app)
		s = getFileSize(apk_path)
		size.append(s)
print(size)
