import copy
import logging
import random
import threading
import time
import traceback
import sys, os

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

class EventHandler(QtCore.QObject):

    __signal = QtCore.pyqtSignal(str, object, object)
    """Emited from worker thread with arguments: key, args, kwargs."""

    def __init__(self, lock, events):
        super().__init__()
        self.__lock = lock
        self.__events = events.copy()
        self.__thread = threading.get_ident()
        self.__signal.connect(lambda key, args, kwargs: self[key](*args, **kwargs))

    def __len__(self):
        return len(self.__events)

    def keys(self):
        return self.__events.keys()

    def items(self):
        return self.__events.items()

    def clear(self):
        with self.__lock:
            self.__events.clear()

    def get(self, key):
        with self.__lock:
            return self.__events.get(key)

    def __getitem__(self, key):
        with self.__lock:
            # Access in main thread
            if self.__thread == threading.get_ident():
                return self.__events[key]
            # Access in worker thread
            def Event(*args, **kwargs):
                self.__signal.emit(key, args, kwargs)
            return Event

    def __setitem__(self, key, value):
        self.__events[key] = value

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        if name.startswith(f'_{self.__class__.__name__}__'):
            super().__setattr__(name, value)
        else:
            self[name] = value

class StopRequest(Exception):
    """Stop request exception."""
    pass

class Process:

    def __init__(self, id=None, target=None, events={}, *args, **kwargs):
        self.id = id
        self.__thread = None
        self.__lock = threading.RLock()
        self.__stop_requested = threading.Event()
        self.__target = target
        self.__events = EventHandler(self.__lock, events)
        self.__values = {}

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    def start(self):
        with self.__lock:
            if not self.alive:
                self.__thread = Thread(target=self.__run, name=self.id)
                self.__thread.start()

    def stop(self):
        with self.__lock:
            if self.alive:
                self.__thread.stop()

    def join(self):
        with self.__lock:
            if not self.alive:
                return
        self.__thread.join()

    @property
    def alive(self):
        with self.__lock:
            return self.__thread and self.__thread.is_alive()

    @property
    def running(self):
        with self.__lock:
            return self.alive and self.__thread.is_running()

    def run(self):
        if callable(self.__target):
            self.__target(self)

    def __run(self):
        if 'started' in self.events.keys():
            self.events['started']()
        try:
            self.run()
        except StopRequest:
            pass
        except Exception as e:
            tb = traceback.format_exc()
            logging.error("%s %s: %s", type(self).__name__, type(e).__name__, e)
            if 'failed' in self.events.keys():
                self.events['failed'](e, tb)
        finally:
            if 'finished' in self.events.keys():
                self.events['finished']()

    @property
    def events(self):
        """Returns event handler."""
        return self.__events

    def set(self, key, value):
        """Set thread safe immutable copy of value."""
        with self.__lock:
            self.__values[key] = copy.deepcopy(value)

    def get(self, key, default=None):
        """Returns thread safe immutable copy of value."""
        with self.__lock:
            return copy.deepcopy(self.__values.get(key, default))

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
