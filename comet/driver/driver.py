from abc import ABC, abstractmethod


class Driver(ABC):

    def __init__(self, resource):
        self.resource = resource

