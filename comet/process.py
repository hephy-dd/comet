from qutie.worker import Worker
from qutie.worker import StopRequest

from .resource import ResourceMixin
from .settings import SettingsMixin
from .collection import Collection

__all__ = ['Process', 'StopRequest', 'ProcessManager', 'ProcessMixin']

class Process(Worker, ResourceMixin, SettingsMixin):
    """Process inheriting from qutie.Worker."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProcessManager(Collection):
    """Process manager."""

    ValueType = Process

    def stop(self):
        """Stop all registered processes."""
        for process in self.values():
            process.stop()

    def join(self):
        """Join all registered processes."""
        for process in self.values():
            process.join()

class ProcessMixin:
    """Mixin class to access global process manager."""

    __processes = ProcessManager()

    @property
    def processes(self):
        return type(self).__processes
