from PyQt5 import QtWidgets

from .widget import Widget
from .input import Text

__all__ = ['ScrollArea']

class ScrollArea(Widget):

    QtBaseClass = QtWidgets.QScrollArea

    def __init__(self, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.__widget = Widget()
        self.qt.setWidgetResizable(True)
        self.qt.setWidget(self.__widget.qt)
        self.layout = layout

    @property
    def layout(self):
        return self.__widget.layout

    @layout.setter
    def layout(self, layout):
        if self.qt.widget():
            self.__widget.layout = layout
