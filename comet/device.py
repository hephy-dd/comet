from .driver import Driver
from .collection import Collection
from .settings import SettingsManager

__all__ = ['DeviceManager', 'DeviceMixin']

class DeviceManager(Collection):
    """Device manager."""

    ValueType = Driver

    def load_settings(self):
        """Load resource settings."""
        settings = SettingsManager()
        resources = settings.get('resources') or {}
        for name, device in self.items():
            for key, value in resources.get(name, {}).items():
                if key == "resource_name":
                    device.resource.resource_name = value
                elif key == "visa_library":
                    device.resource.visa_library = value
                else:
                    device.resource.options[key] = value

    def sync_settings(self):
        """Syncronize settings."""
        settings = SettingsManager()
        resources = settings.get('resources') or {}
        for name, device in self.items():
            if name not in resources:
                resources[name] = {}
            resources[name]["resource_name"] = device.resource.resource_name
            resources[name]["visa_library"] = device.resource.visa_library
            for key, value in device.resource.options.items():
                resources[name][key] = value

    def resources(self):
        """Returns list of resource names for contained devices."""
        return {name: device.resource.resource_name for name, device in self.items()}

class DeviceMixin:
    """Mixin class to access global device manager."""

    __devices = DeviceManager()

    @property
    def devices(self):
        return self.__class__.__devices
