import cv2 as cv
import time
cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FPS, 60)
fps = cap.get(cv.CAP_PROP_FPS)
print('fps',fps)

# set dimensions
cap.set(cv.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

video = cv.VideoWriter('video.mp4', cv.VideoWriter_fourcc(*"mp4v"), fps, (480, 480)) 
frame_list = []
start = time.time()
for i in range(120):
    # take frame 
    ret, frame = cap.read()
    if ret:
        # write frame to file
        #cv.imwrite('image-{}.jpg'.format(i), frame) 
        frame_list.append(frame)
for i in frame_list:
  video.write(i)
print(time.time()-start)

# release camera 
cap.release()