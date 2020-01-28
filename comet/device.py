from .driver import Driver
from .collection import Collection

__all__ = ['DeviceManager', 'DeviceMixin']

class DeviceManager(Collection):
    """Device manager."""

    ValueType = Driver

    def resources(self):
        """Returns list of resource names for contained devices."""
        return {name: device.resource.resource_name for name, device in self.items()}

class DeviceMixin:
    """Mixin class to access global device manager."""

    __devices = DeviceManager()

    @property
    def devices(self):
        return self.__class__.__devices
