import os

from PyQt5 import QtWidgets, uic

from comet.units import ureg
from comet.widgets import Application, MainWindow

Ui_Widget, Widget = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'widget.ui'))

class Widget(Widget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.doubleSpinBox.setUnit(ureg.Hz)
        self.ui.doubleSpinBox.valueChanged.connect(self.valueChanged)

    def valueChanged(self):
        print(self.ui.doubleSpinBox.value())

class MainWindow(MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCentralWidget(Widget(self))

if __name__ == '__main__':
    app = Application()
    app.ApplicationName = 'CometExamplesSimple'
    app.MainWindowClass = MainWindow
    app.run()
