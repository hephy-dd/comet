import logging
import os
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ..worker import WorkerRunnable

from .preferencesdialog import PreferencesDialog
from .aboutdialog import AboutDialog

__all__ = ['MainWindow']

Ui_MainWindow, MainWindowBase = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui', 'mainwindow.ui'))

class MainWindow(MainWindowBase):
    """Main window for COMET applications."""

    closeRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Setup status bar widgets
        self.__messageLabel = QtWidgets.QLabel(self)
        self.__messageLabel.hide()
        self.statusBar().addPermanentWidget(self.__messageLabel)
        self.__progressBar = QtWidgets.QProgressBar(self)
        self.__progressBar.hide()
        self.statusBar().addPermanentWidget(self.__progressBar)

    def showPreferences(self):
        """Show modal preferences dialog."""
        dialog = PreferencesDialog(self)
        dialog.exec_()

    def showContents(self):
        """Open local webbrowser with contets URL."""
        webbrowser.open(self.property('contentsUrl'))

    def showAbout(self):
        """Show modal about dialog."""
        dialog = AboutDialog(self)
        dialog.exec_()

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

    def raiseException(self, exception):
        """Raise message box showing exception inforamtion."""
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), format(exception))

    def connectWorker(self, worker):
        """Connect worker signals to main window slots."""
        self.closeRequested.connect(worker.stop)
        worker.exceptionOccured.connect(self.raiseException)
        worker.messageChanged.connect(self.showMessage)
        worker.messageCleared.connect(self.clearMessage)
        worker.progressChanged.connect(self.showProgress)
        worker.progressHidden.connect(self.hideProgress)

    def startWorker(self, worker):
        """Start worker in  global thread pool."""
        self.connectWorker(worker)
        logging.info("starting worker: %s", worker)
        QtCore.QThreadPool.globalInstance().start(WorkerRunnable(worker))

    def closeEvent(self, event):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setText("Quit application?");
        dialog.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        dialog.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        result = dialog.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            event.accept()
            self.closeRequested.emit()
        else:
            event.ignore()
