from PyQt5 import QtWidgets
import pyqtgraph as pg

from .ui.plotwidget import Ui_PlotWidget

class PlotWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_PlotWidget()
        self.ui.setupUi(self)
        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        pw = pg.PlotWidget(self)
        vbox.addWidget(pw)
        self.plot = pw
        self.ui.plotArea.setLayout(vbox)
