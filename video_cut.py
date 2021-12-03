import numpy as np
import cv2
import os

from func import all_path

path = "/home/kenny/github/Laboratory-monitoring-system/videos/train/stop"
# 获得视频对象 
in_path = path
names = os.listdir(in_path)
out_path = path
for name in names:
    index = name.rfind('.')
    name = name[:index]
    videoCapture = cv2.VideoCapture(in_path+'/'+name+'.mp4')
    if not os.path.exists(out_path+'/'+name): # 判断文件夹是否已经存在    
        os.mkdir(out_path+'/'+name)
    # 获得码率及尺寸
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print('fps {}  size {} nums {}'.format(fps, size, fNUMS))

    # 当成功打开视频时cap.isOpened()返回True,否则返回False
    if videoCapture.isOpened(): 
        time = 2 # 每隔10秒截取一段
        frame_index = 0 # 当前帧
        while (True):
            success, frame = videoCapture.read()
            if success:
                frame_index += 1
                if (frame_index % (fps*time) == 1):
                    videoWriter = cv2.VideoWriter(out_path+'/'+name+'/'+str(int(frame_index//(fps*time))) +'.mp4',
                                                cv2.VideoWriter_fourcc(*"mp4v"), fps,size)
                    videoWriter.write(frame)
                    print(out_path+'/'+name+'/'+str(int(frame_index//(fps*time))) +'.mp4')
                else:
                    videoWriter.write(frame)
            else:
                print('end')
                break

    videoCapture.release()
