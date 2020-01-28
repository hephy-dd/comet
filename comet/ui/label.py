from PyQt5 import QtWidgets

from .widget import Widget

__all__ = ['Label']

class Label(Widget):

    QtBaseClass = QtWidgets.QLabel

    def __init__(self, text=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.qt.setText("" if text is None else format(text))
