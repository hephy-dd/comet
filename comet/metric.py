from .component import Component, ComponentManager

__all__ = ['Metric', 'MetricManager']

class Metric(Component):

    def __init__(self, name, type=float, unit=None, label=None):
        super().__init__(name, label)
        self.add_property('type', type)
        self.add_property('unit', unit)

    def convert(self, value):
        return self.type(value)

class MetricManager(ComponentManager):

    component_type = Metric

    def create_metric(self, name, type, unit=None, label=None):
        metric = self.component_type(name, type, unit, label)
        return self.add_component(metric)
