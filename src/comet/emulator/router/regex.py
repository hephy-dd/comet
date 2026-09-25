import re

from .router import route


class Regex:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def match(self, message: str):
        match = self.pattern.match(message)
        return match.groups() if match else None


def regex(pattern: str):
    return route(Regex(pattern))
