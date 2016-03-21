#!/usr/bin/env python
import time
import SocketServer
from ddbpy.client import Send

DFE = ('127.0.0.1', 5555)
BUCKET = 'graphite'
DEBUG = False


class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        if DEBUG:
            socket = self.request[1]
            print data.split()[0], data.split()[1]
            socket.sendto(data.upper(), self.client_address)
        with Send(DFE) as send:
            send.switch_streaming(BUCKET)
            ts = int(time.time())
            metric = data.split()[0]
            value = data.split()[1]
            send.send_payload(metric, ts, value)


def main():
    HOST, PORT = "0.0.0.0", 2003
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()
