import traceback
import threading
import random
import time
import sys, os
import logging

from PyQt5 import QtCore, QtWidgets

from .driver import InstrumentMixin
from .collection import Collection

__all__ = ['Process', 'StopRequest', 'ProcessManager', 'ProcessMixin']

class Thread(threading.Thread):

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

class Process(QtCore.QObject, InstrumentMixin):

    __begin_signal = QtCore.pyqtSignal()
    """Emitted if process execution started."""

    __finish_signal = QtCore.pyqtSignal()
    """Emitted if process execution finished."""

    __fail_signal = QtCore.pyqtSignal(object)
    """Emitted if exception occured in method `run`, provides exception as argument.
    """

    __push_signal = QtCore.pyqtSignal(str, object, object)
    """Emmited on push() to propagate data from inside a thread."""

    __message_signal = QtCore.pyqtSignal(str)

    __progress_signal = QtCore.pyqtSignal(int, int)

    def __init__(self, begin=None, finish=None, fail=None, slots={}, parent=None):
        super().__init__(parent)
        self.__thread = None
        self.begin = begin
        self.finish = finish
        self.fail = fail
        self.__slots = slots or {}
        self.message = None
        self.progress = None
        self.__begin_signal.connect(self.__begin_handler)
        self.__finish_signal.connect(self.__finish_handler)
        self.__fail_signal.connect(self.__fail_handler)
        self.__push_signal.connect(self.__push_handler)
        self.__message_signal.connect(self.__message_handler)
        self.__progress_signal.connect(self.__progress_handler)

    def __begin_handler(self):
        if callable(self.begin):
            self.begin()

    @property
    def begin(self):
        return self.__begin

    @begin.setter
    def begin(self, fn):
        self.__begin = fn

    def __finish_handler(self):
        if callable(self.finish):
            self.finish()

    @property
    def finish(self):
        return self.__finish

    @finish.setter
    def finish(self, fn):
        self.__finish = fn

    def __fail_handler(self, e):
        if callable(self.fail):
            self.fail(e)

    @property
    def fail(self):
        return self.__fail

    @fail.setter
    def fail(self, fn):
        self.__fail = fn

    def push(self, key, *args, **kwargs):
        """Emit a user callback to the main thread."""
        self.__push_signal.emit(key, args, kwargs)

    def __push_handler(self, key, args, kwargs):
        if key in self.__slots:
            fn = self.__slots.get(key)
            if callable(fn):
                fn(*args, **kwargs)

    @property
    def slots(self):
        return self.__slots

    def __message_handler(self, message):
        if callable(self.message):
            self.message(message)

    def __progress_handler(self, value, maximum):
        if callable(self.progress):
            self.progress(value, maximum)

    def __run(self):
        self.__begin_signal.emit()
        try:
            self.run()
        except StopRequest:
            pass
        except Exception as e:
            self.__handle_exception(e)
        finally:
            self.__finish_signal.emit()

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

    def sleep(self, seconds):
        time.sleep(seconds)

    def time(self):
        return time.time()

    def __handle_exception(self, e):
        e.details = traceback.format_exc()
        logging.error(e.details)
        logging.error(e)
        self.__fail_signal.emit(e)

    def run(self):
        raise NotImplemented()

class ProcessManager(Collection):

    ValueType = Process

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
