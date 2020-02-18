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
    """Thread class with extended stop property."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stop_requested = threading.Event()

    def stop(self):
        self.__stop_requested.set()

    def is_running(self):
        return not self.__stop_requested.is_set()

class StopRequest(Exception):
    """Step process exception."""
    pass

class Process(QtCore.QObject, DeviceMixin):

    __started_signal = QtCore.pyqtSignal()
    """Emitted if process execution started."""

    __finished_signal = QtCore.pyqtSignal()
    """Emitted if process execution finished."""

    __failed_signal = QtCore.pyqtSignal(object, object)
    """Emitted if exception occured in method `run`, provides exception as argument.
    """

    __callback_signal = QtCore.pyqtSignal(str, object, object)
    """Emmited on push() to propagate data from inside a thread."""

    def __init__(self, started=None, finished=None, failed=None, **callbacks):
        super().__init__()
        self.__thread = None
        self.started = started
        self.finished = finished
        self.failed = failed
        self.__callbacks = callbacks
        self.__started_signal.connect(self.__started_handler)
        self.__finished_signal.connect(self.__finished_handler)
        self.__failed_signal.connect(self.__failed_handler)
        self.__callback_signal.connect(self.__callback_handler)

    @property
    def started(self):
        return self.__started

    @started.setter
    def started(self, fn):
        self.__started = fn

    def __started_handler(self):
        if callable(self.started):
            self.started()

    @property
    def finished(self):
        return self.__finished

    @finished.setter
    def finished(self, fn):
        self.__finished = fn

    def __finished_handler(self):
        if callable(self.finished):
            self.finished()

    @property
    def failed(self):
        return self.__failed

    @failed.setter
    def failed(self, fn):
        self.__failed = fn

    def __failed_handler(self, exc, tb):
        if callable(self.failed):
            self.failed(exc, tb)

    @property
    def callbacks(self):
        return self.__callbacks

    def push(self, key, *args, **kwargs):
        """Emit a user callback to the main thread."""
        self.__callback_signal.emit(key, args, kwargs)

    def __callback_handler(self, key, args, kwargs):
        if key in self.__callbacks:
            fn = self.__callbacks.get(key)
            if callable(fn):
                fn(*args, **kwargs)

    def __run(self):
        self.__started_signal.emit()
        try:
            self.run()
        except StopRequest:
            pass
        except Exception as e:
            self.__handle_exception(e)
        finally:
            self.__finished_signal.emit()

    def start(self):
        if not self.alive:
            self.__thread = Thread(target=self.__run)
            self.__thread.start()

    def stop(self):
        if self.alive:
            self.__thread.stop()

    def join(self):
        if self.alive:
            self.__thread.join()

    @property
    def alive(self):
        return self.__thread and self.__thread.is_alive()

    @property
    def running(self):
        return self.alive and self.__thread.is_running()

    def __handle_exception(self, exc):
        tb = traceback.format_exc()
        logging.error(tb)
        logging.error(exc)
        self.__failed_signal.emit(exc, tb)

    def run(self):
        raise NotImplemented()

class ProcessManager(Collection):
    """Process manager."""

    ValueType = Process

    def stop(self):
        """Stop all registered processes."""
        for process in self.values():
            process.stop()

    def join(self):
        """Join all registered processes."""
        for process in self.values():
            process.join()

class ProcessMixin:
    """Mixin class to access global process manager."""

    __processes = ProcessManager()

    @property
    def processes(self):
        return self.__class__.__processes
