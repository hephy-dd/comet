import threading
from contextlib import ContextDecorator

import visa

__all__ = ['Resource']

class Resource(ContextDecorator):

    def __init__(self, resource_name, visa_library='@py', **options):
        self.resource_name = resource_name
        self.visa_library = visa_library
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
