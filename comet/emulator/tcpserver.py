import logging
import socketserver
import threading
import time
from typing import Any, Callable, Tuple

__all__ = ["TCPRequestHandler", "TCPServer", "TCPServerThread", "TCPServerContext"]


class TCPRequestHandler(socketserver.BaseRequestHandler):
    def read_messages(self):
        data = str(self.request.recv(4096), "ascii")
        if not data:
            return None
        self.server.context.logger.info("recv %s", bytes(data, "ascii"))
        return [line for line in data.split(self.server.context.termination) if line]

    def send_messages(self, response):
        if isinstance(response, (list, tuple)):
            response = self.server.context.termination.join(
                format(line) for line in response
            )
        data = bytes(f"{response}{self.server.context.termination}", "ascii")
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

    def __init__(self, address: Tuple[str, int], context: Any) -> None:
        super().__init__(address, TCPRequestHandler)
        self.context: Any = context
        self._shutdown_event = threading.Event()

    @property
    def is_shutdown(self) -> bool:
        return self._shutdown_event.is_set()

    def shutdown(self) -> None:
        self._shutdown_event.set()
        super().shutdown()


class TCPServerThread(threading.Thread):

    def __init__(self, server: TCPServer) -> None:
        super().__init__()
        self.server: TCPServer = server
        self._shutdown_request: threading.Event = threading.Event()

    def shutdown(self) -> None:
        self._shutdown_request.set()
        self.server.shutdown()

    def run(self) -> None:
        with self.server as server:
            server.serve_forever()


class TCPServerContext:

    def __init__(self, name: str, emulator: Callable, termination: str, request_delay: float) -> None:
        self.name: str = name
        self.emulator: Callable = emulator
        self.termination: str = termination
        self.request_delay: float = request_delay
        self.logger: logging.Logger = logging.getLogger(name)

    def __call__(self, request: str) -> str:
        response = self.emulator(request)
        time.sleep(self.request_delay)
        return response
