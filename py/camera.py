import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from threading import Thread
import py.config
if py.config.CONFIG is py.config.Platform.PI:
    from picamera import PiCamera
    from time import sleep


# Camera's class.
class Camera:

    def __init__(self):
        print("Init  camera")
        self.is_run = False
        self.thread = None
        self.camera = PiCamera()
        print("Init  camera completed")

    def start(self):
        if self.is_run is True:
            return

        print("Start camera")
        self.is_run = True
        self.camera.start_preview()
        sleep(2)
        """Run camera in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    def stop(self):
        if self.is_run is False:
            return

        print("Stop  camera")
        self.is_run = False
        self.thread = None
        self.camera.camera.stop_preview()

    def runnable(self):
        while self.is_run:
            self.camera.capture('/home/pi/dev/robocar/py/img/camera_image.jpg')
            sleep(0.1)