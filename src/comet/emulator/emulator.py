import argparse
import importlib
import inspect
import logging
import re
import signal
from typing import Any, Callable, Optional, Union

from .tcpserver import TCPServer, TCPServerThread, TCPServerContext

__all__ = ["Emulator", "message", "emulator_factory", "run"]

logger = logging.getLogger(__name__)

emulator_registry: dict[str, type["Emulator"]] = {}


def emulator_factory(module_name: str) -> type["Emulator"]:
    """Returns emulator class from module specified by `name`."""
    key: str = module_name
    if key not in emulator_registry:
        try:
            # Try to load module from global namespace
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            # If does not exist, try to load from comet.emulator package
            key = f"{__package__}.{module_name}"
            module = importlib.import_module(key)
        # Iterate over all module class members (local and imported).
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, Emulator) and cls is not Emulator:
                # Make sure class is from module, not an imported one.
                if key == cls.__module__:
                    emulator_registry[key] = cls
                    break
    if key not in emulator_registry:
        raise RuntimeError(f"Unable to locate emulator module: {module_name}")
    return emulator_registry[key]


def message(route: str) -> Callable[[Callable[..., Any]], "Route"]:
    """Decorator to register a regex route for an emulator method."""

    def decorator(method: Callable[..., Any]) -> "Route":
        return Route(route, method)

    return decorator


class Route:
    """Route wrapper for message routing."""

    def __init__(self, route: str, method: Callable[..., Any]) -> None:
        self.route: str = route
        self.pattern = re.compile(route)
        self.method: Callable[..., Any] = method

    def __call__(self, *args, **kwargs) -> Any:
        return self.method(*args, **kwargs)

    def match(self, message: str) -> Optional[tuple[str, ...]]:
        m = self.pattern.match(message)
        return m.groups() if m else None


def get_routes(cls: type) -> list[Route]:
    """Return sorted list of routes defined by method decorator."""
    routes: list[Route] = []
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

    def __call__(self, message: str) -> Union[None, str, list[str]]:
        logging.debug("handle message: %s", message)
        for route in get_routes(type(self)):
            args = route.match(message)
            if args is not None:
                response = route(self, *args)
                if response is not None:
                    # If result is list or tuple make sure items are strings
                    if isinstance(response, (list, tuple)):
                        return [format(r) for r in response]
                    # Else make sure result is string
                    return format(response)
                return response
        return None


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
