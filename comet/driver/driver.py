import weakref
import threading
import random
import time
from contextlib import ContextDecorator

__all__ = ['lock', 'Driver']

def lock(function):
    """Decorator function, locks decorated functions to a resource specific RLock."""
    def lock(obj, *args, **kwargs):
        with obj.resource.lock:
            return function(obj, *args, **kwargs)
    return lock

class Driver(ContextDecorator):
    """Base class for custom VISA instrument drivers.
    >>> class MyInstrument(comet.Driver):
    ...     @property
    ...     def voltage(self):
    ...         return float(self.resource.query(":VOLT?"))
    ...     @voltage.setter
    ...     def voltage(self, value):
    ...         self.resource.write(f":VOLT {value:.3f}; *OPC?")
    ...         self.resource.read()
    ...
    >>> with MyInstrument(Resource("GPIB0::15")) as instr:
    ...     instr.voltage = 42
    ...     print(instr.voltage)
    ...
    42.0
    """

    __instances = weakref.WeakKeyDictionary()

    def __init__(self, resource=None):
        self.__resource = resource

    @property
    def resource(self):
        return self.__resource

    def __get__(self, obj, cls):
        if self not in type(self).__instances:
            type(self).__instances[self] = type(self)(obj.resource)
        return type(self).__instances.get(self)

    def __enter__(self):
        self.resource.__enter__()
        return self

    def __exit__(self, *exc):
        self.resource.__exit__(*exc)
        return False
