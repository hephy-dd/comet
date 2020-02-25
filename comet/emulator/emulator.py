"""Instrument emulation on TCP sockets."""

import argparse
import datetime
import logging
import random
import re
import time
import signal
import socketserver

__all__ = ['RequestHandler', 'TCPServer']

_expressions = {}

def message(expression):
    """Function decorator for message handling."""
    def wrapper(f):
        def call(*args, **kwargs):
            return f(*args, **kwargs)
        _expressions[expression] = call
        return call
    return wrapper

class RequestHandler(socketserver.BaseRequestHandler):

    write_termination = "\r\n"
    read_termination = "\r\n"

    state = {}

    recv_size = 1024

    def recv(self, n):
        data = self.request.recv(n)
        if data:
            logging.info("recv (%s, '%s')", len(data), data)
        return data.decode()

    def send(self, message):
        data = f"{message}{self.write_termination}".encode()
        self.request.send(data)
        logging.info("send (%s, '%s')", len(data), data)

    def handle(self):
        while True:
            data = self.recv(self.recv_size)
            if not data:
                return
            for message in data.split(self.read_termination):
                message = message.strip()
                for expression, method in _expressions.items():
                    if re.match(expression, message):
                        result = method(self, message)
                        if result is not None:
                            self.send(result)

class TCPServer:

    def __init__(self, handler):
        self.handler = handler

    def run(self, host, port):

        server = socketserver.ThreadingTCPServer((host, port), self.handler)

        logging.info("Start instrument emulation...")
        logging.info("Serving on port %s", port)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
        server.server_close()

        logging.info("Instrument emulation stopped.")

def run(handler):

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-p', '--port', default=10001, type=int)
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    server = TCPServer(handler)
    server.run(args.host, args.port)

if __name__ == "__main__":
    run(RequestHandler)
