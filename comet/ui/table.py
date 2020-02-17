from PyQt5 import QtCore, QtGui, QtWidgets

from .core import Base, callback
from .widget import Widget

__all__ = ['Table']

class Table(Widget):

    QtBaseClass = QtWidgets.QTableWidget

    def __init__(self, header=[], rows=[], stretch=False, changed=None, entered=None, **kwargs):
        super().__init__(**kwargs)
        self.header = header
        for row in rows:
            self.append(row)
        self.stretch = stretch
        self.changed = changed
        self.entered = entered
        self.qt.itemChanged.connect(self.__changed)
        self.qt.itemActivated.connect(self.__entered)
        self.qt.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.qt.horizontalHeader().setHighlightSections(False)

    @callback
    def __changed(self, item):
        if self.changed is not None:
            item = item.data(item.UserType)
            if item is not None:
                self.changed(item)

    @callback
    def __entered(self, item):
        if self.entered is not None:
            item = item.data(item.UserType)
            if item is not None:
                self.entered(item)

    @property
    def header(self):
        return self.qt.horizontalHeaderLabels()

    @header.setter
    def header(self, items):
        self.qt.setColumnCount(len(items))
        self.qt.setHorizontalHeaderLabels(items)

    def append(self, items):
        row = self.qt.rowCount()
        self.qt.setRowCount(self.qt.rowCount() + 1)
        self.insert(row, items)

    def insert(self, row, items):
        for column, item in enumerate(items):
            if not isinstance(item, TableItem):
                item = TableItem(value=item)
            self.qt.setItem(row, column, item.qt)

    def clear(self):
        self.qt.clearContents()

    @property
    def stretch(self):
        return self.qt.horizontalHeader().stretchLastSection()

    @stretch.setter
    def stretch(self, state):
        self.qt.horizontalHeader().setStretchLastSection(state)

    def fit(self):
        self.qt.resizeColumnsToContents()
        self.qt.resizeRowsToContents()

    def __getitem__(self, row):
        items = []
        for column in range(self.qt.columnCount()):
            item = self.qt.item(row, column)
            items.append(item.data(item.UserType) if item is not None else item)
        return items

    def __setitem__(self, row, items):
        self.qt.removeRow(row)
        self.qt.insertRow(row)
        for column, item in enumerate(items):
            if not isinstance(item, TableItem):
                item = TableItem(value=item)
            self.qt.setItem(row, column, item.qt)

    def __len__(self):
        return self.qt.rowCount()

    def __iter__(self):
        rows = []
        for row in range(self.qt.rowCount()):
            rows.append(self[row])
        return iter(rows)

class TableItem(Base):

    QtBaseClass = QtWidgets.QTableWidgetItem

    def __init__(self, value=None, color=None, background=None, enabled=True, readonly=True, checked=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setData(self.qt.UserType, self)
        self.__default_foreground = self.qt.foreground()
        self.__default_background = self.qt.background()
        self.value = value
        self.color = color
        self.background = background
        self.enabled = enabled
        self.readonly = readonly
        self.checked = checked

    @property
    def value(self):
        return self.qt.data(self.qt.Type)

    @value.setter
    def value(self, value):
        return self.qt.setData(self.qt.Type, value)

    @property
    def color(self):
        return self.qt.foreground().color().name()

    @color.setter
    def color(self, color):
        if color is None:
            brush = self.__default_foreground
        else:
            brush = self.qt.foreground()
            brush.setColor(QtGui.QColor(color))
        self.qt.setForeground(brush)

    @property
    def background(self):
        return self.qt.background().color().name()

    @background.setter
    def background(self, color):
        if color is None:
            brush = self.__default_background
        else:
            brush = self.qt.background()
            brush.setStyle(QtCore.Qt.SolidPattern)
            brush.setColor(QtGui.QColor(color))
        self.qt.setBackground(brush)

    @property
    def enabled(self):
        return bool(self.qt.flags() & QtCore.Qt.ItemIsEnabled)

    @enabled.setter
    def enabled(self, state):
        if state:
            self.qt.setFlags(self.qt.flags() | QtCore.Qt.ItemIsEnabled)
        else:
            self.qt.setFlags(self.qt.flags() & ~QtCore.Qt.ItemIsEnabled)

    @property
    def readonly(self):
        return bool(self.qt.flags() & QtCore.Qt.ItemIsEditable)

    @readonly.setter
    def readonly(self, state):
        if state:
            self.qt.setFlags(self.qt.flags() & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable))
        else:
            self.qt.setFlags(self.qt.flags() | (QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable))

    @property
    def checked(self):
        return self.qt.checkState() == QtCore.Qt.Checked

    @checked.setter
    def checked(self, state):
        if state is None:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
            self.qt.setFlags(flags)
        else:
            flags = self.qt.flags() | QtCore.Qt.ItemIsUserCheckable
            self.qt.setFlags(flags)
            self.qt.setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)
