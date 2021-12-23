import cv2 as cv
#import matplotlib
#matplotlib.use('tkagg')
#import matplotlib.pyplot as plt 
import time
import numpy as np
from email_manager import EmailManager
import onnxruntime as ort
from tempfile import NamedTemporaryFile

def softmax(x):
    
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

def zip_stream(cap):
  # take frame 读取帧
  # frame (H,W,C)
  origin = []
  frame_list = []
  for i in range(16):
    ret, frame = cap.read()
    if ret:
      frame_list.append(frame)
  for i in frame_list:
    origin.append(np.expand_dims(cv.resize(i,(244,244)),axis=0))
  # to "BCTHW"
  video_array = np.transpose(np.expand_dims(np.vstack(origin),axis=0),(0,4,1,2,3))
  return video_array

sess = ort.InferenceSession("models/x3d_m.onnx")

if __name__ == '__main__':
  point = time.time()
  first = True
  em = EmailManager()
  em.set_recv(recv_email = ["124730012@qq.com","l.w.r.f.42@outlook.com"])
  em.connect()
  # 读取设备
  cap = cv.VideoCapture(0)
  # 读取摄像头FPS
  cap.set(cv.CAP_PROP_FPS, 60)
  fps = cap.get(cv.CAP_PROP_FPS)
  print('fps',fps)
  result_lists = []
  # set dimensions 设置分辨率
  cap.set(cv.CAP_PROP_FRAME_WIDTH, 480)
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
  result_dict = {0:'Working!',1:'Stop.',2:'Other.'}
  input_name = sess.get_inputs()[0].name
  label_name = sess.get_outputs()[0].name
  while True:
    try:
      
      start = time.time()
      video_stream = zip_stream(cap)
      # print(f"video_stream cost time:{time.time()-start}")
      start = time.time()
      pred_onx = sess.run( 
            [label_name],{input_name:video_stream.astype(np.float32)})[0][0]
      result_list = softmax(np.array(pred_onx)).tolist()
      result_id = result_list.index(max(result_list))
      
      if len(result_lists)==10:
          del(result_lists[0])
      elif len(result_lists)>10:
          result_lists=[]
      else:
          pass
      result_lists.append(True if result_id == 1 else False)
      result = result_dict[result_id]
      print(result+"\n")
      if all(result_lists) and len(result_lists)>5:
        if first:
          with NamedTemporaryFile(suffix='.mp4') as f:
            video = cv.VideoWriter(f.name, cv.VideoWriter_fourcc(*"mp4v"), fps, (480, 480))
            frame_list = []
            for i in range(120):
            # take frame ��ȡ֡
              ret, frame = cap.read()
              if ret:
                frame_list.append(frame)
            for i in frame_list:
              video.write(i) 
            video.release()
            f.seek(0)
            em.send_msg(str(result_list),header=result,file_list=[f.name])
            point = time.time()
        else:
          # 15分钟重发
          if time.time() - point>900:
            with NamedTemporaryFile(suffix='.mp4') as f:
              video = cv.VideoWriter(f.name, cv.VideoWriter_fourcc(*"mp4v"), fps, (480, 480))
              frame_list = []
              for i in range(120):
              # take frame ��ȡ֡
                ret, frame = cap.read()
                if ret:
                  frame_list.append(frame)
              for i in frame_list:
                video.write(i) 
              video.release()
              f.seek(0)
              em.send_msg(str(result_list),header=result,file_list=[f.name])
              point = time.time()
        first = False
          
    except KeyError as e:
      em.send_msg(str(e),header="KeyError!")
      cap.release()
      raise(e)
    except Exception as e:
      em.send_msg(str(e),header="ERROR!")
      cap.release()
      raise(e)
  
  # release camera 必须要释放摄像头
  cap.release()
