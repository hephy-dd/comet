from PyQt5 import QtWidgets

from .core import Object

__all__ = ['Widget']

class Widget(Object):

    QtBaseClass = QtWidgets.QWidget

    def __init__(self, title=None, enabled=True, visible=True, width=None, height=None, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.enabled = enabled
        self.visible = visible
        self.width = width
        self.height = height
        self.layout = layout

    @property
    def title(self):
        return self.qt.windowTitle()

    @title.setter
    def title(self, title):
        self.qt.setWindowTitle(title)

    @property
    def enabled(self):
        return self.qt.isEnabled()

    @enabled.setter
    def enabled(self, enabled):
        self.qt.setEnabled(enabled)

    @property
    def visible(self):
        return self.qt.isVisible()

    @visible.setter
    def visible(self, visible):
        self.qt.setVisible(visible)

    @property
    def width(self):
        return self.qt.width()

    @width.setter
    def width(self, width):
        if width is None:
            self.qt.setMinimumWidth(0)
            self.qt.setMaximumWidth(QtWidgets.QWIDGETSIZE_MAX)
        else:
            self.qt.setMinimumWidth(width)
            self.qt.setMaximumWidth(width)

    @property
    def height(self):
        return self.qt.height()

    @height.setter
    def height(self, height):
        if height is None:
            self.qt.setMinimumHeight(0)
            self.qt.setMaximumHeight(QtWidgets.QWIDGETSIZE_MAX)
        else:
            self.qt.setMinimumHeight(height)
            self.qt.setMaximumHeight(height)

    @property
    def layout(self):
        return self.__layout

    @layout.setter
    def layout(self, layout):
        if self.qt.layout():
            self.qt.layout().removeItem(self.__layout)
        self.__layout = layout
        if layout is not None:
            if not self.qt.layout():
                self.qt.setLayout(QtWidgets.QVBoxLayout())
            self.qt.layout().addWidget(layout.qt)
