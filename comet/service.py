from .component import Component, ComponentManager

__all__ = ['Service', 'ServiceManager']

class Service(Component):

    def __init__(self, name, label=None):
        super().__init__(name, label)

class ServiceManager(ComponentManager):

    component_type = Service

    def create_process(self, name, service_type=None, label=None):
        service_type = service_type or self.component_type
        service = service_type(name, label)
        return self.add_component(service)
