import importlib
import inspect
import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union

__all__ = ["Emulator", "message", "emulator_factory"]

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


class Response(ABC):
    @abstractmethod
    def __bytes__(self) -> bytes: ...


class TextResponse(Response):
    def __init__(self, text: str, *, encoding: str = "ascii") -> None:
        self.text: str = text
        self.encoding: str = encoding

    def __repr__(self) -> str:
        return f"<{type(self).__name__} text={self.text!r} encoding={self.encoding}>"

    def __bytes__(self) -> bytes:
        return self.text.encode(self.encoding)

    def __int__(self) -> int:
        return int(self.text)

    def __float__(self) -> float:
        return float(self.text)

    def __str__(self) -> str:
        return bytes(self).decode("utf-8")

    def __eq__(self, other):
        if isinstance(other, TextResponse):
            return (self.text, self.encoding) == (other.text, other.encoding)
        if isinstance(other, str):
            return bytes(self) == other.encode("utf-8")
        if isinstance(other, bytes):
            return bytes(self) == other
        return NotImplemented


class BinaryResponse(Response):
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data

    def __repr__(self) -> str:
        return f"<{type(self).__name__} size={len(self.data)} data={self.data!r}>"

    def __bytes__(self) -> bytes:
        n_bytes = len(self.data)
        n_chars = len(str(n_bytes))
        header = f"#{n_chars}{n_bytes}".encode("ascii")
        return header + self.data

    def __eq__(self, other):
        if isinstance(other, BinaryResponse):
            return self.data == other.data
        if isinstance(other, bytes):
            return bytes(self) == other
        return NotImplemented


class RawResponse(Response):
    def __init__(self, data: bytes) -> None:
        self.data: bytes = data

    def __repr__(self) -> str:
        return f"<{type(self).__name__} data={self.data!r}>"

    def __bytes__(self) -> bytes:
        return self.data

    def __eq__(self, other):
        if isinstance(other, RawResponse):
            return self.data == other.data
        if isinstance(other, bytes):
            return bytes(self) == other
        return NotImplemented


def make_response(response: Any) -> Response:
    if isinstance(response, Response):
        return response
    elif isinstance(response, int):
        return TextResponse(format(response))
    elif isinstance(response, float):
        return TextResponse(format(response))
    elif isinstance(response, str):
        return TextResponse(response)
    elif isinstance(response, bytes):
        return BinaryResponse(response)
    elif isinstance(response, bytearray):
        return BinaryResponse(bytes(response))
    raise TypeError(f"Invalid response type: {type(response)}")


class Emulator:
    def __init__(self) -> None:
        self.options: dict[str, Any] = {}

    def __call__(self, message: str) -> Union[None, Response, list[Response]]:
        logging.debug("handle message: %s", message)
        for route in get_routes(type(self)):
            args = route.match(message)
            if args is not None:
                response = route(self, *args)
                if response is not None:
                    if isinstance(response, (list, tuple)):
                        return [make_response(res) for res in response]
                    return make_response(response)
                return response
        return None
