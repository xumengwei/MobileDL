# Extract useful information from dex libs using d2j-dex2jar.sh
import os
import sys
sys.path.append("..")
from basic_func import run_cmd, get_pkg_list

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "conda activate PlayStore_APK"
		print "python dex_process.py /data/mwx/decomposed_apks/ /data/mwx/section_data/r"
		print "example : python extract_so.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/"
		exit(0)

# RAW_APK_PATH=""
DECOMPOSED_APK_PATH=""
JAR_PATH = ""

def get_dex_file(rootdir,out_path):
	for subdir, dirs, files in os.walk(rootdir):
		for filea in files:
			filepath = os.path.join(subdir, filea)
			if filepath.endswith('.dex'):

				cmd = "../../tools/dex2jar/d2j-dex2jar.sh " + filepath
				print(cmd)
				state_code = run_cmd(cmd)
				file_name = filea.split(".")[0]
				remove_name = file_name+"-error.zip"
				cmd_rm = "rm " + remove_name
				run_cmd(cmd_rm)

				out_dir = os.path.join(out_path,file_name)
				if not os.path.exists(out_dir):
					os.mkdir(out_dir)

				# unzip *.jar -d path
				cmd_unzip = "jar -xf " + file_name+"-dex2jar.jar"
				print (cmd_unzip)
				

WHILE_LIST=["FAMILY_MUSICVIDEO","GAME_ARCADE","MUSIC_AND_AUDIO","TRAVEL_AND_LOCAL"]
def extract_section_from_lib_of_all_type():
	# global RAW_APK_PATH
	# RAW_APK_PATH=sys.argv[1]

	global DECOMPOSED_APK_PATH
	DECOMPOSED_APK_PATH=sys.argv[1]  
	JAR_PATH = sys.argv[2]
	
	cats = os.listdir(DECOMPOSED_APK_PATH)
	for cat in cats:
		# print (cat)
		cat_path = os.path.join(DECOMPOSED_APK_PATH, cat)
		jar_cat_path = os.path.join(JAR_PATH,cat)
		if not os.path.exists(jar_cat_path):
			os.mkdir(jar_cat_path)
		# print cat_path
		# Where we really execute the code
		pkgs = os.listdir(cat_path)
		for p in pkgs:
			# print(p)
			decomposed_data_path = os.path.join(cat_path, p)
			out_path = os.path.join(jar_cat_path,p)
			if not os.path.exists(out_path):
				os.mkdir(out_path)
			
			else:
				continue
			os.chdir(out_path)
			get_dex_file(decomposed_data_path,out_path)
			# exit(0)


def main():
	if len(sys.argv)==3:
		extract_section_from_lib_of_all_type()
	else:
		print "python extract_so.py input_apk_path decomposed_apk_path output_dir"
		print "example : python2.7 extract_so.py ../data/decomposed_apks/ ../data/section_data/"
		print "example : python2.7 extract_so.py test sec_test "
main()
