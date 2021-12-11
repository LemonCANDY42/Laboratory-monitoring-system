import cv2 as cv
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt 
import time

import numpy as np
import onnxruntime as ort

def zip_stream(cap):
  # take frame 读取帧
  # frame (H,W,C)
  origin = []
  for i in range(16):
    ret, frame = cap.read()
    if ret:
      origin.append(np.expand_dims(frame,axis=0))
  # to "BCTHW"
  video_array = np.transpose(np.expand_dims(np.vstack(origin),axis=0),(0,4,1,2,3))
  return video_array

sess = ort.InferenceSession("models/x3d_m.onnx")



if __name__ == '__main__':

  # 读取设备
  cap = cv.VideoCapture(0)
  # 读取摄像头FPS
  cap.set(cv.CAP_PROP_FPS, 60)
  fps = cap.get(cv.CAP_PROP_FPS)
  print('fps',fps)
  
  # set dimensions 设置分辨率
  cap.set(cv.CAP_PROP_FRAME_WIDTH, 244)
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, 244)
  
  
  #print(a.shape)
  
  input_name = sess.get_inputs()[0].name
  label_name = sess.get_outputs()[0].name
  while True:
    try:
      start = time.time()
      video_stream = zip_stream(cap)
      print(f"video_stream cost time:{time.time()-start}")
      start = time.time()
      pred_onx = sess.run( 
            [label_name],{input_name:video_stream.astype(np.float32)})[0][0]
      print(pred_onx,f"cost time:{time.time()-start}")
    except KeyError as e:
      break
  
  # release camera 必须要释放摄像头
  cap.release()
