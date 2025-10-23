import importlib
import inspect
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

from .response import Response, make_response

__all__ = ["emulator_factory", "message", "Emulator"]

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
