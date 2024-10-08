import argparse
import importlib
import inspect
import logging
import re
import signal
from typing import Any, Callable, Type, Union

from .tcpserver import TCPServer, TCPServerThread, TCPServerContext

__all__ = ["Emulator", "message", "emulator_factory", "run"]

logger = logging.getLogger(__name__)

emulator_registry: dict[str, Type] = {}


def emulator_factory(module_name: str) -> Type:
    """Returns emulator class from module specifed by `name`."""
    if module_name not in emulator_registry:
        try:
            # Try to load module from global namespace
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            # If does not exist, try to load from comet.emulator package
            module_name = f"{__package__}.{module_name}"
            module = importlib.import_module(module_name)
        # Iterate over all module class members (local and imported).
        cls_members = inspect.getmembers(module, inspect.isclass)
        for member_name, cls in cls_members:
            if issubclass(cls, Emulator) and cls is not Emulator:
                # Make sure class is from module, not an imported one.
                if module_name == cls.__module__:
                    emulator_registry[module_name] = cls
                    break
    cls = emulator_registry.get(module_name)  # type: ignore
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


def get_routes(cls: type) -> list[Route]:
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
    def __init__(self) -> None:
        self.options: dict[str, Any] = {}

    def __call__(self, message: str) -> Union[None, str, list]:
        logging.debug("handle message: %s", message)
        for route in get_routes(type(self)):
            match = re.match(route.route, message)
            if match:
                args = match.groups()
                response = route(self, *args)
                if response is not None:
                    # If result is list or tuple make sure items are strings
                    if isinstance(response, list):
                        return [format(r) for r in response]
                    if isinstance(response, tuple):
                        return [format(r) for r in response]
                    # Else make sure result is string
                    return format(response)
                return response
        return None


def option_type(value: str) -> tuple[str, str]:
    m = re.match(r"^([\w_][\w\d_]*)=(.*)$", value)
    if m:
        return m.group(1), m.group(2)
    raise ValueError()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--hostname", default="", help="hostname, default is 'localhost'"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=10000, help="port, default is 10000"
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
    args = parse_args()

    if not isinstance(emulator, Emulator):
        raise TypeError(f"Emulator must inherit from {Emulator}")

    emulator.options.update({key: value for key, value in args.option})

    logging.basicConfig(level=logging.INFO)

    # Reliable way of getting full module name as it can be `__main__` if source
    # module is the entry point.
    name = inspect.getmodule(emulator.__class__).__spec__.name  # type: ignore

    context = TCPServerContext(name, emulator, args.termination, args.request_delay)

    address = args.hostname, args.port
    server = TCPServer(address, context)
    thread = TCPServerThread(server)

    hostname, port = server.server_address

    context.logger.info("starting... %s:%s", hostname, port)

    thread.start()

    def handle_event(signum, frame):
        context.logger.info("stopping... %s:%s", hostname, port)
        server.shutdown()

    signal.signal(signal.SIGTERM, handle_event)
    signal.signal(signal.SIGINT, handle_event)

    thread.join()

    return 0  # TODO
