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

    def __init__(self, name=None):
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
        self.__widget = Widget(id="root")
        self.__main_window = MainWindow()
        self.__main_window.setCentralWidget(self.__widget.qt)

        # Setup logger
        logging.getLogger().setLevel(logging.INFO)

    def get(self, id):
        return get(id)

    @property
    def title(self):
        return self.__widget.title

    @title.setter
    def title(self, title):
        self.__widget.title = title

    @property
    def layout(self):
        return self.__widget.layout

    @layout.setter
    def layout(self, layout):
        self.__widget.layout = layout

    def __handler(self, signum, frame):
        """Interupt signal handler, trying to close application windows."""
        if signum == signal.SIGINT:
            self.__app.closeAllWindows()

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
