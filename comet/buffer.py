from collections import OrderedDict

from .component import Component, ComponentManager
from .metric import MetricManager

__all__ = ['Buffer', 'BufferManager']

class Buffer(Component):

    def __init__(self, name, label=None):
        super().__init__(name, label)
        self.add_property('metrics', MetricManager())
        self.__handlers = []
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def add_metric(self, name, type=float, unit=None, label=None):
        return self.metrics.create_metric(name, type, unit, label)

    def add_handler(self, handler):
        return self.__handlers.append(handler)

    def write(self, **values):
        record = OrderedDict()
        for metric in self.metrics:
            key = metric.name
            value = values[key]
            record[key] = metric.convert(value)
        self.__data.append(tuple(record.values()))
        for handler in self.__handlers:
            handler(**record)

class BufferManager(ComponentManager):

    component_type = Buffer

    def create_buffer(self, name, buffer_type=None, label=None):
        buffer_type = buffer_type or self.component_type
        buffer = buffer_type(name, label)
        return self.add_component(buffer)
