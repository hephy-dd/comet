import weakref
import logging

from PyQt5 import QtCore, QtWidgets

__all__ = []

class ElementStore:

    __elements = {}

    @classmethod
    def get(cls, id):
        return cls.__elements.get(id)

    @classmethod
    def add(cls, element):
        if element.id in cls.__elements:
            logging.debug("ID already exists: %s", element.id)
        cls.__elements[element.id] = element

def get(id):
    return ElementStore.get(id)

class Event:

    def __init__(self, target, **kwargs):
        self.__target = weakref.ref(target)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def target(self):
        return self.__target()

class Object:

    QtBaseClass = QtCore.QObject

    def __init__(self, id=None):
        self.__qt = self.QtBaseClass()
        self.id = id

    def get(self, id):
        return get(id)

    @property
    def qt(self):
        return self.__qt

    @property
    def id(self):
        return self.qt.objectName()

    @id.setter
    def id(self, id):
        self.qt.setObjectName(id)
        ElementStore.add(self)
