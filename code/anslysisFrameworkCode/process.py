# Extract useful information from so libs using *readelf*
import os
import sys
import json
from multiprocessing import Process,Queue
import atexit

sys.path.append("..")
from basic_func import run_cmd, get_pkg_list

# RAW_APK_PATH=""
# global DECOMPOSED_APK_PATH
DECOMPOSED_APK_PATH=sys.argv[1]
JAR_PATH = ""

key_framework = {}
key_framework["moat"] = "com/moat/analytics"
key_framework["firebase"] = "com/google/firebase/firebase_analytics"
key_framework["ucam"] = "com/uxcam/lib/uxcam"
key_framework["mixpanel"] = "com/mixpanel"
key_framework["flurry"] = "/com/flurry"
key_framework["amplitude"] = "com/amplitude"
key_framework["countly"] = "ly/count/android"
key_framework["adobe"] = "com/adobe/mobile"

key_framework["facebook"] = "com/facebook/internal"
key_framework["localytics"] = "com/localytics"

white_list=["facebook"]
white_list_cat = ["MUSIC_AND_AUDIO", "GAME_ARCADE","FAMILY_MUSICVIDEO"]
# 
# key_framework["interceptd"] = ""

res = {}

@atexit.register
def f():
    print('结束')

def detect_by_path(rootdir, key):
	for subdir, dirs, files in os.walk(rootdir):
		if key_framework[key] in subdir:
			print(subdir)
			return True
	return False

def detect_by_file(rootdir, key):
	for subdir, dirs, files in os.walk(rootdir):
		if key_framework[key] in subdir:
			for filea in files:
				if "AnalyticsEvents" in filea:
					print(subdir)
					return True
	return False
			

def extract_section_from_lib_of_all_type(key,DECOMPOSED_APK_PATH):
	# global RAW_APK_PATH
	# RAW_APK_PATH=sys.argv[1]

	# global DECOMPOSED_APK_PATH
	# DECOMPOSED_APK_PATH=sys.argv[1]
	used_info = []
	cats = os.listdir(DECOMPOSED_APK_PATH)
	for cat in cats:
		print(key+"&"+cat)
		# if cat in white_list_cat:
		# 	pass
		# else:
		# 	continue
		# print (cat)
		cat_path = os.path.join(DECOMPOSED_APK_PATH, cat)
		# print cat_path
		# Where we really execute the code
		pkgs = os.listdir(cat_path)
		for p in pkgs:
			decomposed_data_path = os.path.join(cat_path, p)
			if key not in white_list:
				is_find = detect_by_path(decomposed_data_path, key)
			else:
				is_find = detect_by_file(decomposed_data_path, key)
			if is_find==True:
				used_info.append(decomposed_data_path)
		# 		break
		# if len(used_info)>0:
		# 	break
	print(used_info)
	# with open("./detect_res"+"_"+key+".json",'w') as fp:
	# 	json.dump(fp, res,indent=4,ensure_ascii=False)
	# 		# exit(0)
	with open("./detect/detect_res"+"_"+key+".txt",'w') as fp:
		fp.write(str(used_info))
	# res[key] = used_info

def main():
	if len(sys.argv)==2:
		print(key_framework)
		qs = []
		for key in key_framework:
			# if key!="facebook":
			# 	continue
			print(key)
			p = Process(target=extract_section_from_lib_of_all_type, args=(key, DECOMPOSED_APK_PATH,))
			qs.append(p)
			# _thread.start_new_thread(extract_section_from_lib_of_all_type, (key) )
			# extract_section_from_lib_of_all_type(key)
		for i in range(len(qs)):
			qs[i].start()
		# print(res)
		# with open("./detect_res.json",'w') as fp:
		# 	json.dump(fp, res,indent=4,ensure_ascii=False)
	else:
		print "python extract_so.py input_apk_path decomposed_apk_path output_dir"
		print "example : python2.7 extract_so.py ../data/decomposed_apks/"
		print "example : python2.7 extract_so.py test sec_test "
main()
