import os

from PyQt5 import QtWidgets

from comet.units import ureg
from comet.widgets import bootstrap, MainWindow

from ui_dashboard import Ui_Dashboard

class MainWindow(MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = QtWidgets.QWidget(self)
        w.ui = Ui_Dashboard()
        w.ui.setupUi(w)
        w.ui.doubleSpinBox.setUnit(ureg.Hz)
        w.ui.doubleSpinBox.valueChanged.connect(self.valueChanged)
        self.setCentralWidget(w)
        self.w = w

    def valueChanged(self):
        print(self.w.doubleSpinBox.value())

if __name__ == '__main__':
    bootstrap(MainWindow)
