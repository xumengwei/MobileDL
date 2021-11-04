'''
此文件打印每个tflite模型文件的输入输出和网络结构信息，可以根据该打印信息判定模型信息
'''
import numpy as np
import tensorflow as tf
import sys
model_path = sys.argv[1]

def get_model_info(path):
    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()
    for i in range(len(interpreter.get_tensor_details())):
        print(interpreter._interpreter.TensorName(i))
    # print(interpreter.get_tensor_details())
    for item in interpreter.get_tensor_details():
        print(item)
    return interpreter
if __name__ == '__main__':
    interpreter=get_model_info(model_path)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("inputs",input_details[0])
    print("output:", output_details[0])
