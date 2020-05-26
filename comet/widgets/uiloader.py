import inspect
import os

from PyQt5 import QtCore
from PyQt5 import uic

__all__ = ['UiLoaderMixin']

class UiLoaderMixin:

    def loadUi(self, filename=None):
        """Loads an UI file and calls setupUi(). If filename is omitted a sidefile
        of the current python module is expected (eg. `widget.py` and `widget.ui`).
        """
        dirname = inspect.getfile(self.__class__)
        if filename is None:
            filename = '{}.ui'.format(os.path.splitext(dirname)[0])
        elif not os.path.isabs(filename):
            filename = os.path.join(os.path.dirname(dirname), filename)
        ui, base = uic.loadUiType(filename)
        self.ui = ui()
        self.ui.setupUi(self)
