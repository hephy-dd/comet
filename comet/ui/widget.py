from PyQt5 import QtWidgets

from .core import Object

__all__ = ['Widget']

class Widget(Object):

    QtBaseClass = QtWidgets.QWidget

    def __init__(self, title=None, enabled=True, visible=None, width=None, height=None, layout=None, tooltip=None, tooltip_duration=None, stylesheet=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.enabled = enabled
        # Prevent visual glitch.
        if visible is not None:
            self.visible = visible
        self.width = width
        self.height = height
        self.layout = layout
        self.stylesheet = stylesheet
        self.tooltip = tooltip
        self.tooltip_duration = tooltip_duration

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

    def close(self):
        self.qt.close()

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
        if self.qt.layout() is not None:
            self.qt.layout().removeWidget(self.__layout.qt)
            self.__layout.qt.setParent(None)
            self.__layout.qt.hide()
        self.__layout = layout
        if layout is not None:
            if self.qt.layout() is None:
                self.qt.setLayout(QtWidgets.QVBoxLayout())
            self.qt.layout().addWidget(layout.qt)

    def move(self, x, y):
        return self.qt.move(x, y)

    @property
    def pos(self):
        return self.x, self.y

    def resize(self, width, height):
        self.qt.resize(width, height)

    @property
    def size(self):
        return self.width, self.height

    @property
    def stylesheet(self):
        return self.qt.styleSheet()

    @stylesheet.setter
    def stylesheet(self, stylesheet):
        self.qt.setStyleSheet("" if stylesheet is None else format(stylesheet))

    @property
    def tooltip(self):
        return self.qt.toolTip()

    @tooltip.setter
    def tooltip(self, tooltip):
        self.qt.setToolTip("" if tooltip is None else format(tooltip))

    @property
    def tooltip_duration(self):
        return self.qt.toolTipDuration() / 1000.

    @tooltip_duration.setter
    def tooltip_duration(self, duration):
        self.qt.setToolTipDuration(-1 if duration is None else duration * 1000)

    def update(self):
        self.qt.update()

    @property
    def x(self):
        return self.qt.x()

    @property
    def y(self):
        return self.qt.y()
