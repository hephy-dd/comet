import os

from PyQt5 import QtWidgets, uic
import pyqtgraph as pg

Ui_LinePlotWidget, LinePlotWidgetBase = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui', 'lineplotwidget.ui'))

class LinePlotWidget(LinePlotWidgetBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_LinePlotWidget()
        self.ui.setupUi(self)
