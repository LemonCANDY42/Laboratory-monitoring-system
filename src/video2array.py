import cv2
import numpy as np
import sys
sys.path.append("..") 
from func import all_path

def video_to_array(path = '../video/New directory'):
    video_array = []
    for i in all_path(path):

        cap = cv2.VideoCapture(i)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        count = frameCount//16
        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        #BCTHW
        for i in range(count):
            buf = np.empty((16, 244, 244,3), np.dtype('uint8'))
            fc = 0
            ret = True
            try:
                while (fc < 16  and ret):
                    ret,_buf = cap.read()
                    buf[fc] = cv2.resize(_buf,(244,244))
                    fc += 1
                buf = np.transpose(np.array(buf),(3,0,1,2))
                video_array.append(buf)
            except Exception as e:
                print(e)
        print(len(video_array))

        cap.release()

    return video_array

if __name__ == "__main__":
    video_to_array()

# cv2.namedWindow('frame 10')
# cv2.imshow('frame 10', buf[9])

# cv2.waitKey(0)