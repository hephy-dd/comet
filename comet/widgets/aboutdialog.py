import os
from PyQt5 import QtWidgets, uic

Ui_AboutDialog, AboutDialogBase = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui', 'aboutdialog.ui'))

__all__ = ['AboutDialog']

class AboutDialog(AboutDialogBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
