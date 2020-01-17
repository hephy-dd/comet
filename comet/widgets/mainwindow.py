import webbrowser
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets

from ..utils import make_path
from ..process import ProcessMixin
from .uiloader import UiLoaderMixin
from .preferencesdialog import PreferencesDialog
from .aboutdialog import AboutDialog

__all__ = ['MainWindow']

class MainWindow(QtWidgets.QMainWindow, UiLoaderMixin, ProcessMixin):
    """Main window for COMET applications."""

    closeRequest = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loadUi()
        # Set Icon
        self.setWindowIcon(QtGui.QIcon(make_path('assets', 'icons', 'comet.svg')))
        # Setup status bar widgets
        self.__messageLabel = QtWidgets.QLabel(self)
        self.__messageLabel.hide()
        self.statusBar().addPermanentWidget(self.__messageLabel)
        self.__progressBar = QtWidgets.QProgressBar(self)
        self.__progressBar.hide()
        self.statusBar().addPermanentWidget(self.__progressBar)
        self.about = None

    @QtCore.pyqtSlot()
    def showPreferences(self):
        """Show modal preferences dialog."""
        dialog = PreferencesDialog(self)
        dialog.exec_()

    @QtCore.pyqtSlot()
    def showContents(self):
        """Open local webbrowser with contets URL."""
        webbrowser.open(self.property('contentsUrl'))

    @QtCore.pyqtSlot()
    def showAbout(self):
        """Show modal about dialog."""
        dialog = AboutDialog(self)
        if self.about:
            dialog.ui.aboutTextEdit.setHtml(self.about)
        dialog.exec_()

    @QtCore.pyqtSlot()
    def showAboutQt(self):
        """Show modal about Qt dialog."""
        QtWidgets.QMessageBox.aboutQt(self)

    def setCentralWidget(self, widget):
        super().setCentralWidget(widget)
        self.setWindowTitle(widget.windowTitle())


    def messageLabel(self):
        return self.__messageLabel

    def showMessage(self, message):
        self.messageLabel().setText(message)
        self.messageLabel().show()

    def clearMessage(self):
        self.messageLabel().clear()
        self.messageLabel().hide()

    def progressBar(self):
        return self.__progressBar

    def showProgress(self, value, maximum):
        self.progressBar().setRange(0, maximum)
        self.progressBar().setValue(value)
        self.progressBar().show()

    def hideProgress(self):
        self.progressBar().hide()

    def showException(self, exception):
        """Raise message box showing exception inforamtion."""
        box = QtWidgets.QMessageBox(self)
        box.setIcon(box.Icon.Critical)
        box.setWindowTitle(self.tr("Error"))
        box.setText(format(exception))
        if hasattr(exception, 'details'):
            box.setDetailedText(format(exception.details))
        box.exec_()
        self.showMessage(self.tr("Error"))
        self.hideProgress()

    def connectProcess(self, process):
        """Connect process signals to main window slots."""
        process.failed.connect(self.showException)
        process.messageChanged.connect(self.showMessage)
        process.messageCleared.connect(self.clearMessage)
        process.progressChanged.connect(self.showProgress)
        process.progressHidden.connect(self.hideProgress)

    @QtCore.pyqtSlot(object)
    def closeEvent(self, event):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setText(self.tr("Quit application?"))
        dialog.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        dialog.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        dialog.exec_()

        if dialog.result() == dialog.Ok:
            self.closeRequest.emit()
            if self.processes:
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
        self.processes.stop()
        self.processes.join()
        super().close()

    def exec_(self):
        QtCore.QTimer.singleShot(250, self.close)
        return super().exec_()
