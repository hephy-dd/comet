import importlib
import inspect
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

__all__ = [
    "emulator_factory",
    "TextResponse",
    "BinaryResponse",
    "RawResponse",
    "message",
    "Emulator",
]

logger = logging.getLogger(__name__)

emulator_registry: dict[str, type["Emulator"]] = {}


def emulator_factory(module_name: str) -> type["Emulator"]:
    """Returns emulator class from module specified by `module_name`."""
    key: str = module_name
    if key not in emulator_registry:
        try:
            # Try to load module from global namespace
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            # Package can be None
            if not __package__:
                raise
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


@dataclass
class Response(ABC):
    """Base class for emulator response types."""

    @abstractmethod
    def __bytes__(self) -> bytes: ...


@dataclass(repr=False)
class TextResponse(Response):
    """SCPI text response with optional encoding."""
    text: str
    encoding: str = "ascii"  # SCPI default is ascii

    def __repr__(self) -> str:
        n_chars = len(self.text)
        preview = f"{self.text[:13]}..." if n_chars > 16 else self.text
        return f"<{type(self).__name__} text={preview!r} encoding={self.encoding!r}>"

    def __bytes__(self) -> bytes:
        return self.text.encode(self.encoding)

    def __int__(self) -> int:
        return int(self.text)

    def __float__(self) -> float:
        return float(self.text)

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TextResponse):
            return (self.text, self.encoding) == (other.text, other.encoding)
        if isinstance(other, str):
            return self.text == other
        if isinstance(other, bytes):
            return bytes(self) == other
        return False


@dataclass(repr=False)
class RawResponse(Response):
    """Generic bytes response."""
    data: bytes

    def __repr__(self) -> str:
        n_bytes = len(self.data)
        preview = self.data[:13] + b"..." if n_bytes > 16 else self.data
        return f"<{type(self).__name__} size={n_bytes!r} data={preview!r}>"

    def __bytes__(self) -> bytes:
        return self.data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RawResponse):
            return self.data == other.data
        if isinstance(other, bytes):
            return self.data == other
        return False


@dataclass(repr=False)
class BinaryResponse(RawResponse):
    """Binary SCPI block response in format `#<n_chr_size><chr_size><bytes>`."""

    def __bytes__(self) -> bytes:
        n_bytes = len(self.data)
        n_digits = len(str(n_bytes))
        if n_digits > 9:
            raise ValueError(
                f"Invalid SCPI block length {n_bytes}; "
                "must be representable with 1-9 digits."
            )
        header = f"#{n_digits}{n_bytes}".encode("ascii")
        return header + self.data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BinaryResponse):
            return self.data == other.data
        if isinstance(other, bytes):
            return bytes(self) == other
        return False


def make_response(response: Any) -> Response:
    """Helper function to convert various types returned by emulator routes into
    emulator response types.

    >>> make_response("spam")
    <TextResponse text='spam' encoding='ascii'>
    >>> make_response(42)
    <TextResponse text='42' encoding='ascii'>
    >>> make_response(b"shrubbery")
    <BinaryResponse size=9 data=b'shrubbery'>
    """
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


def normalize_route(pattern: str) -> str:
    """Remove a leading ^ only if it's at the very start of the regex (and not escaped)."""
    if pattern.startswith("^") and not pattern.startswith(r"\^"):
        return pattern[1:]
    return pattern


class Route:
    """Route wrapper for message routing."""
    __slots__ = ["route", "pattern", "method"]

    def __init__(self, route: str, method: Callable[..., Any]) -> None:
        self.route: str = normalize_route(route)
        self.pattern = re.compile(self.route)  # precompile for speed
        self.method: Callable[..., Any] = method

    def __call__(self, *args, **kwargs) -> Any:
        return self.method(*args, **kwargs)

    def match(self, message: str) -> Optional[tuple[str, ...]]:
        m = self.pattern.match(message)
        return m.groups() if m else None


def get_routes(cls: type) -> list[Route]:
    """Return routes with subclass overrides by regex pattern."""
    by_pattern: dict[tuple[str, int], Route] = {}

    # Subclass first, bases later, so subclass wins.
    for cls_ in cls.__mro__:
        for attr in cls_.__dict__.values():
            if isinstance(attr, Route):
                key = (attr.pattern.pattern, attr.pattern.flags)
                # keep the first seen (from the most-derived class)
                by_pattern.setdefault(key, attr)

    routes = list(by_pattern.values())
    # Reverse sort by expression length for specificity; tie-breaker: method name.
    routes.sort(key=lambda r: (-len(r.pattern.pattern), r.method.__name__))
    return routes


def message(route: str) -> Callable[[Callable[..., Any]], Route]:
    """Decorator to register a regex route for an emulator method."""

    def decorator(method: Callable[..., Any]) -> Route:
        return Route(route, method)

    return decorator


class Emulator:
    def __init__(self) -> None:
        self.options: dict[str, Any] = {}

    def __call__(self, message: str) -> Union[None, Response, list[Response]]:
        logger.debug("handle message: %s", message)
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
