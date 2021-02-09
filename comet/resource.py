import threading
from contextlib import ContextDecorator

import pyvisa as visa

from .collection import Collection
from .settings import SettingsManager

__all__ = ['Resource', 'ResourceError', 'ResourceManager', 'ResourceMixin']

class ResourceError(Exception):

    def __init__(self, resource, exc):
        super().__init__(resource.resource_name, resource.visa_library, resource.options, exc)

    @property
    def resource_name(self):
        return self.args[0]

    @property
    def visa_library(self):
        return self.args[1]

    @property
    def options(self):
        return self.args[2]

    @property
    def exc(self):
        return self.args[3]

    def __str__(self):
        return f"{self.resource_name}: {self.exc}"

def lock_resource(f):
    def lock_resource(self, *args, **kwargs):
        with self.lock:
            return f(self, *args, **kwargs)
    return lock_resource

def resource_errors(f):
    def resource_errors(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except (visa.Error, ConnectionError) as exc:
            raise ResourceError(self, exc)
    return resource_errors

class Resource(ContextDecorator):

    def __init__(self, resource_name, visa_library=None, **options):
        super().__init__()
        self.resource_name = resource_name
        self.visa_library = visa_library or '@py'
        self.options = options
        self.instance = None
        self.lock = threading.RLock()

    @lock_resource
    @resource_errors
    def __enter__(self):
        rm = visa.ResourceManager(self.visa_library)
        if self.instance not in rm.list_opened_resources():
            self.instance = rm.open_resource(self.resource_name, **self.options)
        return self

    @lock_resource
    def __exit__(self, *exc):
        if self.instance:
            self.instance.close()
            self.instance = None
        return False

    @lock_resource
    @resource_errors
    def read(self, *args, **kwargs):
        return self.instance.read(*args, **kwargs)

    @lock_resource
    @resource_errors
    def read_bytes(self, *args, **kwargs):
        return self.instance.read_bytes(*args, **kwargs)

    @lock_resource
    @resource_errors
    def read_raw(self, *args, **kwargs):
        return self.instance.read_raw(*args, **kwargs)

    @lock_resource
    @resource_errors
    def write(self, *args, **kwargs):
        return self.instance.write(*args, **kwargs)

    @lock_resource
    @resource_errors
    def write_bytes(self, *args, **kwargs):
        return self.instance.write_bytes(*args, **kwargs)

    @lock_resource
    @resource_errors
    def write_raw(self, *args, **kwargs):
        return self.instance.write_raw(*args, **kwargs)

    @lock_resource
    @resource_errors
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
