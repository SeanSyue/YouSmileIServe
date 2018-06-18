# -*- coding: utf-8 -*-
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time, threading
import cv2, numpy as np
# from PIL.Image import fromarray


from QRdecoder import decode
import face_detection

# from face_detection import Facedetection
LIKELIHOOD_NAME = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                   'LIKELY', 'VERY_LIKELY')


# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class camCapture(object):
    def __init__(self, target):
        self.Frame = []
        self.status = False
        self.isstop = False

        # 攝影機連接。
        self.capture = cv2.VideoCapture(target)

    def setprop(self, width=640, height=480, fps=30):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.capture.set(cv2.CAP_PROP_FPS, fps)

    def start(self):
        # 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('cam started!')
        T = threading.Thread(target=self.queryframe, args=())
        T.setDaemon(True)
        T.start()

    def stop(self):
        # 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('cam stopped!')

    def getframe(self):
        # 當有需要影像時，再回傳最新的影像。
        return self.Frame

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()

        self.capture.release()

    def isOpened(self):
        return self.capture.isOpened()


if __name__ == "__main__":

    # google_face = Facedetection()

    cap = camCapture(0)
    cap.setprop(640, 480, 30)
    cap.start()
    time.sleep(1)

    while cap.isOpened():

        image = cap.getframe()
        img_bytes = cv2.imencode('.jpg', image)[1].tostring()
        faces_INFO = face_detection.detect_face(img_bytes, 1)

        joy = 0
        surprise = 0
        if faces_INFO:
            for face in faces_INFO:
                joy = face.joy_likelihood
                surprise = face.surprise_likelihood
                print('joy: {}\n'
                      'surprise: {}'.format(LIKELIHOOD_NAME[joy], LIKELIHOOD_NAME[surprise]))

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        # rawCapture.truncate(0)
        if key in [ord("q"), ord("o")] or joy >= 3 or surprise >= 3:
            print("JOY: {}\n"
                  "SURPRISE: {}".format(LIKELIHOOD_NAME[joy], LIKELIHOOD_NAME[surprise]))
            cap.stop()
            break

    cv2.destroyAllWindows()
    cap.capture.release()

    # # initialize the camera and grab a reference to the raw camera capture
    # camera = PiCamera()
    # time.sleep(1)
    # camera.resolution = (320, 240)
    # camera.framerate = 30
    # rawCapture = PiRGBArray(camera, size=(320, 240))
    # # allow the camera to warmup
    # time.sleep(0.1)
    # # capture frames from the camera
    # for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #     # grab the raw NumPy array representing the image, then initialize the timestamp
    #     # and occupied/unoccupied text
    #     image = frame.array
    #     qrdata = decode(image)
    #     if qrdata:
    #         # print qrdata
    #         for obj in qrdata:
    #             # print('Type : ', obj.type)
    #             print('Data : ' + str(obj.data))
    #
    #     # show the frame
    #     cv2.imshow("Frame", image)
    #     key = cv2.waitKey(1) & 0xFF
    #     # clear the stream in preparation for the next frame
    #     rawCapture.truncate(0)
    #     # if the `q` key was pressed, break from the loop
    #     if key == ord("q"):
    #         break
    #
    # cv2.destroyAllWindows()
