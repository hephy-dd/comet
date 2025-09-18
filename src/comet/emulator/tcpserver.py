import argparse
import inspect
import logging
import re
import socketserver
import threading
import time
import signal
from typing import Callable, Iterable, Optional, Union

from .emulator import Emulator, Response, TextResponse

__all__ = ["TCPRequestHandler", "TCPServer", "TCPServerThread", "TCPServerContext"]


def split_data(data: bytes, terminator: bytes) -> list[bytes]:
    if terminator:
        return data.split(terminator)
    return [data]


class TCPRequestHandler(socketserver.BaseRequestHandler):
    def read_messages(self, context) -> Optional[list[bytes]]:
        data = self.request.recv(4096)
        if not data:
            return None
        context.logger.info("recv %s", data)
        termination_bytes = context.termination
        return [line for line in split_data(data, termination_bytes) if line]

    def send_messages(self, context, response: Union[Response, Iterable[Response]]) -> None:
        termination_bytes = context.termination
        if not isinstance(response, (list, tuple)):
            response = [response]  # type: ignore
        buffer = bytearray()
        for res in response:
            buffer.extend(bytes(res))
            if isinstance(res, TextResponse):
                buffer.extend(termination_bytes)
        data = bytes(buffer)
        context.logger.info("send %s", data)
        self.request.sendall(data)

    def handle(self) -> None:
        context = self.server.context  # type: ignore
        while True:
            messages = self.read_messages(context)
            if not messages:
                break
            for message in messages:
                response = context.handle_message(str(message, "utf-8"))
                if response is not None:
                    self.send_messages(context, response)


class TCPServerContext:
    def __init__(self, name: str, emulator: Emulator, termination: str, request_delay: float) -> None:
        self.name: str = name
        self.emulator: Emulator = emulator
        self.termination: bytes = termination.encode("utf-8")
        self.request_delay: float = request_delay
        self.logger: logging.Logger = logging.getLogger(name)

    def handle_message(self, message: str) -> Union[None, Response, Iterable[Response]]:
        response = self.emulator(message)
        time.sleep(self.request_delay)
        return response


class TCPServer(socketserver.TCPServer):
    allow_reuse_address: bool = True

    def __init__(self, address: tuple[str, int], context: TCPServerContext) -> None:
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


def option_type(value: str) -> tuple[str, str]:
    m = re.match(r"^([\w_][\w\d_]*)=(.*)$", value)
    if m:
        return m.group(1), m.group(2)
    raise argparse.ArgumentTypeError("expected key=value")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--hostname",
        default="localhost",
        help="hostname, default is 'localhost'",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=10000,
        help="port, default is 10000",
    )
    parser.add_argument(
        "-t",
        "--termination",
        default="\r\n",
        help="message termination, default is '\\r\\n'",
    )
    parser.add_argument(
        "-d",
        "--request-delay",
        type=float,
        default=0.1,
        help="delay between requests in seconds, default is 0.1 sec",
    )
    parser.add_argument(
        "-o",
        "--option",
        type=option_type,
        action="append",
        default=[],
        help="set emulator specific option(s), e.g. '-o version=2.1'",
    )
    return parser.parse_args()


def run(emulator: Emulator) -> int:
    """Convenience emulator runner using TCP server."""
    if not isinstance(emulator, Emulator):
        raise TypeError(f"Emulator must inherit from {Emulator}")

    args = parse_args()
    emulator.options.update({key: value for key, value in args.option})

    logging.basicConfig(level=logging.INFO)

    mod = inspect.getmodule(emulator.__class__)
    name = (getattr(getattr(mod, "__spec__", None), "name", None)
            or emulator.__class__.__module__)

    context = TCPServerContext(name, emulator, args.termination, args.request_delay)
    address = args.hostname, args.port
    server = TCPServer(address, context)
    thread = TCPServerThread(server)

    hostname, port, *_ = server.server_address  # IPv4/IPv6
    context.logger.info("starting... %s:%s", hostname, port)

    thread.start()

    def handle_event(signum, frame):
        context.logger.info("stopping... %s:%s", hostname, port)
        server.shutdown()

    signal.signal(signal.SIGTERM, handle_event)
    signal.signal(signal.SIGINT, handle_event)

    thread.join()

    return 0
