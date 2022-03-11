import logging
import socketserver
import threading
import time

__all__ = [
    'TCPRequestHandler',
    'TCPServer',
    'TCPServerThread',
    'TCPServerContext'
]


class TCPRequestHandler(socketserver.BaseRequestHandler):

    def read_messages(self):
        data = str(self.request.recv(4096), 'ascii')
        if not data:
            return None
        self.server.context.logger.info("recv %s", bytes(data, 'ascii'))
        return [line for line in data.split(self.server.context.termination) if line]

    def send_messages(self, response):
        if isinstance(response, (list, tuple)):
            response = self.server.context.termination.join(format(line) for line in response)
        data = bytes(f'{response}{self.server.context.termination}', 'ascii')
        self.server.context.logger.info("send %s", data)
        self.request.sendall(data)

    def handle(self):
        while True:
            messages = self.read_messages()
            if not messages:
                break
            if self.server.is_shutdown:
                break
            for message in messages:
                response = self.server.context(message)
                if response is not None:
                    self.send_messages(response)


class TCPServer(socketserver.TCPServer):

    allow_reuse_address = True

    def __init__(self, address, context):
        super().__init__(address, TCPRequestHandler)
        self.context = context
        self.shutdown_event = threading.Event()

    @property
    def is_shutdown(self) -> bool:
        return self.shutdown_event.is_set()

    def shutdown(self):
        self.shutdown_event.set()
        super().shutdown()


class TCPServerThread(threading.Thread):

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.shutdown_request = threading.Event()

    def shutdown(self):
        self.shutdown_request.set()
        self.server.shutdown()

    def run(self):
        with self.server as server:
            server.serve_forever()


class TCPServerContext:

    def __init__(self, name, emulator, termination, request_delay):
        self.name = name
        self.emulator = emulator
        self.termination = termination
        self.request_delay = request_delay
        self.logger = logging.getLogger(name)

    def __call__(self, request):
        response = self.emulator(request)
        time.sleep(self.request_delay)
        return response
