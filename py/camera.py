import socket
import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from threading import Thread
from picamera import PiCamera
from time import sleep


# Camera's class.
class Camera:

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
        self.camera.resolution = (640, 480)
        self.camera.framerate = 24
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
        try:
            self.camera.stop_recording()
        except Exception as e:
            print("Exception while stop streaming %s" % e)

    def runnable(self):
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('wb')
        try:
            self.camera.start_recording(connection, format='h264', quality=23)
            self.camera.wait_recording(100000000)
        except Exception as e:
            print("Exception while start streaming %s" % e)
        finally:
            try:
                connection.close()
                server_socket.close()
            except Exception as e:
                print("Exception while close streaming %s" % e)
