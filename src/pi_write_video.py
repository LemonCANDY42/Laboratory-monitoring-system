import cv2 as cv
import time

# ��ȡ�豸
cap = cv.VideoCapture(0)
# ��ȡ����ͷFPS
cap.set(cv.CAP_PROP_FPS, 60)
fps = cap.get(cv.CAP_PROP_FPS)
print('fps',fps)

# set dimensions ���÷ֱ���
cap.set(cv.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

video = cv.VideoWriter('video.mp4', cv.VideoWriter_fourcc(*"mp4v"), fps, (480, 480)) # ��ʼ���ļ�д�� �ļ��� ��������� ֡�� �ļ���С

# ¼��10֡
start = time.time()
for i in range(600):
    # take frame ��ȡ֡
    ret, frame = cap.read()
    if ret:
        # write frame to file
        #cv.imwrite('image-{}.jpg'.format(i), frame) # ��ͼ
        video.write(frame) # ¼����Ƶ
print(time.time()-start)

# release camera ����Ҫ�ͷ�����ͷ
cap.release()