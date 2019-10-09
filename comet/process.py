import traceback
import threading
import random
import time
import sys, os
import logging

from PyQt5 import QtCore, QtWidgets

from .device import DeviceMixin
from .utils import Collection

__all__ = ['Process', 'StopRequest', 'ProcessManager']

class Thread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stopRequested = threading.Event()

    def requestStop(self):
        self.__stopRequested.set()

    def stopRequested(self):
        return self.__stopRequested.is_set()

class StopRequest(Exception):
    """Step process exception."""
    pass

class Process(QtCore.QObject):

    started = QtCore.pyqtSignal()
    """Emitted if process execution started."""

    finished = QtCore.pyqtSignal()
    """Emitted if process execution finished."""

    failed = QtCore.pyqtSignal(object)
    """Emitted if exception occured in method `run`, provides exception as argument."""

    messageChanged = QtCore.pyqtSignal(str)
    messageCleared = QtCore.pyqtSignal()

    progressChanged = QtCore.pyqtSignal(int, int)
    progressHidden = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thread = None

    def __run(self):
        self.started.emit()
        try:
            self.run()
        except StopRequest:
            pass
        except Exception as e:
            logging.error(traceback.print_exc())
            logging.error(e)
            self.failed.emit(e)
        finally:
            self.finished.emit()

    def start(self):
        if not self.isAlive():
            self.__thread = Thread(target=self.__run)
            self.__thread.start()

    def stop(self):
        if self.isAlive():
            self.__thread.requestStop()

    def join(self):
        if self.isAlive():
            self.__thread.join()

    def isAlive(self):
        return self.__thread and self.__thread.is_alive()

    def stopRequested(self):
        return self.__thread.stopRequested()

    def sleep(self, seconds):
        time.sleep(seconds)

    def time(self):
        return time.time()

    def showMessage(self, message):
        """Show message, emits signal `messageChanged`."""
        logging.info("worker %s message: %s", self, message)
        self.messageChanged.emit(message)

    def clearMessage(self):
        """Clears message, emits signal `messageCleared`."""
        self.messageCleared.emit()

    def showProgress(self, value, maximum):
        """Show progress, emits signal `progressChanged`."""
        logging.debug("worker %s progress: %s of %s", self, value, maximum)
        self.progressChanged.emit(value, maximum)

    def hideProgress(self):
        """Hide process, emits sigmal `progressHidden`."""
        self.progressHidden.emit()

    def run(self):
        raise NotImplemented()

class ProcessManager(Collection):

    def __init__(self):
        super().__init__(base=Process)

    def stop(self):
        for process in self.values():
            process.stop()

    def join(self):
        for process in self.values():
            process.join()
