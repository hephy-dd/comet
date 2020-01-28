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
        self.__children.append(child)
        self.qt.layout().addWidget(child.qt)
        self.stretch = self.stretch

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
