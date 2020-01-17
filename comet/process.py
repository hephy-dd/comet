import traceback
import threading
import random
import time
import sys, os
import logging

from PyQt5 import QtCore, QtWidgets

from .device import DeviceMixin
from .collection import Collection

__all__ = ['Process', 'StopRequest', 'ProcessManager', 'ProcessMixin']

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

    __started = QtCore.pyqtSignal()
    """Emitted if process execution started."""

    __finished = QtCore.pyqtSignal()
    """Emitted if process execution finished."""

    __failed = QtCore.pyqtSignal(object)
    """Emitted if exception occured in method `run`, provides exception as argument.
    """

    __push = QtCore.pyqtSignal(object, object)
    """Emmited on push() to propagate data from inside a thread."""

    __message = QtCore.pyqtSignal(str)

    messageChanged = QtCore.pyqtSignal(str)
    messageCleared = QtCore.pyqtSignal()

    progressChanged = QtCore.pyqtSignal(int, int)
    progressHidden = QtCore.pyqtSignal()

    def __init__(self, begin=None, finish=None, fail=None, pop=None, parent=None):
        super().__init__(parent)
        self.__thread = None
        self.begin = begin
        self.finish = finish
        self.fail = fail
        self.pop = pop
        self.__started.connect(self.__started_handler)
        self.__finished.connect(self.__finished_handler)
        self.__failed.connect(self.__failed_handler)
        self.__push.connect(self.__pop_handler)

    def __started_handler(self):
        if callable(self.begin):
            self.begin()
    @property
    def begin(self):
        return self.__begin

    @begin.setter
    def begin(self, callable):
        self.__begin = callable

    def __finished_handler(self):
        if callable(self.finish):
            self.finish()
    @property
    def finish(self):
        return self.__finish

    @finish.setter
    def finish(self, callable):
        self.__finish = callable

    def __failed_handler(self):
        if callable(self.fail):
            self.fail()

    @property
    def fail(self):
        return self.__fail

    @fail.setter
    def fail(self, callable):
        self.__fail = callable

    def push(self, key, value):
        """Push user data to be received by main thread. Key must be a string."""
        self.__push.emit(key, value)

    def __pop_handler(self, key, value):
        if callable(self.pop):
            self.pop(key, value)

    @property
    def pop(self):
        return self.__pop

    @pop.setter
    def pop(self, callable):
        self.__pop = callable

    def __run(self):
        self.__started.emit()
        try:
            self.run()
        except StopRequest:
            pass
        except Exception as e:
            self.handleException(e)
        finally:
            self.__finished.emit()

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

    def handleException(self, exception):
        exception.details = traceback.format_exc()
        logging.error(exception.details)
        logging.error(exception)
        self.__failed.emit(exception)

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

class ProcessMixin:

    __processes = ProcessManager()

    @property
    def processes(self):
        return self.__class__.__processes
