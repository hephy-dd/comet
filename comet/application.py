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

class Application(ProcessMixin, DeviceMixin):

    def __init__(self, name=None, title=None, version=None, about=None):
        app = self.__app = QtWidgets.QApplication(sys.argv)

        # Application settings
        app.setApplicationName(name or "comet")
        app.setApplicationDisplayName("COMET")
        app.setApplicationVersion(__version__)
        app.setOrganizationName("HEPHY")
        app.setOrganizationDomain("hephy.at")

        # Initialize settings
        QtCore.QSettings()

        # Connections
        app.lastWindowClosed.connect(app.quit)

        # Initialize settings
        self.__title = None
        self.__version = None
        self.__widget = Widget(id="root")
        self.__main_window = MainWindow()
        self.__main_window.setCentralWidget(self.__widget.qt)

        # Setup logger
        logging.getLogger().setLevel(logging.INFO)

        # Set properties
        self.title = title
        self.version = version
        self.about = about

    def get(self, id):
        return get(id)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title
        self.__update_window_title()

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version
        self.__update_window_title()

    @property
    def about(self):
        return self.__main_window.about

    @about.setter
    def about(self, about):
        self.__main_window.about = about or ""

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message
        if message is None:
            self.__main_window.clearMessage()
        else:
            self.__main_window.showMessage(message)

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, args):
        self.__progress = args
        if args is None:
            self.__main_window.hideProgress()
        else:
            self.__main_window.showProgress(*args[:2])

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
            self.__app.closeAllWindows()

    def __update_window_title(self):
        tokens = []
        if self.title is not None:
            tokens.append(format(self.title))
        if self.version is not None:
            tokens.append(format(self.version))
        self.__main_window.setWindowTitle(" ".join(tokens))

    def run(self):
        """Run application event loop."""
        self.__main_window.show()

        # Register interupt signal handler
        signal.signal(signal.SIGINT, self.__handler)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        result = self.__app.exec_()

        self.processes.stop()
        self.processes.join()

        return result
