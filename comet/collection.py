"""Collection base class."""

from collections import OrderedDict

__all__ = ['Collection']

class Collection:
    """Base class for instance collections."""

    Type = None

    def __init__(self):
        self.__items = OrderedDict()

    def __len__(self):
        return len(self.__items)

    def keys(self):
        return self.__items.keys()

    def values(self):
        return self.__items.values()

    def items(self):
        return self.__items.items()

    def get(self, key):
        if key not in self.__items:
            raise KeyError("key does not exists '{}'".format(key))
        return self.__items.get(key)

    def add(self, key, value):
        if self.Type is not None:
            if not isinstance(value, self.Type):
                raise TypeError("value must inherit from {}".format(self.Type))
        if key in self.keys():
            raise KeyError("key is already defined: '{}'".format(key))
        self.__items[key] = value
        return value

    def __repr__(self):
        return format(self.__items)
