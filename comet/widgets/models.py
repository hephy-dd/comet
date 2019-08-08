from PyQt5 import QtCore, QtWidgets

class BufferTableModel(QtCore.QAbstractTableModel):
    """Table model for data buffers.

    >>> buff = comet.Buffer()
    >>> buff.addChannel('x')
    >>> buff.addChannel('y')
    >>> model = BufferTableModel()
    >>> model.setBuffer(buff)
    >>> view = QtWidgets.QTableView()
    >>> view.setModel(model)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__buffer = None
        self.__rowCount = 0
        self.__columnCount = 0
        self.__columnNames = []

    def buffer(self):
        """Returns buffer object."""
        return self.__buffer

    def setBuffer(self, buffer):
        """Set buffer for model."""
        self.__buffer = buffer
        self.__rowCount = buffer.size()
        self.__columnCount = len(buffer.keys())
        self.__columnNames = buffer.keys()
        self.__buffer.dataChanged.connect(self.__bufferChanged)
        self.__buffer.channelsChanged.connect(self.__channelsChanged)

    def __bufferChanged(self):
        """Is called if buffer content changed."""
        size = self.__buffer.size()
        count = size - self.__rowCount
        if size < self.__rowCount:
            self.removeRows(size, self.__rowCount, QtCore.QModelIndex())
        else:
            if count > 0:
                self.insertRows(self.__rowCount, count, QtCore.QModelIndex())
        self.__rowCount = size

    def __channelsChanged(self):
        """Is called if buffer channels changed."""
        self.__columnCount = len(buffer.keys())
        self.__columnNames = buffer.keys()

    def insertRows(self, row, count, parent):
        """Insert rows to model."""
        if count < 1 or row < 0 or row > self.__rowCount:
            return False
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent):
        """Remove rows to model."""
        if count < 1 or row < 0 or row > self.__rowCount:
            return False
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + count - 1)
        self.endRemoveRows()
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Returns model row count."""
        return self.__rowCount

    def columnCount(self, parent=QtCore.QModelIndex()):
        """Returns model column count."""
        return self.__columnCount

    def headerData(self, section, orientation, role):
        """Returns model header data for view."""
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__buffer.keys()[section]

    def data(self, index, role):
        """Returns model data for view."""
        if not index.isValid():
            return
        column = index.column()
        row = index.row()
        if role == QtCore.Qt.DisplayRole:
            return self.__buffer.data()[self.__columnNames[column]][row]
