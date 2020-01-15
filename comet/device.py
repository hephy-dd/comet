import threading
import weakref
import logging
from collections import OrderedDict
from contextlib import ContextDecorator

from PyQt5 import QtCore

import visa

__all__ = ['Device', 'DeviceManager', 'DeviceMixin']

class Mapping:
    def __init__(self, d):
        self.d = d
    def get_key(self, value):
        return list(self.d.keys())[list(self.d.values()).index(value)]
    def get_value(self, key):
        return list(self.d.values())[list(self.d.keys()).index(key)]

class Node:
    """Device node for grouping properties and commands."""

    def __init__(self, parent, prefix=''):
        self.__parent = parent
        self.__prefix = prefix

    @property
    def prefix(self):
        return self.__prefix

    @property
    def options(self):
        return self.__parent.options

    @property
    def lock(self):
        return self.__parent.lock

    @property
    def resource(self):
        return self.__parent.resource

class Action:

    def __init__(self, fget=None):
        self.fget = lambda: fget

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

class Property:

    def __init__(self, fget=None, fset=None, type=None, values=None):
        pass

    def __get__(self, obj, cls):
        pass

    def __set__(self, obj, value):
        pass

class ListProperty:

    def __init__(self, fget=None, fset=None, type=None, min=None, max=None):
        pass

class DictProperty:

    def __init__(self, fget=None, fset=None, type=None, values={}):
        pass


class Device(ContextDecorator):
    """Base class for custom VISA devices.
    >>> class MyDevice(comet.Device):
    ...     @property
    ...     def voltage(self):
    ...         with self.lock:
    ...             return float(self.resource.query(':VOLT?'))
    ...     @voltage.setter
    ...     def voltage(self, value):
    ...         with self.lock:
    ...             self.resource.write(f':VOLT {value:.3f}; *OPC?')
    ...             self.resource.read()
    ...
    >>> with MyDevice('GPIB::15') as device:
    ...     device.voltage = 42
    ...     print(device.voltage)
    ...
    42.0
    """

    options = {}
    """Default options passed on to VISA resource."""

    def __init__(self, resource_name, **options):
        options.update(dict(resource_name=resource_name))
        self.options.update(options)
        self.__resource = None
        self.__lock = threading.RLock()

    @property
    def resource(self):
        return self.__resource

    @property
    def lock(self):
        return self.__lock

    def __enter__(self):
        resource_name = self.options.get('resource_name')
        visa_library = QtCore.QSettings().value('visaLibrary', '@py')
        logging.info("opening resource: '%s' with options %s", resource_name, self.options)
        self.__resource = visa.ResourceManager(visa_library).open_resource(**self.options)
        return self

    def __exit__(self, *exc):
        logging.info("closing resource: '%s'", self.__resource.resource_name)
        self.__resource.close()
        self.__resource = None
        return False

class DeviceManager(object):

    __devices = OrderedDict()

    @classmethod
    def get(cls, key):
        if key not in cls.__devices:
            raise KeyError("key does not exist: '{}'".format(key))
        return cls.__devices.get(key)

    @classmethod
    def add(cls, key, value):
        if key in cls.__devices:
            raise KeyError("key already exists: '{}'".format(key))
        if value in cls.__devices.values():
            raise ValueError("value already exists: '{}'".format(value))
        return cls.__devices.setdefault(key, value)

    @classmethod
    def __len__(cls):
        return len(cls.__devices)

    @classmethod
    def values(cls):
        return cls.__devices.values()

    @classmethod
    def items(cls):
        return cls.__devices.items()

    @classmethod
    def resources(cls):
        for name, device in cls.__devices.items():
            yield name, device.options.get('resource_name')

class DeviceMixin:

    __devices = DeviceManager()

    @classmethod
    def devices(cls):
        return cls.__devices
