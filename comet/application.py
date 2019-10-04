import signal
import sys

from PyQt5 import QtCore, QtWidgets

from .version import __version__

__all__ = ['Application']

class Application(QtWidgets.QApplication):

    def __init__(self,):
        super().__init__(sys.argv)

        # Application settings
        self.setApplicationName(self.tr("comet"))
        self.setApplicationDisplayName(self.tr("COMET"))
        self.setApplicationVersion(__version__)
        self.setOrganizationName(self.tr("HEPHY"))
        self.setOrganizationDomain(self.tr("hephy.at"))

        # Connections
        self.lastWindowClosed.connect(self.quit)

        # Initialize settings
        QtCore.QSettings()

    def handler(self, signum, frame):
        """Interupt signal handler, trying to close application windows."""
        if signum == signal.SIGINT:
            self.closeAllWindows()

    def run(self):
        """Run application event loop."""

        # Register interupt signal handler
        signal.signal(signal.SIGINT, self.handler)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        return self.exec_()
