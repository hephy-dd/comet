from PyQt5 import QtWidgets

from .widget import Widget

__all__ = [
    'Row',
    'Column',
    'Stretch'
]

class Layout(Widget):

    QtLayoutClass = None

class BoxLayout(Layout):

    QtLayoutClass = QtWidgets.QBoxLayout

    def __init__(self, *children, stretch=None, **kwargs):
        super().__init__(**kwargs)
        layout = self.QtLayoutClass()
        layout.setContentsMargins(0, 0, 0, 0)
        self.qt.setLayout(layout)
        self.__children = []
        self.stretch = stretch
        for child in children:
            self.append(child)

    @property
    def children(self):
        return self.__children.copy()

    def append(self, child):
        """Append a widget as child."""
        self.__children.append(child)
        self.qt.layout().addWidget(child.qt)
        self.stretch = self.stretch

    def insert(self, index, child):
        """Insert a widget as child at index position."""
        self.__children.insert(index, child)
        self.qt.layout().insertWidget(index, child.qt)
        self.stretch = self.stretch

    def remove(self, child):
        """Remove a child."""
        if child not in self.__children:
            raise ValueError(f"not a child {child}")
        self.__children.remove(child)
        index = self.qt.layout().indexOf(child.qt)
        self.qt.layout().takeAt(index)
        child.qt.setParent(None)

    def clear(self):
        """Remove all children."""
        while self.__children:
            self.remove(self.__children[0])

    @property
    def stretch(self):
        return self.__stretch

    @stretch.setter
    def stretch(self, stretch):
        self.__stretch = stretch
        if stretch is None:
            stretch = []
        stretch = list(stretch) + [0] * (len(self.children) - len(stretch))
        for index, value in enumerate(stretch):
            self.qt.layout().setStretch(index, int(value))

class Row(BoxLayout):

    QtLayoutClass = QtWidgets.QHBoxLayout

class Column(BoxLayout):

    QtLayoutClass = QtWidgets.QVBoxLayout

class Stretch(Widget):

    QtBaseClass = QtWidgets.QWidget

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.qt.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
