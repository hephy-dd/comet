from .component import Component, ComponentManager

__all__ = ['Device', 'DeviceManager']

class Device(Component):

    def __init__(self, name, resource, label=None):
        super().__init__(name, label)
        self.add_property('resource', resource)

    def write(self, message):
        with self.rlock:
            return self.resource.write(message)

    def read(self):
        with self.rlock:
            return self.resource.read()

    def query(self, message):
        with self.rlock:
            return self.resource.query(message)

    def write_bytes(self, message):
        with self.rlock:
            return self.resource.write_raw(message)

    def read_bytes(self, count):
        with self.rlock:
            return self.resource.read_bytes(count)

    def query_bytes(self, message, count):
        with self.rlock:
            self.write_bytes(message)
            return self.read_bytes(count)

class DeviceManager(ComponentManager):

    component_type = Device

    def __init__(self, resource_manager):
        super().__init__()
        self.add_property('resource_manager', resource_manager)

    def create_device(self, name, resource_name, device_type=None, label=None):
        device_type = device_type or self.component_type
        resource = self.resource_manager.open_resource(resource_name)
        device = device_type(name, resource, label)
        self.add_component(device)
