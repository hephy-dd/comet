import logging
import signal
import sys
import webbrowser

from PyQt5 import QtCore, QtWidgets

from .preferencesdialog import PreferencesDialog
from .aboutdialog import AboutDialog

from .ui.mainwindow import Ui_MainWindow

__all__ = ['MainWindow', 'bootstrap']

class MainWindow(QtWidgets.QMainWindow):

    ContentsUrl = 'https://github.com/hephy-dd/comet/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def showPreferences(self):
        """Show modal preferences dialog."""
        dialog = PreferencesDialog(self)
        dialog.exec_()

    def showContents(self):
        """Open local webbrowser with contets URL."""
        webbrowser.open(self.ContentsUrl)

    def showAbout(self):
        """Show modal about dialog."""
        dialog = AboutDialog(self)
        dialog.exec_()

def bootstrap(cls, logging_level=logging.INFO):

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging_level)

    app = QtWidgets.QApplication(sys.argv)

    w = cls()
    w.show()

    # Terminate application on SIG_INT signal.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Run timer to catch SIG_INT signals.
    timer = QtCore.QTimer()
    timer.start(250)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())
