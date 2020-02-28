from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .core import Base, callback
from .widget import Widget

__all__ = ['Table']

class Table(Widget):
    """Table

    >>> table = comet.Table(header=["Key", "Value"])
    >>> table.append(["Spam", "Eggs"])
    >>> table.insert(["Ham", "Spam"])
    >>> for row in table:
    ...     for item in row:
    ...         item.color = "blue"
    >>> table.clear()
    """

    QtBaseClass = QtWidgets.QTableWidget

    def __init__(self, header=[], rows=[], stretch=False, activated=None, changed=None, clicked=None, double_clicked=None, selected=None, **kwargs):
        super().__init__(**kwargs)
        self.header = header
        for row in rows:
            self.append(row)
        self.stretch = stretch
        self.activated = activated
        self.changed = changed
        self.clicked = clicked
        self.double_clicked = double_clicked
        self.selected = selected
        self.qt.itemActivated.connect(self.__activated_handler)
        self.qt.itemChanged.connect(self.__changed_handler)
        self.qt.itemClicked.connect(self.__clicked_handler)
        self.qt.itemDoubleClicked.connect(self.__double_clicked_handler)
        self.qt.itemSelectionChanged.connect(self.__selected_handler)
        self.qt.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.qt.horizontalHeader().setHighlightSections(False)
        self.qt.verticalHeader().hide()

    @property
    def activated(self):
        return self.__activated

    @activated.setter
    def activated(self, activated):
        self.__activated = activated

    @callback
    def __activated_handler(self, item):
        if callable(self.activated):
            item = item.data(item.UserType)
            if item is not None:
                self.activated(item)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    @callback
    def __changed_handler(self, item):
        if callable(self.changed):
            item = item.data(item.UserType)
            if item is not None:
                self.changed(item)

    @property
    def clicked(self):
        return self.__clicked

    @clicked.setter
    def clicked(self, clicked):
        self.__clicked = clicked

    @callback
    def __clicked_handler(self, item):
        if callable(self.clicked):
            item = item.data(item.UserType)
            if item is not None:
                self.clicked(item)

    @property
    def double_clicked(self):
        return self.__double_clicked

    @double_clicked.setter
    def double_clicked(self, double_clicked):
        self.__double_clicked = double_clicked

    @callback
    def __double_clicked_handler(self, item):
        if callable(self.double_clicked):
            item = item.data(item.UserType)
            if item is not None:
                self.double_clicked(item)

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, selected):
        self.__selected = selected

    @callback
    def __selected_handler(self):
        if callable(self.selected):
            items = self.qt.selectedItems()
            if items:
                item = items[0].data(items[0].UserType)
                self.selected(item)

    @property
    def header(self):
        return self.qt.horizontalHeaderLabels()

    @header.setter
    def header(self, items):
        self.qt.setColumnCount(len(items))
        self.qt.setHorizontalHeaderLabels(items)

    def append(self, items):
        """Append items, returns appended items.

        >>> table.append(TableItem(value="Spam"), TableItem(value="Eggs"))
        or
        >>> table.append(["Spam", "Eggs"])
        """
        row = self.qt.rowCount()
        self.qt.setRowCount(self.qt.rowCount() + 1)
        return self.insert(row, items)

    def insert(self, row, items):
        """Insert items at row, returns inserted items.

        >>> table.insert(0, TableItem(value="Spam"), TableItem(value="Eggs"))
        or
        >>> table.insert(0, ["Spam", "Eggs"])
        """
        for column, item in enumerate(items):
            if not isinstance(item, TableItem):
                item = TableItem(value=item)
            self.qt.setItem(row, column, item.qt)
        return self[row]

    def clear(self):
        self.qt.clearContents()

    @property
    def current(self):
        """Returns current table item or None."""
        item = self.qt.currentItem()
        if item is not None:
            return item.data(item.UserType)

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

    def __init__(self, value=None, color=None, background=None, enabled=True, readonly=True, checked=None, checkable=False, **kwargs):
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
        self.checkable = checkable

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
            self.qt.setFlags(self.qt.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            self.qt.setFlags(self.qt.flags() | QtCore.Qt.ItemIsEditable)

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

    @property
    def checkable(self):
        return self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable

    @checkable.setter
    def checkable(self, state):
        if state:
            flags = self.qt.flags() | QtCore.Qt.ItemIsUserCheckable
        else:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
        self.qt.setFlags(flags)
