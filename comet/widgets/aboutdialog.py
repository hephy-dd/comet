from PyQt5 import QtWidgets

from .ui.aboutdialog import Ui_AboutDialog

__all__ = ['AboutDialog']

class AboutDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

