import threading

from PyQt5 import QtCore, QtWidgets

__all__ = ['Channel']

class Channel(QtCore.QObject):
    """Generic data channel, used by class `Buffer`."""

    type = float
    """Channel data type."""

    def __init__(self, name, size=0, parent=None):
        super().__init__(parent)
        self.__lock = threading.RLock()
        self.__name = name
        self.__label = None
        self.__data = [self.type() for _ in range(size)]

    def name(self):
        return self.__name

    def label(self):
        return self.__label

    def setLabel(self, label):
        self.__label = label

    def data(self, size=None):
        """Returns channel content."""
        return self.__data if size is None else self.__data[-size:]

    def append(self, value):
        with self.__lock:
            self.__data.append(self.type(value))

    def clear(self):
        with self.__lock:
            self.__data.clear()

    def size(self):
        """Returns current size of channel."""
        return len(self.__data)
