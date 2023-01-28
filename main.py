# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import broadlink

hostName = "localhost"
serverPort = 8123

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/on':
            self.on()
        elif self.path == '/off':
            self.off()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>OK</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

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

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
