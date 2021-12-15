import cv2 as cv
import time
import numpy as np
import tflite_runtime.interpreter as tflite

def zip_stream(cap):
    # take frame 读取帧
    # frame (H,W,C)
    origin = []
    for i in range(16):
        ret, frame = cap.read()
        if ret:
            origin.append(np.expand_dims(frame, axis=0))
    # to "BCTHW"
    video_array = np.transpose(np.expand_dims(np.vstack(origin), axis=0),
                               (0, 4, 1, 2, 3))
    return video_array


if __name__ == '__main__':

    # 读取设备
    cap = cv.VideoCapture(0)
    # 读取摄像头FPS
    cap.set(cv.CAP_PROP_FPS, 60)
    fps = cap.get(cv.CAP_PROP_FPS)
    print('fps', fps)

    # set dimensions 设置分辨率
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 244)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 244)

    #print(a.shape)
    
    # Load the TFLite model and allocate tensors
    interpreter = tflite.Interpreter(model_path="models/x3d_m_Optimize.tflite",num_threads=4)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    while True:
        try:
            start = time.time()
            video_stream = zip_stream(cap)
            print(f"video_stream cost time:{time.time()-start}")
            start = time.time()
            
            # inference
            interpreter.set_tensor(input_details[0]['index'], video_stream.astype(np.float32))
            interpreter.invoke()
            # get_tensor() returns a copy of the tensor data
            # use tensor() in order to get a pointer to the tensor
            output_data = interpreter.get_tensor(output_details[0]['index'])

            print(output_data, f"cost time:{time.time()-start}")
        except KeyError as e:
            break

    # release camera 必须要释放摄像头
    cap.release()
