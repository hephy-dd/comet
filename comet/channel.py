from PyQt5 import QtCore, QtWidgets

__all__ = ['Channel']

class Channel(QtCore.QObject):
    """Generic data channel, used by `Buffer`."""

    defaultValue = None

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.__name = name
        self.__data = []

    def name(self):
        return self.__name

    def data(self):
        """Returns channel content."""
        return self.__data

    def append(self, value):
        self.__data.append(value)

    def resize(self, size):
        self.__data.extend([self.defaultValue for _ in range(size)])

    def clear(self):
        self.__data.clear()

    def size(self):
        """Returns current size of channel."""
        return len(self.__data)
