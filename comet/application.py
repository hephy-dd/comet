import logging
import signal
import sys

import qutie as ui
from qutie.qt import QtCore
from qutie.qt import QtGui

from .version import __version__
from .ui.mainwindow import MainWindow
from .settings import SettingsMixin
from .resource import ResourceMixin
from .process import ProcessMixin
from .utils import make_path

__all__ = ['Application']

COMET_ORGANIZATION = "HEPHY"
COMET_DOMAIN = "hephy.at"
COMET_DISPLAY_NAME = "COMET"

class Application(ui.Application, SettingsMixin, ProcessMixin, ResourceMixin):
    """Base class for COMET applications providing a default main window."""

    def __init__(self, name=None, *, title=None, width=None,
                 height=None, about=None, **kwargs):
        super().__init__(name=name, **kwargs)

        if 'organization' not in kwargs:
            self.organization = COMET_ORGANIZATION
        if 'domain' not in kwargs:
            self.domain = COMET_DOMAIN
        if 'display_name' not in kwargs:
            self.display_name = COMET_DISPLAY_NAME
        if 'icon' not in kwargs:
            self.icon = make_path('assets', 'icons', 'comet.svg')

        # Connections
        self.qt.lastWindowClosed.connect(self.qt.quit)

        # Initialize main window
        self.__window = MainWindow()
        self.__widget = ui.Widget()

        # Main window properties
        if title is not None:
            self.title = title
        if about is not None:
            self.about = about
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        self.window.layout = self.__widget

    @property
    def title(self):
        return self.window.title

    @title.setter
    def title(self, value):
        self.window.title = value

    @property
    def width(self):
        return self.window.width

    @width.setter
    def width(self, width):
        self.window.width = width

    @property
    def height(self):
        return self.window.height

    @height.setter
    def height(self, height):
        self.window.height = height

    @property
    def about(self):
        return self.window.aboutText()

    @about.setter
    def about(self, value):
        self.window.setAboutText(value)

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message
        if message is None:
            self.window.clearMessage()
        else:
            self.window.showMessage(message)

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, args):
        self.__progress = args
        if args is None:
            self.window.hideProgress()
        else:
            self.window.showProgress(*args[:2])

    @property
    def window(self):
        return self.__window

    @property
    def layout(self):
        return self.__widget.layout

    @layout.setter
    def layout(self, layout):
        self.__widget.layout = layout

    def run(self):
        """Run application event loop."""
        # Show main window
        self.window.show()
        self.window.up()

        # Run event loop
        result = super().run()

        # Stop processes
        self.processes.stop()
        self.processes.join()

        return result
