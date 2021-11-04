'''
判断每个tflite模型文件是否能成功解释
'''
import tensorflow as tf
from collections import defaultdict, OrderedDict
import json
import sys

model_type = sys.argv[1]

def tflite_inpteret(path_model):
    # Load the TFLite model and allocate tensors.
    # print(path_model)
    interpreter = tf.lite.Interpreter(model_path=path_model)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # # Test the model on random input data.
    input_shape = input_details[0]['shape']
    output_shape = output_details[0]['shape']
    return input_shape,output_shape


def tflite_read(path_model):
    interpreter = tf.lite.Interpreter(model_path=path_model)

if __name__ == '__main__':
    
    base = "/data/mwx/decomposed_apks"
    res = defaultdict(list)
    f = open("./model_files_info/"+model_type+".txt")               # 返回一个文件对象
    line = f.readline()               # 调用文件的 readline()方法   
    while line:   
        path = base+line[1:-1]
        try:
            input_shape,output_shape = tflite_inpteret(path)
            res[path] = {}
            res[path]["interpreter"] = "sucess"
            res[path]["inputs"] =[str(i) for i in list(input_shape)]
            res[path]["outputs"] =[str(0) for i in list(output_shape)]
            
        except:
            try:
                interpreter = tf.lite.Interpreter(model_path=path)
                res[path]={}
                res[path]["interpreter"] = "sucess"
            except:
                res[path]={}
                res[path]["interpreter"] = "error"
            # print(e)
            # print(path)

        # break
        line = f.readline()   
    f.close()
    # print(res)
    print(json.dumps(res))
    with open("./model_files_info/"+model_type+".json",'w') as fp:
        json.dump(fp,res)
