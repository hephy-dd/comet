import os
from PyQt5 import QtGui, QtWidgets, uic

from ..utilities import make_path

Ui_AboutDialog, AboutDialogBase = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')

__all__ = ['AboutDialog']

class AboutDialog(AboutDialogBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        icon = QtGui.QPixmap(make_path('assets', 'icons', 'comet.svg'))
        self.ui.iconLabel.setPixmap(icon)
