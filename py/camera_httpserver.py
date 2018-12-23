import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py import pymjpeg
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8001


class ConnectionHandler(BaseHTTPRequestHandler):

    is_loop = False

    def do_GET(self):
        print("Camera server - get incoming connection")
        self.send_response(200)
        # Response headers (multipart)
        for k, v in pymjpeg.request_headers().items():
            self.send_header(k, v)
            # Multipart content
        while ConnectionHandler.is_loop:
            filename = dirname(dirname(abspath(__file__))) + "/img/camera_image.jpg"
            # Part boundary string
            self.end_headers()
            self.wfile.write(pymjpeg.boundary.encode())
            self.end_headers()
            # Part headers
            for k, v in pymjpeg.image_headers(filename).items():
                self.send_header(k, v)
            self.end_headers()
            # Part binary
            for chunk in pymjpeg.image(filename):
                self.wfile.write(chunk)


class CameraHttpServer:

    def __init__(self):
        print("Init  Camera http server")
        self.server = HTTPServer(('', PORT_NUMBER), ConnectionHandler)
        self.is_run = False
        self.thread = None

    def start(self):
        if self.is_run is True:
            return

        self.is_run = True
        ConnectionHandler.is_loop = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    def stop(self):
        if self.is_run is False:
            return

        print('Shutting down Camera http server')
        ConnectionHandler.is_loop = False
        self.is_run = False
        self.server.socket.close()
        self.server.shutdown()
        self.thread = None

    def runnable(self):
        while self.is_run:
            print('Started Camera http server on port ', PORT_NUMBER)
            # Wait forever for incoming http requests
            self.server.serve_forever()
        print('Exit runnable of Camera http server')