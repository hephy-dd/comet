"""Collection base class."""

from collections import OrderedDict

__all__ = ['Collection']

class Collection:
    """Base class for instance collections."""

    ValueType = None

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
        if self.ValueType is not None:
            if not isinstance(value, self.ValueType):
                raise TypeError("value must inherit from {}".format(self.ValueType))
        if key in self.keys():
            raise KeyError("key is already defined: '{}'".format(key))
        self.__items[key] = value
        return value

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self.items())})"
