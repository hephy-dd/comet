from PyQt5 import QtWidgets

from .widget import Widget

__all__ = [
    'Tab',
    'Tabs'
]

class Tab(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def title(self):
        return self.qt.windowTitle()

    @title.setter
    def title(self, title):
        self.qt.setWindowTitle(title)
        if self.qt.parent():
            if self.qt.parent().parent():
                index = self.qt.parent().parent().indexOf(self.qt)
                self.qt.parent().parent().setTabText(index, title)

class Tabs(Widget):

    QtBaseClass = QtWidgets.QTabWidget

    def __init__(self, *tabs, **kwargs):
        super().__init__(**kwargs)
        self.__tabs = []
        for tab in tabs:
            self.append(tab)

    def append(self, tab):
        self.qt.addTab(tab.qt, tab.title)
        self.__tabs.append(tab)

    def insert(self, index, tab):
        self.qt.insertTab(index, tab.qt, tab.title)
        self.__tabs.insert(index, tab)

    def remove(self, tab):
        index = self.__tabs.index(tab)
        self.qt.removeTab(index)
        del self.__tabs[index]

    @property
    def current(self):
        return self.qt.currentIndex()

    @current.setter
    def current(self, index):
        self.qt.setCurrentIndex(index)

    @property
    def children(self):
        return self.__tabs.copy()

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def __setitem__(self, index, tab):
        self.insert(index, tab)
