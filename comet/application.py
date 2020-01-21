import logging
import signal
import sys

from PyQt5 import QtCore, QtWidgets

from .version import __version__
from .widgets import MainWindow
from .device import DeviceMixin
from .process import ProcessMixin
from .ui.core import get
from .ui.widget import Widget
from .ui.layout import Layout

__all__ = ['Application']

DisplayName = "COMET"
OrganizationName = "HEPHY"
OrganizationDomain = "hephy.at"

class Application(ProcessMixin, DeviceMixin):

    QtBaseClass = QtWidgets.QApplication

    def __init__(self, name=None, title=None, version=None, about=None):
        self.__qt = self.QtBaseClass(sys.argv)

        # Application settings
        self.name = name
        self.version = version
        self.qt.setApplicationDisplayName(DisplayName)
        self.qt.setOrganizationName(OrganizationName)
        self.qt.setOrganizationDomain(OrganizationDomain)

        # Connections
        self.qt.lastWindowClosed.connect(self.qt.quit)

        # Initialize window
        self.__widget = Widget(id="root")
        self.__window = MainWindow()
        self.__window.setCentralWidget(self.__widget.qt)
        self.title = title
        self.about = about
        self.__update_window_title()

        # Setup logger
        logging.getLogger().setLevel(logging.INFO)

        # Initialize settings
        QtCore.QSettings()

    @property
    def qt(self):
        return self.__qt

    def get(self, id):
        return get(id)

    @property
    def name(self):
        return self.qt.applicationName()

    @name.setter
    def name(self, name):
        self.qt.setApplicationName("" if name is None else format(name))

    @property
    def version(self):
        return self.qt.applicationVersion()

    @version.setter
    def version(self, version):
        self.qt.setApplicationVersion(version)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = "" if title is None else format(title)
        self.__update_window_title()

    @property
    def about(self):
        return self.__window.about

    @about.setter
    def about(self, about):
        self.__window.about = about or ""

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message
        if message is None:
            self.__window.clearMessage()
        else:
            self.__window.showMessage(message)

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, args):
        self.__progress = args
        if args is None:
            self.__window.hideProgress()
        else:
            self.__window.showProgress(*args[:2])

    @property
    def layout(self):
        return self.__widget.layout

    @layout.setter
    def layout(self, layout):
        if callable(layout):
            layout = layout()
        self.__widget.layout = layout

    def __handler(self, signum, frame):
        """Interupt signal handler, trying to close application windows."""
        if signum == signal.SIGINT:
            self.qt.closeAllWindows()

    def __update_window_title(self):
        tokens = []
        if self.title is not None:
            tokens.append(format(self.title))
        if self.version is not None:
            tokens.append(format(self.version))
        self.__window.setWindowTitle(" ".join(tokens))

    def show_exception(self, e):
        self.__window.showException(e)

    def run(self):
        """Run application event loop."""
        self.__window.show()

        # Register interupt signal handler
        signal.signal(signal.SIGINT, self.__handler)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        result = self.qt.exec_()

        self.processes.stop()
        self.processes.join()

        return result
