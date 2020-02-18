from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .core import Base, callback
from .widget import Widget

__all__ = ['Tree']

class Tree(Widget):

    QtBaseClass = QtWidgets.QTreeWidget

    def __init__(self, header=[], **kwargs):
        super().__init__(**kwargs)
        self.header = header

    @property
    def header(self):
        return self.qt.headerLabels()

    @header.setter
    def header(self, items):
        self.qt.setColumnCount(len(items))
        self.qt.setHeaderLabels(items)

    def append(self, item):
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.addTopLevelItem(item.qt)
        item.expanded = True
        return item

    def insert(self, index, item):
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.insertTopLevelItem(index, item.qt)
        item.expanded = True
        return item

    def clear(self):
        self.qt.clear()

    @property
    def stretch(self):
        return self.qt.header().stretchLastSection()

    @stretch.setter
    def stretch(self, state):
        self.qt.header().setStretchLastSection(state)

    def fit(self):
        for column in range(self.qt.columnCount()):
            self.qt.resizeColumnToContents(column)

    def __getitem__(self, index):
        item = self.qt.topLevelItem(index)
        return item.data(0, item.UserType)

    def __setitem__(self, index, items):
        self.qt.removeRow(row)
        self.qt.insertRow(row)
        for column, item in enumerate(items):
            if not isinstance(item, TableItem):
                item = TableItem(value=item)
            self.qt.setItem(row, column, item.qt)

    def __len__(self):
        return self.qt.topLevelItemCount()

    def __iter__(self):
        items = []
        for index in range(self.qt.topLevelItemCount()):
            items.append(self[index])
        return iter(items)

class TreeItem(Base):

    QtBaseClass = QtWidgets.QTreeWidgetItem

    def __init__(self, values, **kwargs):
        super().__init__(**kwargs)
        self.qt._default_foreground = self.qt.foreground(0)
        self.qt._default_background = self.qt.background(0)
        for column, value in enumerate(values):
            self.qt.setData(column, self.qt.Type, value)
            self.qt.setData(column, self.qt.UserType, self)

    @property
    def children(self):
        items = []
        for index in range(self.qt.childCount()):
            item = self.qt.child(index)
            items.append(item.data(0, item.UserType))
        return items

    def append(self, item):
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.addChild(item.qt)
        return item

    def insert(self, index, item):
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.insertChild(index, item.qt)
        return item

    @property
    def expanded(self):
        return self.qt.isExpanded()

    @expanded.setter
    def expanded(self, expand):
        self.qt.setExpanded(expand)

    def __getitem__(self, index):
        return TreeItemColumn(index, self.qt)

class TreeItemColumn:

    def __init__(self, column, qt):
        self.column = column
        self.qt = qt

    @property
    def value(self):
        return self.qt.data(self.column, self.qt.Type)

    @value.setter
    def value(self, value):
        return self.qt.setData(self.column, self.qt.Type, value)

    @property
    def color(self):
        return self.qt.foreground(self.column).color().name()

    @color.setter
    def color(self, color):
        if color is None:
            brush = self.qt._default_foreground
        else:
            brush = self.qt.foreground(self.column)
            brush.setColor(QtGui.QColor(color))
        self.qt.setForeground(self.column, brush)

    @property
    def background(self):
        return self.qt.background(self.column).color().name()

    @background.setter
    def background(self, color):
        if color is None:
            brush = self.qt._default_background
        else:
            brush = self.qt.background(self.column)
            brush.setStyle(QtCore.Qt.SolidPattern)
            brush.setColor(QtGui.QColor(color))
        self.qt.setBackground(self.column, brush)

    @property
    def checked(self):
        return self.qt.checkState(self.column) == QtCore.Qt.Checked

    @checked.setter
    def checked(self, state):
        if state is None:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
            self.qt.setFlags(flags)
        else:
            flags = self.qt.flags() | QtCore.Qt.ItemIsUserCheckable
            self.qt.setFlags(flags)
            self.qt.setCheckState(self.column, QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)
