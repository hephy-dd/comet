"""Simple spin box eample assigning a unit from Pint unit registry."""

import os
from PyQt5 import QtWidgets, uic

import comet

Ui_Widget, WidgetBase = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'widget.ui'))

class Widget(WidgetBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.doubleSpinBox.setUnit(comet.ureg.Hz)
        self.ui.doubleSpinBox.valueChanged.connect(self.valueChanged)

    def valueChanged(self):
        print(self.ui.doubleSpinBox.value())

class MainWindow(comet.MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCentralWidget(Widget(self))

if __name__ == '__main__':
    app = comet.Application()
    app.addWindow(MainWindow())
    app.run()
