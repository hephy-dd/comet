import logging
import signal
import sys

import qutie as ui
from qutie.qutie import QtCore
from qutie.qutie import QtGui

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
        self.last_window_closed = self.qt.quit

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
        """Main window title."""
        return self.window.title

    @title.setter
    def title(self, value):
        self.window.title = value

    @property
    def width(self):
        """Main window width."""
        return self.window.width

    @width.setter
    def width(self, width):
        self.window.resize(width, self.height)

    @property
    def height(self):
        """Main window height."""
        return self.window.height

    @height.setter
    def height(self, height):
        self.window.resize(self.width, height)

    @property
    def about(self):
        """Application about text."""
        return self.window.about_text

    @about.setter
    def about(self, value):
        self.window.about_text = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message
        if message is None:
            self.window.hide_message()
        else:
            self.window.show_message(message)

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, args):
        self.__progress = args
        if args is None:
            self.window.hide_progress()
        else:
            self.window.show_progress(*args[:2])

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

        try:
            # Run event loop
            return super().run()
        finally:
            # Stop processes
            self.processes.stop()
            self.processes.join()
