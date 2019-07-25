from .component import Component, ComponentManager

__all__ = ['Parameter', 'ParameterManager']

class Parameter(Component):

    def __init__(self, name, type, default, group=None, minimum=None, maximum=None, precision=None, unit=None, label=None):
        super().__init__(name, label)
        self.add_property('type', type)
        self.add_property('value', default)
        self.add_property('group', group)
        self.add_property('unit', unit)
        self.add_property('minimum', minimum)
        self.add_property('maximum', maximum)
        self.add_property('precision', precision)

    def convert(self, value):
        return self.type(value)

class ParameterManager(ComponentManager):

    component_type = Parameter

    def create_parameter(self, name, type, default, group=None, minimum=None, maximum=None, precision=None, unit=None, label=None):
        parameter = self.component_type(name, type, default, group, minimum, maximum, precision, unit, label)
        return self.add_component(parameter)

    def by_group(self, group):
        return tuple(filter(lambda parameter: parameter.group == group, self))
