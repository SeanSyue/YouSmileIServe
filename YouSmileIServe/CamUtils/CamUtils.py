from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
import logging

from .ThreadCam import ThreadCam
from .qr_decoder import decode
from . import face_detection

LIKELIHOOD_NAME = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')


def detect_smile():
    is_smiled = False
    smile_icom = cv2.imread("/home/pi/.config/YouSmileIServe/smile.jpg")
    smile_icom = cv2.resize(smile_icom, (225, 225))
    cap = ThreadCam(0)
    cap.set_prop(640, 480, 30)
    cap.start()
    sleep(1)
    logging.getLogger(__name__).info("Please smile")
    joy = -1
    while cap.isOpened():

        image = cap.Frame
        img_bytes = cv2.imencode('.jpg', image)[1].tostring()
        faces_info = face_detection.detect_face(img_bytes, 1)

        if faces_info:
            for face in faces_info:
                if joy == -1:
                    logging.getLogger(__name__).info("Please smile")
                    joy = 0
                    
                joy = face.joy_likelihood
                logging.getLogger(__name__).info("joy: " + str(LIKELIHOOD_NAME[joy]))
                # print("joy: ", LIKELIHOOD_NAME[joy])

        cv2.imshow("Smile dectect", image)
        key = cv2.waitKey(1) & 0xFF
        if joy >= 3:
            logging.getLogger(__name__).info("OK! You Smile!")
            for _ in range(200):
                image = cap.Frame
                image[0:225, -225:] = smile_icom
                cv2.imshow("Smile dectect", image)
                cv2.waitKey(1)
            cap.stop()
            is_smiled = True
            break            
        
        if key in [ord("q"), ord("o")] or joy >= 3:
            logging.getLogger(__name__).info("Close camera")
            # print("JOY: ", LIKELIHOOD_NAME[joy])
            cap.stop()
            is_smiled = False
            break

    cv2.destroyAllWindows()
    cap.release()

    return is_smiled


def scan_qrcode():
    """
    detect qrcode during payment session
    :param camera: picamera.PiCamera
    :return:is_payed: indicate whether payment accomplished(QR code detected)
    """
    # initialize the camera and grab a reference to the raw camera capture
    # print("[INFO] Start scanning QR code!")
    logging.getLogger(__name__).info("Start scanning QR code!")
    is_payed = False
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(320, 240))
    # allow the camera to warmup
    sleep(3)
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        qrdata = decode(image)
        if qrdata:
            # print("[INFO] Payment received!")
            logging.getLogger(__name__).info("Payment received!")
            is_payed = True
            break

        cv2.imshow("Please pay by QRcode", image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        if key == ord("q"):
            logging.getLogger(__name__).info("Quit scanning QR code!")
            break

    camera.close()
    cv2.destroyAllWindows()
    return is_payed
