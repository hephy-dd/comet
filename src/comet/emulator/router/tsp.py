# router/tsp.py

from dataclasses import dataclass

from .router import route

__all__ = ["call", "get", "set"]


@dataclass(frozen=True)
class Statement:
    operation: str
    path: tuple[str, ...]
    args: tuple[str, ...] = ()


def _path(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split("."))


def parse(message: str) -> Statement:
    message = message.strip()

    # print(foo.bar) -> get foo.bar
    if message.startswith("print(") and message.endswith(")"):
        path = message[6:-1].strip()
        return Statement("get", _path(path))

    # foo.bar = value -> set foo.bar, value
    if "=" in message:
        target, value = message.split("=", 1)
        return Statement(
            "set",
            _path(target.strip()),
            (value.strip(),),
        )

    # foo.bar(...) -> call foo.bar, ...
    if message.endswith(")") and "(" in message:
        name, args = message[:-1].split("(", 1)

        args = tuple(arg.strip() for arg in args.split(",") if arg.strip())

        return Statement(
            "call",
            _path(name.strip()),
            args,
        )

    raise ValueError(f"Invalid TSP statement: {message!r}")


class Tsp:
    def __init__(self, operation: str, path: str):
        self.operation = operation
        self.path = _path(path)

    def match(self, message: str):
        try:
            statement = parse(message)
        except ValueError:
            return None

        if statement.operation != self.operation:
            return None

        if statement.path != self.path:
            return None

        return statement.args


def _route(operation: str, path: str):
    return route(Tsp(operation, path))


def get(path: str):
    return _route("get", path)


def set(path: str):
    return _route("set", path)


def call(path: str):
    return _route("call", path)
