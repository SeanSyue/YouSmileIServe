from threading import Thread
import cv2
from cv2 import VideoCapture
import logging


class ThreadCam(VideoCapture, Thread):
    """
    Web cam + threading = low latency
    """

    def __init__(self, target):
        VideoCapture.__init__(self, target)
        Thread.__init__(self, target=self._query_frame, args=())
        self.setDaemon(True)
        self.Frame = []
        self.status = False
        self.is_stopped = False

    def set_prop(self, width=640, height=480, fps=30):
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.set(cv2.CAP_PROP_FPS, fps)

    def start(self):
        super(ThreadCam, self).start()
        logging.getLogger(__name__).info(" Camera started!")

    def stop(self):
        """ prevent infinite loop """
        self.is_stopped = True
        logging.getLogger(__name__).info(" Camera stopped!")

    def _query_frame(self):
        while not self.is_stopped:
            self.status, self.Frame = self.read()
        self.release()
