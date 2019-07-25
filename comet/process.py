from .component import Component, ComponentManager

__all__ = ['Process', 'ProcessManager']

class Process(Component):

    def __init__(self, name, label=None):
        super().__init__(name, label)

class ProcessManager(ComponentManager):

    component_type = Process

    def create_process(self, name, process_type=None, label=None):
        process_type = process_type or self.component_type
        process = process_type(name, label)
        return self.add_component(process)
