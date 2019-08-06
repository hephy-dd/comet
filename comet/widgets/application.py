import argparse
import logging
import signal
import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets

from .mainwindow import MainWindow

__all__ = ['Application']

class Application(object):
    """Bootstrap graphical COMET application class.

    >>> from comet.widgets import Application
    >>> app = Application()
    >>> app.run()
    """

    OrganizationName = 'HEPHY'
    """Organization name for application."""

    OrganizationDomain = 'hephy.at'
    """Organization domain for application."""

    ApplicationName = 'COMET'
    """Application name used to store settings."""

    MainWindowClass = MainWindow
    """Application main window class."""

    def setupWindow(self, context):
        """Overwrite method to setup window and central widget."""
        pass

    def setupArgumentParser(self, parser):
        """Overwrite method to setup argument parser."""
        pass

    def parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbose', action='store_true', help="Verbose messages")
        self.setupArgumentParser(parser)
        return parser.parse_args()

    def run(self):
        """Bootstrap and execute application."""

        args = self.parse()

        # Setup logger
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO if args.verbose else logging.WARNING)

        # Create application
        app = QtWidgets.QApplication(sys.argv)

        # Setup application
        app.setOrganizationName(self.OrganizationName)
        app.setOrganizationDomain(self.OrganizationDomain)
        app.setApplicationName(self.ApplicationName)

        # Initalize settings
        QtCore.QSettings()

        # Create main window
        w = self.MainWindowClass()
        self.setupWindow(w)
        w.show()
        w.raise_()

        # Register interupt signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Run timer to process signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        return app.exec_()

