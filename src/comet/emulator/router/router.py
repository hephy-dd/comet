import inspect
from dataclasses import dataclass
from typing import Any


class NoRouteError(Exception):
    pass


@dataclass(frozen=True)
class Route:
    matcher: Any


def route(matcher):
    def decorator(func):
        func.__route__ = Route(matcher)
        return func

    return decorator


class Router:
    def __init__(self, target):
        self.target = target

    def dispatch(self, message: str):
        for name, member in inspect.getmembers_static(type(self.target)):
            spec = getattr(member, "__route__", None)
            if spec is None:
                continue

            args = spec.matcher.match(message)
            if args is None:
                continue

            handler = getattr(self.target, name)
            return handler(*args)

        raise NoRouteError(message)
