import weakref
import threading
import random, time
from contextlib import ContextDecorator

import visa

__all__ = ['lock', 'opc_wait', 'opc_poll', 'Resource', 'Driver']

def lock(function):
    """Decorator function, locks decorated functions to a resource specific
    RLock."""
    def lock(obj, *args, **kwargs):
        with obj.resource.lock:
            return function(obj, *args, **kwargs)
    return lock

def opc_wait(function):
    """Decorator function, locks the resource and waits for `*OPC?` after
    function execution."""
    @lock
    def opc_wait(obj, *args, **kwargs):
        result = function(obj, *args, **kwargs)
        obj.resource.query("*OPC?")
        return result
    return opc_wait

def opc_poll(function, interval=.250, retries=40):
    """Decorator function, locks the resource, writes `*CLS` and `*OPC` before
    the function call and polls after function execution for `*ESR?` bit 0 to be
    set."""
    @lock
    def opc_poll(obj, *args, **kwargs):
        obj.resource.write("*CLS")
        obj.resource.write("*OPC")
        result = function(obj, *args, **kwargs)
        for i in range(retries):
            if 1 == int(obj.resource.query("*ESR?")) & 0x1:
                return result
            time.sleep(interval)
        raise RuntimeError("failed to poll for ESR")
    return opc_poll

class Resource:

    def __init__(self, resource_name, visa_library='@py', **options):
        self.resource_name = resource_name
        self.visa_library = visa_library
        self.options = options
        self.instance = None
        self.lock = threading.RLock()

    def __enter__(self):
        with self.lock:
            rm = visa.ResourceManager(self.visa_library)
            if self.instance not in rm.list_opened_resources():
                self.instance = rm.open_resource(self.resource_name, **self.options)
            return self

    def __exit__(self, *exc):
        with self.lock:
            if self.instance:
                self.instance.close()
                self.instance = None
            return False

    def read(self, *args, **kwargs):
        return self.instance.read(*args, **kwargs)

    def read_bytes(self, *args, **kwargs):
        return self.instance.read_bytes(*args, **kwargs)

    def read_raw(self, *args, **kwargs):
        return self.instance.read_raw(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.instance.write(*args, **kwargs)

    def write_bytes(self, *args, **kwargs):
        return self.instance.write_bytes(*args, **kwargs)

    def write_raw(self, *args, **kwargs):
        return self.instance.write_raw(*args, **kwargs)

    def query(self, *args, **kwargs):
        return self.instance.query(*args, **kwargs)

class Driver:
    """Base class for custom VISA instrument drivers.
    >>> class MyDevice(comet.Driver):
    ...     @property
    ...     def voltage(self):
    ...         return float(self.resource.query(":VOLT?"))
    ...     @voltage.setter
    ...     def voltage(self, value):
    ...         self.resource.write(f":VOLT {value:.3f}; *OPC?")
    ...         self.resource.read()
    ...
    >>> with MyDevice(Resource("GPIB0::15")) as device:
    ...     device.voltage = 42
    ...     print(device.voltage)
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
