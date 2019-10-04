import threading
import logging
from collections import OrderedDict
from contextlib import ContextDecorator

import visa

__all__ = ['Device', 'DeviceManager', 'DeviceMixin']

class Device(ContextDecorator):
    """Base class for custom VISA devices.
    >>> class MyDevice(comet.Device):
    ...     def voltage(self):
    ...         return float(self.resource().query(':VOLT?'))
    ...     def setVoltage(self, value):
    ...         self.resource().query(':VOLT {:.3f}'.format(value))
    ...
    >>> with MyDevice('GPIB::15') as device:
    ...     device.setVoltage(42)
    ...     device.voltage()
    ...
    42.0
    """

    options = {}
    """Options passed on to VISA resource."""

    def __init__(self, resourceName, visaLibrary):
        self.__resourceName = resourceName
        self.__visaLibrary = visaLibrary
        self.__resource = None
        self.__lock = threading.RLock()

    def resourceName(self):
        return self.__resourceName

    def visaLibrary(self):
        return self.__visaLibrary

    def resource(self):
        return self.__resource

    def lock(self):
        return self.__lock

    def __enter__(self):
        rm = visa.ResourceManager(self.__visaLibrary)
        logging.info("opening resource: '%s' with options %s", self.__resourceName, self.options)
        self.__resource = rm.open_resource(self.__resourceName, **self.options)
        return self

    def __exit__(self, *exc):
        logging.info("closing resource: '%s'", self.__resourceName)
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
            yield name, device.resourceName()

class DeviceMixin(object):

    __devices = DeviceManager()

    @classmethod
    def devices(cls):
        return cls.__devices
