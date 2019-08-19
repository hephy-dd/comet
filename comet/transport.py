"""Generic transport layers."""

import visa

from .settings import Settings

__all__ = ['Transport', 'Visa']

class Transport(object):

    def __init__(self, address, visaLibrary=None):
        self.__address = address
        self.__resource = None
        self.visaLibrary = visaLibrary or Settings().visaLibrary()

    def resource(self):
        return self.__resource

    def open(self):
        rm = visa.ResourceManager(self.visaLibrary)
        self.__resource = rm.open_resource(self.__address)

    def close(self):
        self.__resource.close()

    def read(self, *args, **kwargs):
        return self.__resource.read(*args, **kwargs)

    def read_bytes(self, count, *args, **kwargs):
        return self.__resource.read_bytes(count, *args, **kwargs)

    def write(self, message, *args, **kwargs):
        return self.__resource.write(message, *args, **kwargs)

    def write_raw(self, message, *args, **kwargs):
        return self.__resource.write_raw(message, *args, **kwargs)

    def query(self, message, *args, **kwargs):
        return self.__resource.query(message, *args, **kwargs)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

class Visa(Transport):

    pass
