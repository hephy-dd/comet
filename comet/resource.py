import threading
from contextlib import ContextDecorator

import visa

from .collection import Collection
from .settings import SettingsManager

__all__ = ['Resource', 'ResourceManager', 'ResourceMixin']

class Resource(ContextDecorator):

    def __init__(self, resource_name, visa_library=None, **options):
        self.resource_name = resource_name
        self.visa_library = visa_library or '@py'
        self.options = options
        self.instance = None
        self.lock = threading.RLock()

    def __enter__(self):
        with self.lock:
            rm = visa.ResourceManager(self.visa_library)
            if self.instance not in rm.list_opened_resources():
                self.instance = rm.open_resource(self.resource_name, **self.options)
            return self

    def __exit__(self, *exc):
        with self.lock:
            if self.instance:
                self.instance.close()
                self.instance = None
            return False

    def read(self, *args, **kwargs):
        return self.instance.read(*args, **kwargs)

    def read_bytes(self, *args, **kwargs):
        return self.instance.read_bytes(*args, **kwargs)

    def read_raw(self, *args, **kwargs):
        return self.instance.read_raw(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.instance.write(*args, **kwargs)

    def write_bytes(self, *args, **kwargs):
        return self.instance.write_bytes(*args, **kwargs)

    def write_raw(self, *args, **kwargs):
        return self.instance.write_raw(*args, **kwargs)

    def query(self, *args, **kwargs):
        return self.instance.query(*args, **kwargs)

class ResourceManager(Collection):
    """Resource manager."""

    ValueType = Resource

    def load_settings(self):
        """Load resource settings."""
        settings = SettingsManager()
        resources = settings.get('resources') or {}
        for name, resource in self.items():
            for key, value in resources.get(name, {}).items():
                if key == "resource_name":
                    resource.resource_name = value
                elif key == "visa_library":
                    resource.visa_library = value
                else:
                    resource.options[key] = value

    def sync_settings(self):
        """Syncronize settings."""
        settings = SettingsManager()
        resources = settings.get('resources') or {}
        for name, resource in self.items():
            if name not in resources:
                resources[name] = {}
            resources[name]["resource_name"] = resource.resource_name
            resources[name]["visa_library"] = resource.visa_library
            for key, value in resource.options.items():
                resources[name][key] = value
        settings['resources'] = resources

    def resources(self):
        """Returns list of resource names for contained devices."""
        return {name: device.resource.resource_name for name, device in self.items()}

class ResourceMixin:
    """Mixin class to access global resource manager."""

    __resources = ResourceManager()

    @property
    def resources(self):
        return self.__class__.__resources
