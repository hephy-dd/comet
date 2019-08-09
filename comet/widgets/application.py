import logging
import signal
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from ..logger import logger

__all__ = ['MainWindow']

class Application(object):

    def __init__(self):
        self.__name = 'comet'
        self.__windows = []
        self.__application = QtWidgets.QApplication(sys.argv)
        self.__application.setOrganizationName('HEPHY')
        self.__application.setOrganizationDomain('hephy.at')
        self.__application.setApplicationName(self.name())

    def name(self):
        return self.__name

    def setName(self, name):
        """Set application name."""
        self.__name = name

    def addWindow(self, window):
        self.__windows.append(window)

    def run(self):
        # Setup logger
        fileHandler = logging.FileHandler('comet.log')
        fileHandler.setLevel(logging.INFO)
        logger().addHandler(fileHandler)

        # Setup application
        self.__application.setApplicationName(self.name())

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
