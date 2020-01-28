from PyQt5 import QtWidgets

from .core import Object

__all__ = ['Widget']

class Widget(Object):

    QtBaseClass = QtWidgets.QWidget

    def __init__(self, title=None, enabled=True, visible=True, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.enabled = enabled
        self.visible = visible
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
