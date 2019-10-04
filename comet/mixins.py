import inspect
import os

from PyQt5 import QtCore, uic

from .process import ProcessManager

__all__ = ['UiLoaderMixin', 'ProcessMixin']

class UiLoaderMixin(object):

    def loadUi(self, filename=None):
        if filename is None:
            filename = '{}.ui'.format(os.path.splitext(inspect.getfile(self.__class__))[0])
            print(filename)
        ui, base = uic.loadUiType(filename)
        self.ui = ui()
        self.ui.setupUi(self)

class ProcessMixin(object):

    __processes = ProcessManager()

    @classmethod
    def processes(cls):
        return cls.__processes
