import csv

from ..formatter import Formatter

__all__ = ['CsvFormatter']

class CsvFormatter(Formatter):

    def __init__(self, target, fieldnames, *args, **kwargs):
        super().__init__(target)
        self.__writer = csv.DictWriter(traget, fieldnames=fieldnames, *args, **kwargs)

    def write_header(self):
        self.__writer.writeheader()

    def write(self, data):
        self.__writer.writerow(data)
