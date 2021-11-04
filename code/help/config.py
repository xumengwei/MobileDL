RAW_APK_PATH="/data/mobileDL/raw_apks/ANDROID_WEAR"
DECOMPOSED_APK_PATH="/data/mobileDL/decompose_apps/ANDROID_WEAR"
SECTION_DATA_PATH="/data/mobileDL/section_data/ANDROID_WEAR"  # .rodata files


magic_str_all = {}
suffix_list_all = {}

magic_str = ['tensorflow/contrib/lite/kernels/', 'N5EigenForTFLite', 'kTfLiteNullBufferHandle',  '/google/android/libraries/vision/facenet/','/tensorflow/lite/']
magic_str_all["tflite"] = magic_str
suffix_list_all["tflite"] = ['.tflite', '.lite','tfl']

magic_str = ['org/nd4j/nativeblas/Nd4jCpu', 'N4nd4j6random10IGeneratorE', 'N4nd4j3ops', '/deeplearning4j/']
magic_str_all["dl4j"] = magic_str
suffix_list_all["dl4j"] = ['.zip']

magic_str = ['overwrite existing custom layer index', 'layer load_param failed', '14ncnnClassifier', 'N4ncnn5LayerE', 'sqz set ncnn load param']
magic_str_all["ncnn"] = magic_str
suffix_list_all["ncnn"] = ['.param', '.bin']

magic_str = ['.mnn', '/MNN/', 'Error for alloc memory in', 'MNN ERROR', 'MNNInfo', 'MNNWarning', 'MNN_Vulkan', 'MNNDimensionType']
magic_str_all['mnn'] = magic_str
suffix_list_all['mnn'] = ['.mnn', '.om']

magic_str = ['N6paddle4lite9operators', 'N6paddle4lite', '/Paddle-Lite/','paddle-mobile','N13paddle_mobile','paddle_mobile','PaddleMobile_','PADDLE_MOBILE__FRAMEWORK__PROTO__VAR_TYPE__TYPE_','PaddleMobile__Framework']
magic_str_all['paddleLite'] = magic_str
suffix_list_all['paddleLite'] = ['.nb',]

magic_str = ['libmace','mace_input_node_','./mace/core/','mace/kernels/','N4mace6BufferE','N4mace27PreallocatedPooledAllocatorE']
magic_str_all['mace'] = magic_str
suffix_list_all['mace'] = ['.data', 'pb']

magic_str = ['snpe_dsp_setup', '/SNPE/SecondParty/symphony/src/', 'snpe_get_tensor_dims']
magic_str_all['snpe'] = magic_str
suffix_list_all['snpe'] = ['.dlc']

magic_str = ['/dnnlibrary/','Type::TENSOR_QUANT8_ASYMM','AddTensorFromBuffer','TENSOR_BOOL8','TENSOR_QUANT8_SYMM_PER_CHANNEL','TENSOR_QUANT16_ASYMM','TENSOR_QUANT16_SYMM']
magic_str_all['DNNLibrary'] = magic_str
suffix_list_all['DNNLibrary'] = ['.daq','.onnx']

magic_str = ['N10tensorflow8GraphDefE', 'TF_AllocateTensor', 'TF_NewTensor', 'N18tensorflow20ReadOnlyMemoryRegionE', 'speech/tts/engine/neural_network/tensorflow_inference', 'org.tensorflow.framework']
magic_str_all['tensorflow'] = magic_str
suffix_list_all['tensorflow'] = ['.pb', '.pbtxt', 'ckpt', '.model', '.rf', '.tensorflow']

magic_str = ['caffe-android-lib/', 'pIN5caffe5Caffe3RNG9G', 'caffe.BlobProto', 'N5caffe5LayerIfEE', 'caffe::Net<float>', 'N16caffe_client_9919', 'goturn.caffemodel']
magic_str_all['caffe'] = magic_str
suffix_list_all['caffe'] = ['.caffemodel', '.prototxt','.model']

magic_str = ['Caffe2 alloc', 'N6caffe28OpSchema', 'N6caffe26NetDefE', 'caffe2/caffe2/core/', '/gen/caffe2/caffe2Android']
magic_str_all['caffe2'] = magic_str
suffix_list_all['caffe2'] = ['.pb']

magic_str = ['N3mdl5LayerE', '/baidu/mdl/demo/','/mdl/']
magic_str_all['mdl'] = magic_str
suffix_list_all['mdl'] = ['.min.bin', '.min.json']

magic_str = ['N5mxnet6EngineE', 'N5mxnet13GraphExecutor',' MXNET_','N4dmlc5ErrorE','N5mxnet','N4dmlc10ParamErrorE']
magic_str_all['mxnet'] = magic_str
suffix_list_all['mxnet'] = ['.params', '.json']

magic_str = ['ScriptC_convRolledIn','cnndroid','CNNdroid']
magic_str_all['cnndroid'] = magic_str
suffix_list_all['cnndroid'] = ['.txt', '.msg']

magic_str = ['feathercnn','feather::LayerParameter','feather::PoolingLayer']
magic_str_all['featherCNN'] = magic_str
suffix_list_all['featherCNN'] = ['.feathermodel']

magic_str = ['/xNN-wallet/Android/','/xNN/src//layers/','/xNN/src/layers/','FALCONXNN']
magic_str_all['xnn'] = magic_str
suffix_list_all['xnn'] = []

magic_str = ['/dlib/','VisionDetRet','jni_people_det.cpp']
magic_str_all['dlib'] = magic_str
suffix_list_all['dlib'] = ['.dat']

magic_str = ['PyTorch','TensorList','_save_for_mobile','pytorch_qnnp']
magic_str_all['pytorchmobile'] = magic_str
suffix_list_all['pytorchmobile'] = ['.pt']

magic_str = ['N11arm_compute','/arm_compute/','/GLES_COMPUTE/']
magic_str_all['computelibrary'] = magic_str
suffix_list_all['computelibrary'] = ['.csv']

magic_str = ['Tengine','tengine',"Batchtospaceend","unregister_absval_op","unregister_batchnorm_op","unregister_conv_op"]
magic_str_all['tengine'] = magic_str
suffix_list_all['tengine'] = [".timfile"]

