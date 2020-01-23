import weakref
import threading
import random, time
from contextlib import ContextDecorator

import visa

__all__ = ['lock', 'opc_wait', 'opc_poll', 'Resource', 'Driver']

def lock(function):
    def lock(obj, *args, **kwargs):
        with obj.resource.lock:
            return function(obj, *args, **kwargs)
    return lock

def opc_wait(function):
    def opc_wait(obj, *args, **kwargs):
        result = function(obj, *args, **kwargs)
        obj.resource.query("*OPC?")
        return result
    return opc_wait

def opc_poll(function, interval=.250, retries=40):
    def opc_poll(obj, *args, **kwargs):
        obj.resource.write("*CLS")
        obj.resource.write("*OPC")
        result = function(obj, *args, **kwargs)
        for i in range(retries):
            if "1" == obj.resource.query("*ESR?"):
                return result
            time.sleep(interval)
        raise RuntimeError("failed to poll for ESR")
    return opc_poll

class Resource:

    visa_library = '@py'

    def __init__(self, resource_name, **options):
        self.options = options
        self.options.update(dict(resource_name=resource_name))
        self.instance = None
        self.lock = threading.RLock()

    def open(self):
        with self.lock:
            rm = visa.ResourceManager(self.visa_library)
            resource_name = self.options.get('resource_name')
            if resource_name not in map(lambda res: res.resource_name, rm.list_opened_resources()):
                self.instance = rm.open_resource(**self.options)

    def close(self):
        with self.lock:
            if self.instance:
                self.instance.close()

    def write(self, message):
        return self.instance.write(message)

    def query(self, message):
        return self.instance.query(message)

    def read(self):
        return self.instance.read()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc):
        self.close()
        return False

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
        self.resource.open()
        return self

    def __exit__(self, *exc):
        self.resource.close()
        return False
