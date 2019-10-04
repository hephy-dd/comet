"""Simple spin box example."""

import sys
from PyQt5 import QtWidgets

import comet

class Widget(QtWidgets.QWidget, comet.UiLoaderMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadUi()
        self.ui.doubleSpinBox.valueChanged.connect(self.valueChanged)

    def valueChanged(self):
        print(self.ui.doubleSpinBox.value())

def main():
    app = comet.Application()
    window = comet.MainWindow()
    window.setCentralWidget(Widget())
    window.show()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
