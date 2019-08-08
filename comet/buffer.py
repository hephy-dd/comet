import threading
from collections import OrderedDict

from PyQt5 import QtCore, QtWidgets

from .channel import Channel

class Buffer(QtCore.QObject):

    dataChanged = QtCore.pyqtSignal()
    """Emitted when data is appended to the buffer."""

    channelsChanged = QtCore.pyqtSignal()
    """Emitted when new channels are added."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__lock = threading.RLock()
        self.__channels = OrderedDict()
        self.__size = 0

    def addChannel(self, name):
        with self.__lock:
            channel = Channel(self)
            channel.resize(self.__size)
            self.__channels[name] = channel
        self.channelsChanged.emit()

    def keys(self):
        return list(self.__channels.keys())

    def data(self):
        """Returns snapshot of buffer channels."""
        data = OrderedDict()
        with self.__lock:
            for name, channel in self.__channels.items():
                data[name] = channel.data().copy() # shallow copy
        return data

    def append(self, data):
        """Append values to buffer channels."""
        with self.__lock:
            for name, channel in self.__channels.items():
                channel.append(data.get(name))
            self.__size += 1
            self.dataChanged.emit()

    def clear(self):
        """Clear all channels."""
        with self.__lock:
            for name, channel in self.__channels.items():
                channel.clear()
            self.__size = 0
        self.dataChanged.emit()

    def size(self):
        """Returns current size of buffer."""
        return self.__size
