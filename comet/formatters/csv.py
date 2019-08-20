import csv

from ..formatter import Formatter

__all__ = ['CsvFormatter']

class CsvFormatter(Formatter):

    def __init__(self, target, fieldnames, formats=None, *args, **kwargs):
        super().__init__(target)
        self.__writer = csv.DictWriter(target, fieldnames=fieldnames, *args, **kwargs)
        self.__formats = formats or {}

    def write_header(self):
        self.__writer.writeheader()

    def write(self, data):
        row = {}
        for k, v in data.items():
            row[k] = format(v, self.__formats.get(k, ''))
        self.__writer.writerow(row)
