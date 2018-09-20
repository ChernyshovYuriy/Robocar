import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8080


# This class will handles any incoming request from
# the browser
class ConnectionHandler(BaseHTTPRequestHandler):

    echo_data = ""

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

            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests
    def do_POST(self):
        print("POST: %s" % self.path)
        if self.path == "/camera":
            # self.send_image()
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
        self.wfile.write(bytes(self.echo_data, "utf-8"))


class HttpServer:

    echo_data = ""

    def __init__(self, data):
        print("Init http server")
        # Create a web server and define the handler to manage the
        # incoming request
        self.data = data
        ConnectionHandler.echo_data = self.data.echo
        self.server = HTTPServer(('', PORT_NUMBER), ConnectionHandler)

    def start(self):
        print('Started http server on port ', PORT_NUMBER)
        # Wait forever for incoming http requests
        self.server.serve_forever()

    def stop(self):
        print('Shutting down http server')
        self.server.socket.close()


class HttpServerData:

    def __init__(self):
        print("Init http server data")
        self.echo = ""
