import os
import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from threading import Thread
from picamera import PiCamera
from time import sleep


# Camera's class.
class Camera:

    DATA_DIR = dirname(dirname(abspath(__file__))) + "/img/cam"

    def __init__(self):
        print("Init  camera")
        self.prepare_dir()
        self.is_run = False
        self.thread = None
        self.camera = PiCamera()
        print("Init  camera completed")

    def start(self):
        if self.is_run is True:
            return

        print("Start camera")
        self.is_run = True
        self.camera.resolution = (1024, 768)
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
        self.camera.stop_preview()

    def runnable(self):
        counter = 0
        while self.is_run:
            self.camera.capture(Camera.DATA_DIR + "/camera_image_{0}.jpg".format(counter))
            counter += 1
            if counter == 10:
                counter = 0
            sleep(0.1)

    @staticmethod
    def prepare_dir():
        try:
            os.rmdir(Camera.DATA_DIR)
        except OSError:
            print("Deletion of the directory %s failed" % Camera.DATA_DIR)
        else:
            print("Successfully deleted the directory %s" % Camera.DATA_DIR)
        try:
            os.mkdir(Camera.DATA_DIR)
        except OSError:
            print("Creation of the directory %s failed" % Camera.DATA_DIR)
        else:
            print("Successfully created the directory %s " % Camera.DATA_DIR)