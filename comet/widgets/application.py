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
import pyqtgraph

from ..utilities import make_path
from ..settings import Settings

__all__ = ['MainWindow']

class Application(object):

    OrganizationName = 'HEPHY'
    OrganizationDomain = 'hephy.at'
    ApplicationName = 'comet'

    def __init__(self):
        self.__application = QtWidgets.QApplication(sys.argv)
        self.__application.setOrganizationName(self.OrganizationName)
        self.__application.setOrganizationDomain(self.OrganizationDomain)
        self.__application.setApplicationName(self.ApplicationName)
        self.__application.setWindowIcon(QtGui.QIcon(make_path('assets', 'icons', 'comet.svg')))

        # Setup logger
        logging.getLogger('comet').setLevel(logging.INFO)
        fileHandler = logging.FileHandler('comet.log')
        fileHandler.setLevel(logging.INFO)
        logging.getLogger('comet').addHandler(fileHandler)

        # Setup plot configuration
        settings = Settings()
        pyqtgraph.setConfigOption('background', 'w' if settings.invertPlots() else 'k')

    def name(self):
        """Returns application name."""
        return self.__application.applicationName()

    def setName(self, name):
        """Set application name."""
        return self.__application.setApplicationName(name)

    def run(self):
        """Run application event loop."""

        # Register interupt signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        return self.__application.exec_()
