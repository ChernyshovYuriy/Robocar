import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import shutil
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8080


# This class will handles any incoming request from
# the browser
class ConnectionHandler(BaseHTTPRequestHandler):

    echo_data = None
    controller_in = None

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

        print("Init ConnectionHandler")

    # Handler for the GET requests
    def do_GET(self):
        print("GET: %s" % self.path)
        try:
            # Check the file extension required and
            # set the right mime type
            if self.path.endswith(".html"):
                mimetype = 'text/html'
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
            if self.path.endswith(".css"):
                mimetype = 'text/css'
            if self.path.endswith("/camera"):
                self.send_image()
            if self.path.endswith("/echo"):
                self.send_echo()
            if self.path.endswith("/battery/level"):
                self.send_battery_level()

            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests
    def do_POST(self):
        print("POST: %s" % self.path)
        if self.path == "/camera":
            # self.send_image()
            pass
        if self.path == "/motors/stop":
            self.controller_in.eng_stop()
            pass
        if self.path == "/motors/fwd":
            self.controller_in.eng_fwd()
            pass
        if self.path == "/motors/bwd":
            self.controller_in.eng_bwd()
            pass
        if self.path == "/motors/turn/left":
            self.controller_in.eng_turn_l()
            pass
        if self.path == "/motors/turn/right":
            self.controller_in.eng_turn_r()
            pass
        if self.path == "/start":
            self.controller_in.start()
            pass
        if self.path == "/stop":
            self.controller_in.stop()
            pass

    def send_image(self):
        mime_type = 'image/jpg'
        url = "/home/pi/dev/ivan/robocar/py/img/camera_image.jpg"
        print("url %s" % url)
        f = open(url, "rb")
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()
        with open(url, 'rb') as content:
            shutil.copyfileobj(content, self.wfile)
        f.close()

    def send_echo(self):
        mime_type = 'text/plain'
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        message = "-- Robocar greeting you --"
        if self.echo_data is not None and self.echo_data.echo is not "":
            message = " ".join(str(e) for e in self.echo_data.echo)
        self.wfile.write(bytes(message, "utf-8"))

    def send_battery_level(self):
        mime_type = 'text/plain'
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        message = "100%"
        if self.echo_data is not None and self.echo_data.echo is not "":
            message = " ".join(str(e) for e in self.echo_data.echo)
        self.wfile.write(bytes(message, "utf-8"))


class HttpServer:

    echo_data = ""

    def __init__(self, data, controller_in):
        print("Init  http server")
        # Create a web server and define the handler to manage the
        # incoming request
        self.data = data
        ConnectionHandler.echo_data = self.data
        ConnectionHandler.controller_in = controller_in
        self.server = HTTPServer(('', PORT_NUMBER), ConnectionHandler)
        self.is_run = False
        self.thread = None

    def start(self):
        if self.is_run is True:
            return

        self.is_run = True
        """Run echo in separate thread"""
        if self.thread is None:
            self.thread = Thread(target=self.runnable)
        self.thread.start()

    def stop(self):
        if self.is_run is False:
            return

        print('Shutting down http server')
        self.is_run = False
        self.server.socket.close()
        self.server.shutdown()
        self.thread = None

    def runnable(self):
        while self.is_run:
            print('Started http server on port ', PORT_NUMBER)
            # Wait forever for incoming http requests
            self.server.serve_forever()
        print('Exit runnable of http server')


class HttpServerData:

    def __init__(self):
        print("Init  http server data")
        self.echo = ""
