import logging
import socketserver
import threading
import time
from typing import Callable, Iterable, List, Optional, Tuple, Union

__all__ = ["TCPRequestHandler", "TCPServer", "TCPServerThread", "TCPServerContext"]


def split_data(data: str, terminator: str) -> List[str]:
    if terminator:
        return data.split(terminator)
    return [data]


class TCPRequestHandler(socketserver.BaseRequestHandler):

    def read_messages(self) -> Optional[List[str]]:
        data = str(self.request.recv(4096), "ascii")
        if not data:
            return None
        self.server.context.logger.info("recv %s", bytes(data, "ascii"))  # type: ignore
        return [line for line in split_data(data, self.server.context.termination) if line]  # type: ignore

    def send_messages(self, response: Union[str, Iterable[str]]) -> None:
        if isinstance(response, (list, tuple)):
            response = self.server.context.termination.join(  # type: ignore
                format(line) for line in response
            )
        data = bytes(f"{response}{self.server.context.termination}", "ascii")  # type: ignore
        self.server.context.logger.info("send %s", data)  # type: ignore
        self.request.sendall(data)

    def handle(self) -> None:
        while True:
            messages = self.read_messages()
            if not messages:
                break
            for message in messages:
                response = self.server.context(message)  # type: ignore
                if response is not None:
                    self.send_messages(response)


class TCPServerContext:

    def __init__(self, name: str, emulator: Callable, termination: str, request_delay: float) -> None:
        self.name: str = name
        self.emulator: Callable = emulator
        self.termination: str = termination
        self.request_delay: float = request_delay
        self.logger: logging.Logger = logging.getLogger(name)

    def __call__(self, request: str) -> Union[str, Iterable[str]]:
        response = self.emulator(request)
        time.sleep(self.request_delay)
        return response


class TCPServer(socketserver.TCPServer):

    allow_reuse_address = True

    def __init__(self, address: Tuple[str, int], context: TCPServerContext) -> None:
        super().__init__(address, TCPRequestHandler)
        self.context: TCPServerContext = context


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
