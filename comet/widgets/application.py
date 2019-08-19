"""Application module.

Usage:

>>> app = comet.Application()
>>> app.setName('MyApp')
>>> app.addWindow(comet.MainWindow())
>>> app.run()
"""

import logging
import signal
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from ..logger import logger

__all__ = ['MainWindow']

class Application(object):

    OrganizationName = 'HEPHY'
    OrganizationDomain = 'hephy.at'
    ApplicationName = 'comet'

    def __init__(self):
        self.__windows = []
        self.__application = QtWidgets.QApplication(sys.argv)
        self.__application.setOrganizationName(self.OrganizationName)
        self.__application.setOrganizationDomain(self.OrganizationDomain)
        self.__application.setApplicationName(self.ApplicationName)

    def name(self):
        """Returns application name."""
        return self.__application.applicationName()

    def setName(self, name):
        """Set application name."""
        return self.__application.setApplicationName(name)

    def addWindow(self, window):
        """Add application window."""
        self.__windows.append(window)

    def run(self):
        """Run application event loop."""
        # Setup logger
        fileHandler = logging.FileHandler('comet.log')
        fileHandler.setLevel(logging.INFO)
        logger().addHandler(fileHandler)

        # Initalize settings
        QtCore.QSettings()

        # Register interupt signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        # Raise windows
        for window in self.__windows:
            window.show()
            window.raise_()

        return self.__application.exec_()
