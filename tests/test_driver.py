import unittest
import random

from comet.driver import Driver


class Resource:

    def __init__(self):
        self.buffer = []

    def read(self):
        return self.buffer.pop(0)

    def write(self, message):
        self.buffer.append(message)

    def query(self, message):
        self.write(message)
        return self.read()


class BaseDriverTest(unittest.TestCase):

    driver_cls = None

    def setUp(self):
        self.resource = Resource()
        self.driver = self.driver_cls(self.resource)


class DriverTest(unittest.TestCase):

    pass
