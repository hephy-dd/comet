import argparse
import logging
import re
import threading

from typing import Callable, List, Optional

from .tcpsocket import TCPServer, TCPHandler

__all__ = ['Emulator', 'message', 'run']

logger = logging.getLogger(__name__)


def message(route: str) -> Callable:
    """Method decorator for emulator message routing."""
    def message(method):
        return Route(route, method)
    return message


class Route:
    """Route wrapper class for message routes."""

    def __init__(self, route, method):
        self.route = route
        self.method = method

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)


def get_routes(cls: type) -> List[Route]:
    """Return sorted list of routes defined by method decorator."""
    routes = []
    for cls_ in cls.__mro__:
        for name in dir(cls_):
            attr = getattr(cls_, name)
            if isinstance(attr, Route):
                routes.append(attr)
    # Reverse sort methods by expression length.
    routes.sort(key=lambda route: len(route.route), reverse=True)
    return routes


class Emulator:

    def __call__(self, message: str) -> Optional[str]:
        logging.debug("handle message: %s", message)
        for route in get_routes(type(self)):
            match = re.match(route.route, message)
            if match:
                args = match.groups()
                response = route(self, *args)
                if response is not None:
                    return format(response)
                return response
        return None


def create_handler(emulator: Emulator, termination: str, delay: float) -> TCPHandler:
    handler = TCPHandler
    handler.message_handler = [emulator]
    handler.read_termination = termination
    handler.write_termination = termination
    handler.request_delay = delay
    return handler


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', default='localhost')
    parser.add_argument('-p', '--port', type=int, default=10000)
    parser.add_argument('-t', '--termination', choices=['\\n', '\\r', '\\r\\n'], default='\\r\\n')
    parser.add_argument('--delay', type=float, default=0.025)
    return parser.parse_args()


def run(emulator):
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    termination = args.termination.replace('\\n', '\n').replace('\\r', '\r')

    handler = create_handler(emulator, termination, args.delay)
    server = TCPServer((args.hostname, args.port), handler)

    def serve_forever(server):
        with server:
            server.serve_forever()

    thread = threading.Thread(target=serve_forever, args=[server], daemon=True)
    thread.start()

    try:
        threading.Event().wait()
    finally:
        server.shutdown()
        thread.join()
