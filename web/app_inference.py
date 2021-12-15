from flask import Flask, render_template, Response
import cv2
import threading
import numpy as np
from threading import Thread
import sys

sys.path.append('/home/pi/Laboratory-monitoring-system/')
from inference.onnx_offline import *
app = Flask(__name__)

def zip_list_stream(frame_list):
      # take frame 读取帧
  # frame (H,W,C)
  origin = []
  for i in frame_list:
      origin.append(np.expand_dims(cv2.resize(i,(244,244)),axis=0))
  # to "BCTHW"
  video_array = np.transpose(np.expand_dims(np.vstack(origin),axis=0),(0,4,1,2,3))
  return video_array

camera = cv2.VideoCapture(0)  # use 0 for web camera
# 读取摄像头FPS
camera.set(cv2.CAP_PROP_FPS, 60)
fps = camera.get(cv2.CAP_PROP_FPS)
print('fps',fps)

# # set dimensions 设置分辨率
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 244)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 244)

def gen_frames():  # generate frame by frame from camera
    locker = threading.Lock()
    text = "Warm up..."
    frame_list = []
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if len(frame_list)==16:
            del(frame_list[0])
        elif len(frame_list)>16:
            frame_list=[]
        else:
            pass
        frame_list.append(frame)
        if len(frame_list)==16 and not locker.locked():
            locker.acquire()
            text = inference_img(locker,zip_list_stream(frame_list))
        print(text)
        # cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
    