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
        """Add element to global element store."""
        if element.id in cls.__elements:
            logging.debug("ID already exists: %s", element.id)
        cls.__elements[element.id] = element

    @classmethod
    def remove(cls, element):
        """Remove element from global element store by ID."""
        if element.id in cls.__elements:
            del cls.__elements[element.id]

def get(id):
    return ElementStore.get(id)

def callback(method):
    def callback(*args, **kwargs):
        return method(*args, **kwargs)
    return callback

class Event:

    def __init__(self, target, **kwargs):
        self.__target = weakref.ref(target)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def target(self):
        return self.__target()

class Base:
    """Case class for any UI elements."""

    QtBaseClass = object

    def __init__(self, *args, **kwargs):
        self.__qt = self.QtBaseClass(*args, **kwargs)

    @property
    def qt(self):
        """Returns underlying Qt instance."""
        return self.__qt

    def get(self, id):
        """Returns UI element by ID or None if not found."""
        return get(id)

class Object(Base):
    """Base class for UI elements to be referenced by ID."""

    QtBaseClass = QtCore.QObject

    def __init__(self, *args, id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id

    @property
    def id(self):
        return self.qt.objectName() or None

    @id.setter
    def id(self, id):
        if id is None:
            self.qt.setObjectName("")
            ElementStore.remove(self)
        else:
            self.qt.setObjectName(format(id))
            ElementStore.add(self)
