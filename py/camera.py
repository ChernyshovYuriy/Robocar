import os
import socket
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
        # self.prepare_dir()
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
        # self.camera.start_preview()
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
        # self.camera.stop_preview()
        self.camera.stop_recording()

    def runnable(self):
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('wb')
        try:
            self.camera.start_recording(connection, format='h264')
            self.camera.wait_recording(60)
            # self.camera.stop_recording()
        finally:
            connection.close()
            server_socket.close()

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