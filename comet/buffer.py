from threading import RLock
from collections import OrderedDict
from PyQt5 import QtCore

from .units import ureg

__all__ = ['Buffer']

class Channel(QtCore.QObject):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.__name = name
        self.__unitX = ureg.dimensionless
        self.__unitY = ureg.dimensionless
        self.__dataX = []
        self.__dataY = []
        self.__lock = RLock()

    def name(self):
        """Retruns channel name."""
        return self.__name

    def setName(self, name):
        """Set channel name."""
        self.__name = name

    def unitX(self):
        """Returns unit for X axis."""
        return self.__unitX

    def setUnitX(self, unit):
        """Set unit for X axis."""
        self.__unitX = unit

    def unitY(self):
        """Returns unit for Y axis."""
        return self.__unitY

    def setUnitY(self, unit):
        """Set unit for Y axis."""
        self.__unitY = unit

    def append(self, x, y):
        """Append data to channel."""
        x = x.to(self.__unitX)
        y = y.to(self.__unitY)
        with self.__lock:
            self.__dataX.append(x)
            self.__dataY.append(y)

    def __len__(self):
        """Returns size of channel content."""
        with self.__lock:
            return len(self.__dataX)

    def data(self):
        """Returns channel content."""
        with self.__lock:
            return self.__dataX, self.dataY

    def subsample(self, count):
        """Returns subsampled channel content."""
        with self.__lock:
            width = (len(self.__dataX)-1) / count
            return self.__dataX[::width], self.dataY[::width]

class Buffer(QtCore.QObject):
    """Buffer holding data channels."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__channels = OrderedDict()

    def addChannel(self, name):
        """Add data channel."""
        if name in self.__channels:
            raise KeyError("Key already exists: '{}'".format(name))
        channel = Channel(self)
        self.__channels[name] = channel
        return channel

    def channels(self):
        """Returns channel dictionary."""
        return self.__channels
