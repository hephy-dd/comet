import pyvisa

from .component import Component
from .parameter import ParameterManager
from .device import DeviceManager
from .buffer import BufferManager
from .process import ProcessManager
from .service import ServiceManager

__all__ = ['Application']

class Application(Component):

    visa_library = '@sim'

    def __init__(self, name, label=None):
        super().__init__(name, label)
        resource_manager = pyvisa.ResourceManager(self.visa_library)
        self.add_event('on_begin')
        self.add_event('on_finished')
        self.add_property('parameters', ParameterManager())
        self.add_property('devices', DeviceManager(resource_manager))
        self.add_property('buffers', BufferManager())
        self.add_property('processes', ProcessManager())
        self.add_property('services', ServiceManager())

    def add_parameter(self, name, type, default, group=None, minimum=None, maximum=None, precision=None, unit=None, label=None):
        self.parameters.create_parameter(name, type, default, group, minimum, maximum, precision, unit, label)

    def add_device(self, name, resource_name, device_type=None, label=None):
        return self.devices.create_device(name, resource_name, device_type, label)

    def add_buffer(self, name, buffer_type=None, label=None):
        return self.buffers.create_buffer(name, buffer_type, label)

    def add_process(self, name, process_type=None, label=None):
        return self.processes.create_process(name, process_type, label)

    def add_service(self, name, service_type=None, label=None):
        return self.services.create_service(name, service_type, label)

    def code(self):
        pass

    def run(self):
        self.on_begin.emit()
        self.code()
        self.on_finished.emit()
