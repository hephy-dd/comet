import threading
from collections import OrderedDict

from PyQt5 import QtCore, QtWidgets

from .channel import Channel

class Buffer(QtCore.QObject):

    dataChanged = QtCore.pyqtSignal()
    """Emitted when data is appended to the buffer."""

    cleared = QtCore.pyqtSignal()

    channelsChanged = QtCore.pyqtSignal()
    """Emitted when new channels are added."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__lock = threading.RLock()
        self.__channels = OrderedDict()
        self.__size = 0

    def addChannel(self, name, label=None):
        """Add channel to buffer."""
        with self.__lock:
            channel = Channel(name, self.__size, self)
            channel.setLabel(label)
            self.__channels[name] = channel
        self.channelsChanged.emit()

    def keys(self):
        return list(self.__channels.keys())

    def data(self, size=None):
        """Returns buffer channels, limit size using param `size`."""
        data = OrderedDict()
        with self.__lock:
            for name, channel in self.__channels.items():
                data[name] = channel.data(size)
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
        self.cleared.emit()
        self.dataChanged.emit()

    def size(self):
        """Returns current size of buffer."""
        return self.__size
