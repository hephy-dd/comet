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

    message = QtCore.pyqtSignal(str)

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
