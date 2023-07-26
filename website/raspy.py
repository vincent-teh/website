from threading import Event, Lock
import cv2
from website.mqtt_client import mqtt_client
import time

class Raspy():
    def __init__(self, url=0) -> None:
        self.thread = {
            'thread': None,
            'event': Event(),
            'lock': Lock()
        }
        self.image = dict(
            pre     = None,
            post   = None
        )
        self._im_lock = Lock()
        self._direction = -1
        self._url = url

    def get_pre_img(self):
        return self.image['pre']

    def get_post_img(self) -> bytes:
        return self.image['post']

    def get_direction(self):
        return self._direction

    def detect_image(self):
        cap = cv2.VideoCapture(self._url)  # Change the parameter to the appropriate camera index if needed
        while self.thread['event'].is_set():
            success, frame = cap.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break
            self._direction = 1
            frame = buffer.tobytes() # Yield the output frame in the byte format
            self.image['pre']  = buffer
            self.image['post'] = frame


