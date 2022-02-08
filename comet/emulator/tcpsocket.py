import argparse
import logging
import threading
import time
import socketserver
import re

from typing import Callable, Iterator, List

logger = logging.getLogger(__name__)

__all__ = ['TCPServer', 'TCPHandler']


def split_messages(data: str, separator: str) -> Iterator:
    """Retrun iterator of splitted messages."""
    return (message.strip() for message in data.split(separator) if message.strip())


class TCPServer(socketserver.TCPServer):

    allow_reuse_address = True


class TCPHandler(socketserver.BaseRequestHandler):

    read_termination = '\r\n'

    write_termination = '\r\n'

    request_delay = .025

    recv_size = 1024

    message_handler: List[Callable] = []

    def recv(self, n):
        data = self.request.recv(n)
        if data:
            logger.info("recv (%s, %s)", len(data), data)
        return data.decode()

    def send(self, message):
        # Multi response (eg. corvus)
        if isinstance(message, (tuple, list)):
            message = self.write_termination.join([format(m) for m in message])
        data = f"{message}{self.write_termination}".encode()
        self.request.send(data)
        logger.info("send (%s, %s)", len(data), data)

    def handle(self):
        while True:  # TODO
            data = self.recv(self.recv_size)
            if not data:
                return
            for message in split_messages(data, self.read_termination):
                self.handle_message(message)

    def handle_message(self, message):
        for message_handler in self.message_handler:
            result = message_handler(message)
            time.sleep(self.request_delay)
            if result is not None:
                self.send(result)
