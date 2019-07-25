from collections import OrderedDict
from threading import RLock

from .utilities import make_label
from .event import Event

__all__ = ['Component', 'ComponentManager']

class __Component(object):

    def __init__(self):
        super().__init__()
        self.__properties = OrderedDict()
        self.add_property('rlock', RLock())

    def add_property(self, name, value, access='g', doc=None):
        def getter(self):
            return self.__properties[name]
        def setter(self, value):
            self.__properties[name] = value
        def deleter(self, value):
            del self.__properties[name]
        kwargs = {'doc': doc}
        if 'g' in access:
            kwargs['fget'] = getter
        if 's' in access:
            kwargs['fset'] = getter
        if 'd' in access:
            kwargs['fdel'] = deleter
        setattr(self.__class__, name, property(**kwargs))
        self.__properties[name] = value

    def add_event(self, name):
        self.add_property(name, Event())

class Component(__Component):

    def __init__(self, name, label=None):
        super().__init__()
        self.add_property('name', name)
        label = label or make_label(name)
        self.add_property('label', label, access='gs')

class ComponentManager(__Component):

    component_type = Component

    def __init__(self):
        super().__init__()
        self.__components = OrderedDict()
        self.add_event('on_component_added')

    def add_component(self, component):
        if not isinstance(component, self.component_type):
            raise TypeError("Component must be inherited from: '{}'".format(self.component_type.__class__.__name__))
        name = component.name
        if name in self.__components:
            raise KeyError("Component already exists: '{}'".format(name))
        self.__components[name] = component
        self.on_component_added.emit()
        return component

    def get(self, name):
        if name not in self.__components:
            raise KeyError("No such component: '{}'".format(name))
        return self.__components.get(name)

    def names(self):
        return tuple(self.__components.keys())

    def __iter__(self):
        return iter(self.__components.values())
