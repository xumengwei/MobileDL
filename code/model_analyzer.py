# Analyze DL models 
# The model size, type (DNN, CNN, or RNN?), depth, usage, etc 
#Packed in the apk or downloaded after installation? (This one is easy) 
# Find more!
import os
import sys
import array
import random
import tensorflow as tf
import numpy as np

from collections import Counter
from tensorflow.python.platform import gfile
from basic_func import getFileSize
from google.protobuf import text_format
from google.protobuf.json_format import MessageToJson

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print ("python model_analyzer.py decomposed_apk_path")
		print ("example : python model_analyzer.py ../data/decomposed_apks/")
		exit(0)

DECOMPOSED_APK_PATH=sys.argv[1]

# information of all founded models
# apk name \t model path \t framework \t suffix \t usable \n 
# can load from configuration/model_xsl.txt
model_xsl = '''kr.co.daou.isa\tmbdir/MobileDL/data/section_data/apks_4/kr.co.daou.isa/libAppSuit.txt\tdllib\tmodel\t1'''
#model_xsl= '''apk_name \t model_path \t framework \t suffix \t usable \n'''
#model_xsl = '''com.iconparking\tassets/cardrecognizer/model/DateLocalization/DateLocalizationL0.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/DateLocalization/DateLocalizationL0.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/DateLocalization/DateLocalizationL1.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/DateLocalization/DateLocalizationL1.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/DateRecognition/DateRecognition.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/DateRecognition/DateRecognition.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/NameLocalization/NameLocalizationX.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/NameLocalization/NameLocalizationX.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/NameRecognition/NameSpaceCharRecognition.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/NameRecognition/NameSpaceCharRecognition.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/NumberLocalization/loc_x.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/NumberLocalization/loc_x.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/NumberLocalization/loc_y.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/NumberLocalization/loc_y.prototxt\tcaffe\tproto\t1\ncom.iconparking\tassets/cardrecognizer/model/NumberRecognition/NumberRecognition.caffemodel\tcaffe\tbin\t1\ncom.iconparking\tassets/cardrecognizer/model/NumberRecognition/NumberRecognition.prototxt\tcaffe\tproto\t1\ncom.incode.mobile\tres/raw/det1.caffemodel\tcaffe\tbin\t1\ncom.incode.mobile\tres/raw/det1_deploy.prototxt\tcaffe\tproto\t1\ncom.incode.mobile\tres/raw/det2.caffemodel\tcaffe\tbin\t1\ncom.incode.mobile\tres/raw/det2_deploy.prototxt\tcaffe\tproto\t1\ncom.incode.mobile\tres/raw/det3.caffemodel\tcaffe\tbin\t1\ncom.incode.mobile\tres/raw/det3_deploy.prototxt\tcaffe\tproto\t1\n'''

		

lines = model_xsl.split('\n')
res = {}
for l in lines:
        items = l.split('\t')
        #print (items)
        if items[3] == 'proto': continue
        mn = items[1].split('/')[-1]
        mn = mn.replace('.pb', '').replace('.tflite', '').replace('.RF', '').replace('.bin', '').replace('.caffemodel', '')
        if mn not in res: res[mn] = []
        res[mn].append(items[0])
print ({r: res[r] for r in res if len(res[r]) > 5})

def cal_flops_conv(in_shape, out_num, kw, kh, sw, sh, pw, ph):
	in_shape = [int(t) for t in in_shape]
	out_w = (in_shape[-1] - kw + 2 * pw) / sw + 1
	out_h = (in_shape[-2] - kh + 2 * ph) / sh + 1
	flops = out_w * out_h * out_num * (in_shape[0] * kw * kh + 1)
	out_shape = [out_num, out_h, out_w]
	print("ko")
	return flops, out_shape

# 5.1 TensorFlow
def tf_parse_model(model_path):
	ret_layers = []
	graph_def = tf.compat.v1.GraphDef()
	with gfile.FastGFile(model_path, 'rb') as f:
		try:
			graph_def.ParseFromString(f.read())
		except Exception as e:
			print ('Fail to parse model: ' + model_path + ', error: ' + str(e))
	for node in graph_def.node:
		ret_layers.append(node.op)
	with tf.Graph().as_default():
		tf.import_graph_def(graph_def, name="")
		run_meta = tf.compat.v1.RunMetadata()
		opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()
		flops = tf.compat.v1.profiler.profile(tf.compat.v1.get_default_graph(), run_meta=run_meta, cmd='op', options=opts)
		return {'layers': ret_layers, 'flops': flops.total_float_ops}

def tf_parse_model2(model):
	graph = tf.compat.v1.get_default_graph()
	graph_def = graph.as_graph_def()
	try:
		graph_def.ParseFromString(tf.compat.v1.gfile.FastGFile(model,'rb').read())
		tf.import_graph_def(graph_def,name='graph')
		sess = tf.compat.v1.Session()
		init = tf.compat.v1.global_variables_initializer()
		sess.run(init)
		op = sess.graph.get_operations()
		for i in op:
			print(i.values())
	except Exception as e:
		print('\\t'+str(e))

def tf_model_analyzer(model_path):
	ret = {}
	ret['model_size'] = getFileSize(model_path)
	parse_tf_model(model_path, ret)
	return ret

# 5.2 ncnn

def parse_layer_params(in_shapes, items):
	if items[0] == 'Input':
		s = [int(items[-3]), int(items[-2]), int(items[-1])]
		return 0, s
	elif items[0] == 'Convolution':
		if len(items) > 13:
			num_output, kernel_w, kernel_h, dilation, stride_w, pad_w, pad_h = [int(t) for t in items[-11:-4]]
			stride_h = stride_w
		else:
			num_output, kernel_w, dialation, stride_w, pad_w, _, _ =  [int(t) for t in items[-7:]]
			kernel_h = kernel_w
			stride_h = stride_w
			pad_h = pad_w
		if pad_w < 0: pad_w = kernel_w - 1
		if pad_h < 0: pad_h = kernel_h - 1
		r1, r2 = cal_flops_conv(in_shapes[0], num_output, kernel_w, kernel_h, stride_w, stride_h, pad_w, pad_h)
		return r1, r2
	elif items[0] == 'Pooling':
		in_shape = in_shapes[0]
		_, kernel, stride, pad, _ = [int(t) for t in items[-5:]]
		out_w = (in_shape[-1] - kernel + 2 * pad) / stride + 1
		out_h = (in_shape[-2] - kernel + 2 * pad) / stride + 1
		out_shape = [in_shapes[0][0], out_h, out_w]
		return 0, out_shape
	elif items[0] == 'InnerProduct':
		in_shape = in_shapes[0]
		return in_shape[0] * in_shape[1] * in_shape[2] * int(items[-3]), in_shape
	else:
		return 0, in_shapes[0]

def ncnn_parse_param_bin(param_file):
	f = open(param_file)
	ret_layers = []
	flops = 0
	blob_shapes = {}
	a = array.array("i")  
	# L is the typecode for uint32
	a.fromfile(f, 2)
	layer_cnt, blob_cnt = a.tolist()
	if layer_cnt == 7767517:
		print ("YYYYYYY")
	if not 0 < layer_cnt < 1000: return None
	for i in range(layer_cnt):
		a.fromfile(f, 3)
		type_index, bottom_cnt, top_cnt = a.tolist()[-3:]
		layer = tps[type_index]
		ret_layers.append(layer[0])
		if bottom_cnt > 0:
			a.fromfile(f, bottom_cnt)
			blob_in = a.tolist()[-1 * bottom_cnt:]
		else:
			blob_in = []
		if top_cnt > 0:
			a.fromfile(f, top_cnt)
			blob_out = a.tolist()[-1 * top_cnt:]
		else:
			blob_out = []
		a.fromfile(f, layer[1])
		items = a.tolist()[-1 * layer[1]:]
		_flops, _shape = parse_layer_params([blob_shapes[b] for b in blob_in], [layer[0]] + items)
		for b in blob_out:
			blob_shapes[b] = _shape
		flops += _flops
	return {'layers': ret_layers, 'flops': flops}

def ncnn_parse_param_raw(param_file):
	ret_layers = []
	flops = 0
	with open(param_file) as f:
		lines = f.readlines()
		lines = [l.strip() for l in lines]
		if lines[0] == '7767517':
			lines = lines[1:]
		layer_cnt, blob_cnt = [int(t) for t in lines[0].split()]
		blob_shapes = {}
		for i in range(layer_cnt):
			items = lines[1 + i].split()
			ret_layers.append(items[0])
			items = [t.split('=')[-1] for t in items]
			blob_in = [items[4 + x] for x in range(int(items[2]))]
			blob_out = [items[len(blob_in) + 4 + x] for x in range(int(items[3]))]
			_flops, _shape = parse_layer_params([blob_shapes[b] for b in blob_in], items)
			for b in blob_out:
				blob_shapes[b] = _shape
			flops += _flops
	return {'layers': ret_layers, 'flops': flops}

def ncnn_parse_param(param_file):
	ret = ncnn_parse_param_bin(param_file)
	if ret == None:
		ret = ncnn_parse_param_raw(param_file)
	return ret
'''
# 5.3 tflite
test_model = '/assets/vision_face_x_1.0.0.model' #fill in your path of test model of tflite
# example: ../data/models/.../xxx.tflite
#print(model_path)

interpreter = tf.lite.Interpreter(model_path=test_model)
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print (input_details, output_details,"ho")

# Test model on random input data
input_shape = input_details[0]['shape']

# change the following line to feed into your own data
input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data,"hi")
'''


# 5.4 caffe
def caffe_parse_model(model_path):
	ret_layers = []
	with open(model_path) as f:
		for line in f.readlines():
			if len(line) > 5 and line[3] != ' ' and line.find('type: ') != -1:
				layer = line.strip().split()[-1][1:-1]
				ret_layers.append(layer)
	return {'layers': ret_layers}

# 5.5 Analyze all
model_meta = [l.strip().split('\t') for l in model_xsl.split('\n')]
model_meta = [l for l in model_meta if len(l) == 5]
model_num = 0
analyzable_model_num = 0
good_apps = []
for mm in model_meta:
	if mm[3] != 'bin' and mm[4] == '1':
		analyzable_model_num += 1
		good_apps.append(mm[0])
	if mm[3] in ['bin', 'both']:
		model_num += 1
print("lo")
print (model_num, analyzable_model_num, len(list(set([mm[0] for mm in model_meta]))), len(list(set(good_apps))))

# count layers
layer_cnt = {}
# merge layers with different names
merge = {'innerproduct': 'matmul', 'conv2d': 'conv', 'convolution': 'conv', 'conv3d': 'conv', 'convolutiondepthwise': 'conv',
'avgpool': 'pooling', 'maxpool': 'pooling', 'minpool': 'pooling', 'biasadd': 'add'}
layer_cnt_total = 0
def add_to_layer_cnt(layers):
	global layer_cnt_total
	layer_cnt_total += 1
	counter = Counter(layers)
	for l in counter:
		cnt = counter[l]
		l = l.lower()
		if l in merge: l = merge[l]
		if l not in layer_cnt: layer_cnt[l] = []
		layer_cnt[l].append(cnt)

model_perf = {}
for mm in model_meta:
	app, model, fmk, tp, tag = mm
	model_path = os.path.join(DECOMPOSED_APK_PATH, app, model)
	flops = 0
	model_size = 0
	if fmk == 'ncnn' and tp != 'bin' and tag == '1':
		ret = ncnn_parse_param(model_path)
		add_to_layer_cnt(ret['layers'])
		flops = ret['flops']
		if model.find('style') != -1: flops /= 20
		if tp == 'proto':
			if model_path.endswith('.param'): prefix = model_path[:-6]
			elif model_path.endswith('.param.bin'): prefix = model_path[:-10]
			elif model_path.endswith('.proto'): prefix = model_path[:-6]
			for temp in model_meta:
				temp_path = os.path.join(DECOMPOSED_APK_PATH, temp[0], temp[1])
				if temp_path.startswith(prefix) and temp_path != model_path:
					model_size = getFileSize(temp_path)
		else:
			model_size = getFileSize(model_path)
	elif fmk.lower() in ['tensorflow', 'sensetime'] and tp != 'bin' and tag == '1':
		ret = tf_parse_model(model_path)
		if len(ret['layers']) > 0:
			add_to_layer_cnt(ret['layers'])
		flops = ret['flops']
		model_size = getFileSize(model_path)
	elif fmk.lower() == 'caffe' and tp != 'bin' and tag == '1':
		ret = caffe_parse_model(model_path)
		if len(ret['layers']) > 0:
			add_to_layer_cnt(ret['layers'])
	model_perf[app + '_' + model] = [model_size, flops]

layer_cnt = sorted(layer_cnt.items(), key = lambda x: len(x[1]), reverse=True)
print ('total cnt: ', layer_cnt_total)

for layer in layer_cnt:
	print("layer")
	print (layer[0], 1.0 * len(layer[1]) / layer_cnt_total, np.median(layer[1]), np.mean(layer[1]))

