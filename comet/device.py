import threading
import weakref
import logging
from contextlib import ContextDecorator

from PyQt5 import QtCore
import visa

import comet
from .collection import Collection

__all__ = ['lock_resource', 'Device', 'DeviceManager', 'DeviceMixin']

def lock_resource(method):
    """Resource lock decorator."""
    def f(self, *args, **kwargs):
        with self.lock:
            print(">>>>> ON")
            r = method(self, *args, **kwargs)
            print(r)
            print("<<<<< OFF")
            return r
    return f

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
        if isinstance(parent, Node):
            prefix = f'{parent.prefix}{prefix}'
        self.__prefix = prefix

    @property
    def prefix(self):
        return self.__prefix

    @property
    def options(self):
        return self.__parent.options

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
    ...         return float(self.resource.query(':VOLT?'))
    ...     @voltage.setter
    ...     def voltage(self, value):
    ...         self.resource.write(f':VOLT {value:.3f}; *OPC?')
    ...         self.resource.read()
    ...
    >>> with MyDevice('GPIB::15') as device:
    ...     device.voltage = 42
    ...     print(device.voltage)
    ...
    42.0
    """

    options = {}
    """Default options passed on to VISA resource."""

    __resource_locks = {}

    def __init__(self, resource_name, **options):
        options.update(dict(resource_name=resource_name))
        self.options.update(options)
        self.__resource = None
        self.__context_lock = threading.Lock()

    @property
    def resource(self):
        return self.__resource

    @property
    def lock(self):
        resource_name = self.options.get('resource_name')
        return self.__class__.__resource_locks.setdefault(resource_name, threading.RLock())

    def __enter__(self):
        self.__context_lock.acquire()
        resource_name = self.options.get('resource_name')
        visa_library = comet.app().settings.get('visaLibrary', '@py') if comet.app() else '@py' # TODO!
        logging.info("opening resource: '%s' with options %s", resource_name, self.options)
        self.__resource = visa.ResourceManager(visa_library).open_resource(**self.options)
        return self

    def __exit__(self, *exc):
        logging.info("closing resource: '%s'", self.__resource.resource_name)
        self.__resource.close()
        self.__resource = None
        self.__context_lock.release()
        return False

class DeviceManager(Collection):

    ValueType = Device

    def resources(self):
        return {name: device.options.get('resource_name') for name, device in self.items()}

class DeviceMixin:

    __devices = DeviceManager()

    @property
    def devices(self):
        return self.__class__.__devices
