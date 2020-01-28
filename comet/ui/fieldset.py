from PyQt5 import QtWidgets

from .widget import Widget

__all__ = ['FieldSet']

class FieldSet(Widget):

    QtBaseClass = QtWidgets.QGroupBox

    def __init__(self, title=None, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.layout = layout

    @property
    def title(self):
        return self.qt.title()

    @title.setter
    def title(self, title):
        self.qt.setTitle("" if title is None else format(title))
