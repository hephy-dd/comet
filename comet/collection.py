"""Collection base class."""

from collections import OrderedDict

__all__ = ['Collection']

class Collection:
    """Base class for instance collections."""

    def __init__(self, items=None, base=None):
        self.__items = OrderedDict()
        self.__base = base
        if items is not None:
            for key, value in items:
                self.add(key, value)

    def __len__(self):
        return len(self.__items)

    def keys(self):
        return self.__items.keys()

    def values(self):
        return self.__items.values()

    def items(self):
        return self.__items.copy()

    def get(self, key):
        if key not in self.__items:
            raise KeyError("key down not exists '{}'".format(key))
        return self.__items.get(key)

    def add(self, key, value):
        if self.__base is not None:
            if not isinstance(value, self.__base):
                raise TypeError("value must inherit from {}".format(self.__base))
        if key in self.keys():
            raise KeyError("key is already defined: '{}'".format(key))
        self.__items[key] = value

    def __str__(self):
        return format(self.__items)
