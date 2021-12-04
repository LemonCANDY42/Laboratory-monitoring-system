import numpy as np
import cv2
import os

from func import all_path


path = "/home/kenny/github/Laboratory-monitoring-system/videos/train/other"
# 获得视频对象 
in_path = path
names = os.listdir(in_path)
split_time = 2
for name in names:
    index = name.rfind('.')
    name = name[:index]
    end = '.mp4'
    os.chdir(path)
    os.getcwd()
    # videoCapture = cv2.VideoCapture(in_path+'/'+name+'.mp4')
    out_path = './'+name+'/'
    if not os.path.exists(out_path): # 判断文件夹是否已经存在    
        os.mkdir(out_path)
    print(r'ffmpeg -i {0}{2} -threads 8 -vcodec copy -f segment -segment_time {3} {4}{1}%04d{2}'.format(name,name,end,split_time,out_path))  
    output = os.popen(r'ffmpeg -i {0}{2} -threads 8 -vcodec copy -f segment -segment_time {3} {4}{1}%04d{2}'.format(name,name,end,split_time,out_path)).readlines()
    