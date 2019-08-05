from PyQt5 import QtWidgets
import pyqtgraph as pg

from .ui.lineplotwidget import Ui_linePlotWidget

class LinePlotWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_linePlotWidget()
        self.ui.setupUi(self)
