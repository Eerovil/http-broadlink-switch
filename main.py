# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import broadlink

hostName = "0.0.0.0"
serverPort = 8123

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/on':
            self.on()
        elif self.path == '/off':
            self.off()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(self.get_state(), "utf-8"))

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        print(body)
        if body == b'ON':
            self.on()
        elif body == b'OFF':
            self.off()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(self.get_state(), "utf-8"))

    def get_device(self):
        device = broadlink.hello('192.168.100.109')
        device.auth()
        return device

    def on(self):
        device = self.get_device()
        device.set_power(True)
        print("on")

    def off(self):
        device = self.get_device()
        device.set_power(False)
        print("off")

    def get_state(self):
        device = self.get_device()
        return 'on' if device.check_power() else 'off'

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
