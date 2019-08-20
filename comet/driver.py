"""Module `comet.driver` provides class `Driver` to be inherited by custom
device driver classes.
"""

import inspect
import logging
import threading
import os

import visa

from .utilities import make_path

__all__ = ['Driver']

class Driver(object):
    """Base class for custom device drivers.

    >>> class MyDriver(comet.Driver):
    ...     def voltage(self):
    ...         return float(self.transport.query(':VOLT?'))
    ...     def setVoltage(self, value):
    ...         self.transport.query(':VOLT {:.3f}'.format(value))
    ...
    >>> with MyDriver('GPIB::15') as device:
    ...     device.setVoltage(42)
    ...     device.voltage()
    ...
    42.0
    """

    readTermination = '\r'

    def __init__(self, address, visaLibrary=None):
        self.__address = address
        self.__visaLibrary = visaLibrary
        self.__resource = None
        self.__lock = threading.RLock()

    def resource(self):
        return self.__resource

    def lock(self):
        return self.__lock

    def open(self):
        rm = visa.ResourceManager(self.__visaLibrary)
        options = dict(
            read_termination=self.readTermination,
        )
        self.__resource = rm.open_resource(self.__address, **options)

    def close(self):
        self.__resource.close()
        self.__resource = None

    def isOpen(self):
        return self.__resource is not None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
