from PyQt5 import QtGui, QtWidgets

from ..mixins import UiLoaderMixin

__all__ = ['AboutDialog']

class AboutDialog(QtWidgets.QDialog, UiLoaderMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadUi()
        #icon = QtGui.QPixmap(make_path('assets', 'icons', 'comet.svg'))
        #self.ui.iconLabel.setPixmap(icon)
