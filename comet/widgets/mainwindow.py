from PyQt5 import QtCore, QtWidgets

from ..mixins import UiLoaderMixin, ProcessMixin
from .preferencesdialog import PreferencesDialog
from .aboutdialog import AboutDialog

__all__ = ['MainWindow']

class MainWindow(QtWidgets.QMainWindow, UiLoaderMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loadUi()

    @QtCore.pyqtSlot()
    def onShowPreferences(self):
        dialog = PreferencesDialog(self)
        dialog.exec_()

    @QtCore.pyqtSlot()
    def onShowAbout(self):
        dialog = QtWidgets.AboutDialog(self)
        dialog.exec_()

    @QtCore.pyqtSlot()
    def onShowAboutQt(self):
        dialog = QtWidgets.QDialog(self)
        dialog.exec_()

    def setCentralWidget(self, widget):
        super().setCentralWidget(widget)
        self.setWindowTitle(widget.windowTitle())

    @QtCore.pyqtSlot(object)
    def closeEvent(self, event):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setText(self.tr("Quit application?"))
        dialog.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        dialog.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        dialog.exec_()

        if dialog.result() == dialog.Ok:
            dialog = ProcessDialog(self)
            dialog.exec_()
            event.accept()
        else:
            event.ignore()

class ProcessDialog(QtWidgets.QProgressDialog, ProcessMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 0)
        self.setValue(0)
        self.setCancelButton(None)
        self.setLabelText("Stopping active threads...")

    @QtCore.pyqtSlot()
    def close(self):
        self.processes().stop()
        self.processes().join()
        super().close()

    def exec_(self):
        QtCore.QTimer.singleShot(250, self.close)
        return super().exec_()
