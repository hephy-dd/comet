from PyQt5 import QtWidgets

from .widget import Widget

__all__ = [
    'Tab',
    'Tabs'
]

class Tab(Widget):

    pass

class Tabs(Widget):

    QtBaseClass = QtWidgets.QTabWidget

    def __init__(self, *tabs, **kwargs):
        super().__init__(**kwargs)
        self.__tabs = []
        for tab in tabs:
            self.append(tab)

    def append(self, tab):
        self.__tabs.append(tab)
        self.qt.addTab(tab.qt, tab.title)
