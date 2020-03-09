import weakref
import threading
import random
import time
from contextlib import ContextDecorator

from .resource import Resource

__all__ = ['lock', 'Driver', 'Action', 'Property']

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

    def __init__(self, resource, **kwargs):
        if isinstance(resource, str):
            self.__resource = Resource(resource_name=resource, **kwargs)
        elif isinstance(resource, Resource):
            self.__resource = resource
        else:
            raise ValueError(f"invalid resource {resource!r}")

    @property
    def resource(self):
        return self.__resource

    def __setattr__(self, name, value):
        """Prevent overriding driver attributes."""
        if name in self.__dict__ and isinstance(self.__dict__.get(name), Driver):
            raise AttributeError("can't set attribute")
        super().__setattr__(name, value)

    def __enter__(self):
        self.resource.__enter__()
        return self

    def __exit__(self, *exc):
        self.resource.__exit__(*exc)
        return False

class Action:
    def __init__(self):
        pass
    def __call__(self, method):
        def action(*args, **kwargs):
            return method(*args, **kwargs)
        return action

def Property(*, values=None, minimum=None, maximum=None, keys=None):
    _values = values
    _min = minimum
    _max = maximum
    _keys = keys

    def get_transform(value):
        if _values is not None:
            if isinstance(_values, dict):
                if value not in _values.values():
                    values = tuple(_values.values())
                    raise ValueError(f"{value!r} not in {values}")
                value = {v: k for k, v in _values.items()}[value]
            else:
                if value not in _values:
                    values = tuple(_values)
                    raise ValueError(f"{value!r} not in {values}")
        if _min is not None:
            if value < _min:
                raise ValueError(value)
        if _max is not None:
            if value > _max:
                raise ValueError(value)
        return value

    def set_transform(value):
        if _values is not None:
            if isinstance(_values, dict):
                if value not in _values.keys():
                    values = tuple(_values.keys())
                    raise ValueError(f"{value!r} not in {values}")
                value = _values[value]
            else:
                if value not in _values:
                    values = tuple(_values)
                    raise ValueError(f"{value!r} not in {values}")
        if _min is not None:
            if value < _min:
                raise ValueError(value)
        if _max is not None:
            if value > _max:
                raise ValueError(value)
        return value

    class _PropertyProxy:
        def __init__(self, obj, fget, fset, doc=None):
            self.obj = obj
            self.fget = fget
            self.fset = fset
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __len__(self):
            return len(_keys)

        def __iter__(self):
            return iter(_keys)

        def __getitem__(self, key):
            if key not in _keys:
                raise KeyError(key)
            value = self.fget(self.obj, key)
            return get_transform(value)

        def __setitem__(self, key, value):
            if key not in _keys:
                raise KeyError(key)
            value = set_transform(value)
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(self.obj, key, value)

    class _Property:
        def __init__(self, fget=None, fset=None, doc=None):
            self.fget = fget
            self.fset = fset
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            if _keys is not None:
                return _PropertyProxy(obj, self.fget, self.fset, self.__doc__)
            value = self.fget(obj)
            return get_transform(value)

        def __set__(self, obj, value):
            value = set_transform(value)
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(obj, value)

        def getter(self, fget):
            return type(self)(fget, self.fset, self.__doc__)

        def setter(self, fset):
            return type(self)(self.fget, fset, self.__doc__)

    return _Property
