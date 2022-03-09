import argparse
import importlib
import logging
import re
import threading

from typing import Any, Callable, List, Optional, Type

from .tcpsocket import TCPServer, TCPHandler

__all__ = ['Emulator', 'message', 'run']

logger = logging.getLogger(__name__)

emulator_registry = {}


def register_emulator(name):
    def register_wrapper(cls):
        emulator_registry[name] = cls
        return cls
    return register_wrapper


def emulator_factory(name):
    if name not in emulator_registry:
        importlib.import_module(f'.{name}', 'comet.emulator')
    return emulator_registry.get(name)


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
                    return format(response)
                return response
        return None
