import logging
import signal
import sys

from PyQt5 import QtCore, QtWidgets

from .version import __version__
from .widgets import MainWindow
from .settings import SettingsMixin
from .device import DeviceMixin
from .process import ProcessMixin
from .ui.widget import Widget
from .ui.layout import Layout

__all__ = ['CoreApplication', 'Application']

class CoreApplication(SettingsMixin, ProcessMixin, DeviceMixin):
    """Base class for COMET application classes."""

    QtBaseClass = QtCore.QCoreApplication

    __instance = None

    def __init__(self, name=None, version=None):
        self.__qt = self.QtBaseClass(sys.argv)

        # Setup logger
        logging.getLogger().setLevel(logging.INFO)

        # Store reference to application
        CoreApplication.__instance = self

        # Application settings
        self.name = name
        self.version = version
        self.organization_name = "HEPHY"
        self.organization_domain = "hephy.at"

    @classmethod
    def app(cls):
        return cls.__instance

    @property
    def qt(self):
        return self.__qt

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
        self.qt.setApplicationVersion("" if version is None else format(version))

    @property
    def organization_name(self):
        return self.qt.organizationName()

    @organization_name.setter
    def organization_name(self, name):
        self.qt.setOrganizationName("" if name is None else format(name))

    @property
    def organization_domain(self):
        return self.qt.organizationDomain()

    @organization_domain.setter
    def organization_domain(self, domain):
        self.qt.setOrganizationDomain("" if domain is None else format(domain))

    def __signal_handler(self, signum, frame):
        """Interupt signal handler, trying to close application windows."""
        if signum == signal.SIGINT:
            self.quit()

    def quit(self):
        """Request quit application."""
        self.qt.quit()

    def run(self):
        """Run application event loop."""

        # Register interupt signal handler
        signal.signal(signal.SIGINT, self.__signal_handler)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        # Run event loop
        result = self.qt.exec_()

        # Stop processes
        self.processes.stop()
        self.processes.join()

        return result

class Application(CoreApplication):
    """Base class for COMET applications providing a default main window."""

    QtBaseClass = QtWidgets.QApplication

    def __init__(self, name=None, version=None, title=None, about=None):
        super().__init__(name, version)

        # Connections
        self.qt.lastWindowClosed.connect(self.qt.quit)

        # Initialize main window
        self.qt.window = MainWindow()
        self.__widget = Widget(id="root")

        self.qt.window.setCentralWidget(self.__widget.qt)

        # Application properties
        self.display_name = "COMET"
        self.title = title
        self.about = about

    @property
    def display_name(self):
        return self.qt.applicationDisplayName()

    @display_name.setter
    def display_name(self, name):
        self.qt.setApplicationDisplayName("" if name is None else format(name))

    @property
    def title(self):
        return self.qt.window.windowTitle()

    @title.setter
    def title(self, title):
        self.qt.window.setWindowTitle("" if title is None else format(title))

    @property
    def about(self):
        return self.qt.window.aboutText()

    @about.setter
    def about(self, about):
        self.qt.window.setAboutText(about or "")

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message
        if message is None:
            self.qt.window.clearMessage()
        else:
            self.qt.window.showMessage(message)

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, args):
        self.__progress = args
        if args is None:
            self.qt.window.hideProgress()
        else:
            self.qt.window.showProgress(*args[:2])

    @property
    def layout(self):
        return self.__widget.layout

    @layout.setter
    def layout(self, layout):
        if callable(layout):
            layout = layout()
        self.__widget.layout = layout

    def show_exception(self, e):
        self.qt.window.showException(e)

    def quit(self):
        """Request quit application."""
        self.qt.closeAllWindows()

    def run(self):
        """Run application event loop."""

        # Show main window
        self.qt.window.show()

        return super().run()
