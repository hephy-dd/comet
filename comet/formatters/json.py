import json

from ..formatter import Formatter

__all__ = ['JsonFormatter']

class JsonFormatter(Formatter):

    def __init__(self, target):
        super().__init__(target)

    def write(self, data):
        data = json.dumps(data)
        super().write(data)
