# Detecting DL usage
# What apps are using DL?
# Where are their model files?
import os
import sys
import array
import tensorflow as tf

from tensorflow.python.platform import gfile
from extract_zip import extract_file, get_zips
from basic_func import iterate_dir, get_pkg_list,run_cmd

DL_PKGS = {}
DL_MODELS = {}

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "python DL_Sniffer_Model_extractor.py input_apk_path decomposed_apk_path section_data_path"
		print "example : python DL_Sniffer_Model_extractor.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/"
		exit(0)

RAW_APK_PATH=sys.argv[1]
DECOMPOSED_APK_PATH=sys.argv[2]  
SECTION_DATA_PATH=sys.argv[3]  # .rodata files

# model blacklist
MODEL_BLKLIST = ['com.google.android.apps.messaging/res/raw/sensitive_classifier_20171221.pb',]
for dl_lib in DL_MODELS:
	for pkg in DL_MODELS[dl_lib]:
		for model in DL_MODELS[dl_lib][pkg]:
			for bm in MODEL_BLKLIST:
				if bm in model: # if the model path contains the model in blacklist
					DL_MODELS[dl_lib][pkg].remove(model)
			if len(DL_MODELS[dl_lib][pkg]) == 0:
				DL_MODELS[dl_lib].pop(pkg, None)

global_pkgs = get_pkg_list(RAW_APK_PATH)

def iterate_rodata(pkg_list, detector, dl_lib):
	ret = {}
	sec_path = os.path.join(SECTION_DATA_PATH, '.rodata')
	for pkg in pkg_list:
		pkg_path = os.path.join(sec_path, pkg)
		if not os.path.exists(pkg_path): continue
		for lib in os.listdir(pkg_path):
			if detector(os.path.join(pkg_path, lib)):
				ret[pkg] = lib
				break
	DL_PKGS[dl_lib] = ret

# use suffix to detect DL models: this approach may have false negative
def find_model_via_suffix(pkg_list, suffix_list, dl_lib):
	def filter(path):
		for su in suffix_list:
			if path.endswith(su):
				return True
		return False
	ret = {}
	for pkg in pkg_list:
		decomposed_pkg_path = os.path.join(DECOMPOSED_APK_PATH, pkg)
		models = iterate_dir(decomposed_pkg_path, filter)
		ret[pkg] = models
	DL_MODELS[dl_lib] = ret

# 3.1 Tensorflow Lite
# Which apps are using Tensorflow Lite
def tflite_detector_rodata(lib_path):
	magic_str = ['tensorflow/contrib/lite/kernels/', 'N5EigenForTFLite', 'kTfLiteNullBufferHandle',  '/google/android/libraries/vision/facenet/']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, tflite_detector_rodata, 'tflite')
# print(len(DL_PKGS['tflite']))

# extract their model files
find_model_via_suffix(DL_PKGS['tflite'].keys(), ['.tflite', '.lite'], 'tflite')

# 3.2 Tencent ncnn
# Which apps are using ncnn
def ncnn_detector_rodata(lib_path):
	magic_str = ['overwrite existing custom layer index', 'layer load_param failed', '14ncnnClassifier', 'N4ncnn5LayerE', 'sqz set ncnn load param']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, ncnn_detector_rodata, 'ncnn')

# extract their model files
find_model_via_suffix(DL_PKGS['ncnn'].keys(), ['.param', '.bin'], 'ncnn')

def ncnn_model_validate(model_path):
	f = open(model_path)
	try:
		a = array.array("i")
		# L is the typecode for uint32
		a.fromfile(f, 2)
		layer_cnt, blob_cnt = a.tolist()
		if not 0 < layer_cnt < 1000: return False
		a.fromfile(f, 3)
		type_index, bottom_cnt, top_cnt = a.tolist()[-3:]
		if type_index != 16: return False # first layer must be input layer
		return True
	except:
		return False


# 3.3 TensorFlow
# Which apps are using Tensorflow
def tf_detector_rodata(lib_path):
	magic_str = ['N10tensorflow8GraphDefE', 'TF_AllocateTensor', 'TF_NewTensor', 'N18tensorflow20ReadOnlyMemoryRegionE', 'speech/tts/engine/neural_network/tensorflow_inference', 'org.tensorflow.framework']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, tf_detector_rodata, 'tf')

# extract their model files
find_model_via_suffix(DL_PKGS['tf'].keys(), ['.pb', '.pbtxt', 'ckpt', '.model', '.rf', '.tensorflow'], 'tf')

def tf_model_validate(model_file):
	graph_def = tf.GraphDef()
	with gfile.FastGFile(model_file, 'rb') as f:
		try:
			graph_def.ParseFromString(f.read())
		except Exception as e1:
			print 'Fail to parse model: ' + model_path
			return
	return True

zip_files = get_zips(DL_MODELS['tf'])
for f in zip_files:
	extract_file(f, f + '_EXTRACTION')
print zip_files

# 3.4 Caffe
# Which apps are using Caffe
def caffe_detector_rodata(lib_path):
	magic_str = ['caffe-android-lib/', 'pIN5caffe5Caffe3RNG9G', 'caffe.BlobProto', 'N5caffe5LayerIfEE', 'caffe::Net<float>', 'N16caffe_client_9919', 'goturn.caffemodel']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, caffe_detector_rodata, 'caffe')

# extract their model files
find_model_via_suffix(DL_PKGS['caffe'].keys(), ['.caffemodel', '.prototxt','.model'], 'caffe')

# 3.5 Caffe2
# Which apps are using Caffe2
def caffe2_detector_rodata(lib_path):
	magic_str = ['Caffe2 alloc', 'N6caffe28OpSchema', 'N6caffe26NetDefE', 'caffe2/caffe2/core/', '/gen/caffe2/caffe2Android']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, caffe2_detector_rodata, 'caffe2')

# extract their model files
find_model_via_suffix(DL_PKGS['caffe2'].keys(), ['.pb'], 'caffe2')

# 3.6 Mobile Deep Learning
#Which apps are using MDL
def mdl_detector_rodata(lib_path):
	magic_str = ['N3mdl5LayerE', '/baidu/mdl/demo/',]
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, mdl_detector_rodata, 'mdl')

# extract their model files
find_model_via_suffix(DL_PKGS['mdl'].keys(), ['.min.bin', '.min.json'], 'mdl')

# 3.7 deeplearning4j
#Which apps are using dl4j
def dl4j_detector_rodata(lib_path):
	magic_str = ['org/nd4j/nativeblas/Nd4jCpu', 'N4nd4j6random10IGeneratorE', 'N4nd4j3ops']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					return True
	return False

iterate_rodata(global_pkgs, dl4j_detector_rodata, 'dl4j')

# extract their model files
find_model_via_suffix(DL_PKGS['dl4j'].keys(), [], 'dl4j')

# 3.8 SNPE
#Which apps are using snpe
def snpe_detector_rodata(lib_path):
	magic_str = ['snpe_dsp_setup', '/SNPE/SecondParty/symphony/src/', 'snpe_get_tensor_dims']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					print(lib_path)
					return True
	return False

iterate_rodata(global_pkgs, snpe_detector_rodata, 'snpe')

# extract their model files
find_model_via_suffix(DL_PKGS['snpe'].keys(), ['.dlc'], 'snpe')

# 3.9 MxNet
#Which apps are using Mxnet
def mxnet_detector_rodata(lib_path):
	magic_str = ['N5mxnet6EngineE', 'N5mxnet13GraphExecutor']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					print(lib_path)
					return True
	return False

iterate_rodata(global_pkgs, mxnet_detector_rodata, 'mxnet')

# extract their model files
find_model_via_suffix(DL_PKGS['mxnet'].keys(), ['.params', '.json'], 'mxnet')

# 3.10 CNNDroid: https://github.com/ENCP/CNNdroid
#Which apps are using CNNdroid
def cnndroid_detector_rodata(lib_path):
	magic_str = []
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					print(lib_path)
					return True
	return False

iterate_rodata(global_pkgs, cnndroid_detector_rodata, 'cnndroid')

# extract their model files
find_model_via_suffix(DL_PKGS['cnndroid'].keys(), ['.txt', '.msg'], 'cnndroid')

# 3.11 Mace
#Which apps are using Mace
def mace_detector_rodata(lib_path):
	magic_str = ['libmace','mace_input_node_','./mace/core/','mace/kernels/','N4mace6BufferE','N4mace27PreallocatedPooledAllocatorE']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					print(lib_path)
					return True
	return False

iterate_rodata(global_pkgs, mace_detector_rodata, 'mace')

# 3.12 FeatherCNN
#Which apps are using FeatherCNN
def featherCNN_detector_rodata(lib_path):
	magic_str = ['feathercnn','feather::LayerParameter','feather::PoolingLayer']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					print(lib_path)
					return True
	return False

iterate_rodata(global_pkgs, featherCNN_detector_rodata, 'featherCNN')

# 3.13 xnn
#Which apps are using xnn
def xnn_detector_rodata(lib_path):
	magic_str = ['/xNN-wallet/Android/','/xNN/src//layers/','FALCONXNN']
	with open(lib_path) as f:
		for line in f:
			for str in magic_str:
				if str in line:
					print(lib_path)
					return True
	return False

iterate_rodata(global_pkgs, xnn_detector_rodata, 'xnn')

print DL_PKGS
print DL_MODELS


