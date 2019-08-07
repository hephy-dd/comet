import argparse
import logging
import signal
import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets

from .mainwindow import MainWindow

CentralWidget = QtWidgets.QWidget

__all__ = ['Application']

class Application(object):
    """Bootstrap graphical COMET application class.

    >>> from comet.widgets import Application
    >>> app = Application()
    >>> app.run()
    """

    organization = 'HEPHY'
    """Organization name for application."""

    domain = 'hephy.at'
    """Organization domain for application."""

    name = 'COMET'
    """Application name used for title and settings."""

    mainWindowClass = MainWindow
    """Application main window class."""

    centralWidgetClass = CentralWidget
    """Application main window class."""

    def createMainWindow(self):
        """Overwrite method to create custom main window."""
        window = MainWindow()
        window.setWindowTitle(self.name)
        return window

    def setupMainWindow(self, window):
        """Overwrite method to extend main window."""
        pass

    def createCentralWidget(self, context):
        """Overwrite method to create custom central widget."""
        widget = CentralWidget(context)
        return widget

    def setupCentralWidget(self, widget):
        """Overwrite method to extend central widget."""
        pass

    def createArgumentParser(self):
        """Overwrite method to create custom argument parser."""
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbose', action='store_true', help="verbose messages")
        return parser

    def setupArgumentParser(self, parser):
        """Overwrite method to extend argument parser."""
        pass

    def run(self):
        """Bootstrap and execute application."""

        # Run argument parser
        args = self.createArgumentParser().parse_args()

        # Setup logger
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO if args.verbose else logging.WARNING)

        # Create application
        app = QtWidgets.QApplication(sys.argv)

        # Setup application
        app.setOrganizationName(self.organization)
        app.setOrganizationDomain(self.domain)
        app.setApplicationName(self.name)

        # Initalize settings
        QtCore.QSettings()

        # Register interupt signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Run timer to process signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        # Create main window and central widget
        window = self.createMainWindow()
        widget = self.createCentralWidget(window)
        window.setCentralWidget(widget)
        window.show()
        window.raise_()

        return app.exec_()
