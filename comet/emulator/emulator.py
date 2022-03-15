import argparse
import importlib
import inspect
import logging
import re
import threading

from typing import Any, Callable, List, Optional, Type

from .tcpserver import TCPServer, TCPServerContext

__all__ = ['Emulator', 'message', 'emulator_factory', 'run']

logger = logging.getLogger(__name__)

emulator_registry = {}


def emulator_factory(module_name: str) -> type:
    """Returns emulator class from module specifed by `name`."""
    if module_name not in emulator_registry:
        try:
            # Try to load module from global namespace
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            # If does not exist, try to load from comet.emulator package
            module_name = f'comet.emulator.{module_name}'
            module = importlib.import_module(module_name)
        # Iterate over all module class members (local and imported).
        cls_members = inspect.getmembers(module, inspect.isclass)
        for member_name, cls in cls_members:
            if issubclass(cls, Emulator) and cls is not Emulator:
                # Make sure class is from module, not an imported one.
                if module_name == cls.__module__:
                    emulator_registry[module_name] = cls
                    break
    cls = emulator_registry.get(module_name)
    if cls is None:
        raise RuntimeError(f"Unable to locate emulator module: {module_name}")
    return cls


def message(route: str) -> Callable:
    """Method decorator for emulator message routing."""
    def message(method):
        return Route(route, method)
    return message


class Route:
    """Route wrapper class for message routes."""

    def __init__(self, route: str, method: Callable) -> None:
        self.route: str = route
        self.method: Callable = method

    def __call__(self, *args, **kwargs) -> Any:
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
                    # If result is list or tuple make sure items are strings
                    if isinstance(response, list):
                        return list([format(r) for r in response])
                    if isinstance(response, tuple):
                        return tuple([format(r) for r in response])
                    # Else make sure result is string
                    return format(response)
                return response
        return None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', default='')
    parser.add_argument('-p', '--port', type=int, default=10000)
    parser.add_argument('-t', '--termination', default='\r\n')
    parser.add_argument('-d', '--request_delay', type=float, default=0.1)
    return parser.parse_args()


def run(emulator) -> int:
    """Convenience emulator runner using TCP server."""
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    # Relable way of getting full module name as it can be `__main__` if source
    # module is the entry point.
    name = inspect.getmodule(emulator.__class__).__spec__.name

    context = TCPServerContext(name, emulator, args.termination, args.request_delay)

    address = args.hostname, args.port
    server = TCPServer(address, context)

    hostname, port = server.server_address

    context.logger.info("starting... %s:%s", hostname, port)

    try:
        with server:
            while True:
                server.handle_request()
    except KeyboardInterrupt:
        ...

    context.logger.info("stopping... %s:%s", hostname, port)

    return 0
