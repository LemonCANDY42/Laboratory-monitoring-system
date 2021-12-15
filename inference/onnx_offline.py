import cv2 as cv
import time

import numpy as np
import threading
from threading import Thread

import onnxruntime as ort
sess = ort.InferenceSession("models/x3d_m.onnx")
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

def create_thread(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs,daemon=True)
        thr.start()

    return wrapper


def softmax(x):
    
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

@create_thread
def inference_img(locker,video_stream):
    pred_onx = sess.run( 
        [label_name],{input_name:video_stream.astype(np.float32)})[0][0]
    locker.release()
    return str(softmax(np.array(pred_onx)))

    # release camera 必须要释放摄像头

