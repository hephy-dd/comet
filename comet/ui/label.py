from PyQt5 import QtWidgets

from .widget import Widget

__all__ = ['Label']

class Label(Widget):
    """A text label."""

    QtBaseClass = QtWidgets.QLabel

    def __init__(self, text=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, text):
        self.qt.setText("" if text is None else format(text))
