import cv2 as cv
import time

# 读取设备
cap = cv.VideoCapture(0)
# 读取摄像头FPS
cap.set(cv.CAP_PROP_FPS, 60)
fps = cap.get(cv.CAP_PROP_FPS)
print('fps',fps)

# set dimensions 设置分辨率
cap.set(cv.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

video = cv.VideoWriter('video.mp4', cv.VideoWriter_fourcc(*"mp4v"), fps, (480, 480)) # 初始化文件写入 文件名 编码解码器 帧率 文件大小

# 录制10帧
start = time.time()
for i in range(600):
    # take frame 读取帧
    ret, frame = cap.read()
    if ret:
        # write frame to file
        #cv.imwrite('image-{}.jpg'.format(i), frame) # 截图
        video.write(frame) # 录制视频
print(time.time()-start)

# release camera 必须要释放摄像头
cap.release()