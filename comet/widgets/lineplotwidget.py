import os

from PyQt5 import QtWidgets, uic
import pyqtgraph as pg

Ui_LinePlotWidget, LinePlotWidgetBase = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')

class LinePlotWidget(LinePlotWidgetBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_LinePlotWidget()
        self.ui.setupUi(self)
