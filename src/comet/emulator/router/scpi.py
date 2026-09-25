# scpi.py

from dataclasses import dataclass

from .router import route

__all__ = ["scpi"]


@dataclass(frozen=True)
class Command:
    path: tuple[str, ...]
    query: bool
    args: tuple[str, ...] = ()


def parse(message: str) -> Command:
    header, *rest = message.strip().split(maxsplit=1)

    query = header.endswith("?")
    header = header.removesuffix("?")

    path = tuple(filter(None, header.lstrip(":").split(":")))

    args = ()
    if rest:
        args = tuple(x.strip() for x in rest[0].split(","))

    return Command(path, query, args)


def keyword_matches(value: str, spec: str) -> bool:
    minimum = sum(c.isupper() for c in spec)

    value = value.upper()
    spec_upper = spec.upper()

    return minimum <= len(value) <= len(spec_upper) and spec_upper.startswith(value)


class Scpi:
    def __init__(self, spec: str):
        self.spec = parse(spec)

    def match(self, message: str):
        command = parse(message)

        if command.query != self.spec.query:
            return None

        if len(command.path) != len(self.spec.path):
            return None

        if not all(
            keyword_matches(value, expected)
            for value, expected in zip(command.path, self.spec.path)
        ):
            return None

        return command.args


def scpi(spec: str):
    return route(Scpi(spec))
