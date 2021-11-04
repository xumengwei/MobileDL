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
import json
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
			# print(decomposed_pkg_path)
			models = iterate_dir(decomposed_pkg_path, filter)
			ret[pkg] = models
		DL_MODELS[dl_lib] = ret

	# 1 Tensorflow Lite
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

	# extract their model files
	find_model_via_suffix(global_pkgs, ['.tflite', '.lite'], 'tflite')

	# print json.dumps(DL_PKGS, indent=4, ensure_ascii=False)
	# print json.dumps(DL_MODELS, indent=4, ensure_ascii=False)
	# exit(0)
	# 2 deeplearning4j
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
	find_model_via_suffix(global_pkgs, [], 'dl4j')

	# 3 Tencent ncnn
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
	find_model_via_suffix(global_pkgs, ['.param', '.bin'], 'ncnn')

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

	# 4 mnn
	# Which apps are using ncnn
	def mnn_detector_rodata(lib_path):
		magic_str = ['.mnn', '/MNN/', 'Error for alloc memory in', 'MNN ERROR', 'MNNInfo', 'MNNWarning', 'MNN_Vulkan', 'MNNDimensionType']
		with open(lib_path) as f:
			for line in f:
				for str in magic_str:
					if str in line:
						return True
		return False

	iterate_rodata(global_pkgs, mnn_detector_rodata, 'mnn')

	# extract their model files
	find_model_via_suffix(global_pkgs, ['.mnn', '.om'], 'mnn')

	# 5 paddle lite
	def paddleLite_detector_rodata(lib_path):
		magic_str = ['N6paddle4lite9operators15ActivationParamE', 'N6paddle4lite9operators18AffineChannelParamE', 'paddle4lite', '/Paddle-Lite/']
		with open(lib_path) as f:
			for line in f:
				for str in magic_str:
					if str in line:
						return True
		return False

	iterate_rodata(global_pkgs, paddleLite_detector_rodata, 'paddleLite')

	# extract their model files
	find_model_via_suffix(global_pkgs, ['.nb',], 'paddleLite')


	# 6 Mace
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

	# 7 SNPE
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
	find_model_via_suffix(global_pkgs, ['.dlc'], 'snpe')

	# 8 DNNLibrary
	#Which apps are using snpe
	def DNNLibrary_detector_rodata(lib_path):
		magic_str = []
		with open(lib_path) as f:
			for line in f:
				for str in magic_str:
					if str in line:
						print(lib_path)
						return True
		return False

	iterate_rodata(global_pkgs, DNNLibrary_detector_rodata, 'DNNLibrary')

	# extract their model files
	find_model_via_suffix(global_pkgs, ['daq','onnx'], 'DNNLibrary')


	# 9 TensorFlow
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
	find_model_via_suffix(global_pkgs, ['.pb', '.pbtxt', 'ckpt', '.model', '.rf', '.tensorflow'], 'tf')

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

	# 10 Caffe
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
	find_model_via_suffix(global_pkgs, ['.caffemodel', '.prototxt','.model'], 'caffe')

	# 11 Caffe2
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
	find_model_via_suffix(global_pkgs, ['.pb'], 'caffe2')

	# 12 Mobile Deep Learning
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
	find_model_via_suffix(global_pkgs, ['.min.bin', '.min.json'], 'mdl')


	# 13 MxNet
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
	find_model_via_suffix(global_pkgs, ['.params', '.json'], 'mxnet')

	# 14 CNNDroid: https://github.com/ENCP/CNNdroid
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
	find_model_via_suffix(global_pkgs, ['.txt', '.msg'], 'cnndroid')

	# 15 FeatherCNN
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
	# find_model_via_suffix(DL_PKGS['featherCNN'].keys(), ['.txt', '.msg'], 'featherCNN')

	# 16 xnn
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


	# 18 dlib
	# Which apps are using dlib
	def dlib_detector_rodata(lib_path):
		magic_str = ['/dlib/']
		with open(lib_path) as f:
			for line in f:
				for str in magic_str:
					if str in line:
						print(lib_path)
						return True
		return False


	iterate_rodata(global_pkgs, dlib_detector_rodata, 'dlib')

	# extract their model files
	find_model_via_suffix(global_pkgs, ['.dat'], 'dlib')

	with open("./DL_PKGS_tmp.json", "w") as dump_f:
		json.dump(DL_PKGS, dump_f)
	with open("./DL_MODELS_tmp.json", "w") as dump_f:
		json.dump(DL_MODELS, dump_f)

	print json.dumps(DL_PKGS,indent=4,ensure_ascii=False)
	print json.dumps(DL_MODELS,indent=4,ensure_ascii=False)


	# https://github.com/jackwish/qnnpack.git