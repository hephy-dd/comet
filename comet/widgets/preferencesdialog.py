from PyQt5 import QtCore, QtWidgets

from .ui.preferencesdialog import Ui_PreferencesDialog

__all__ = ['PreferencesDialog']

class PreferencesDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.loadSettings()

    def loadSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('preferences')
        operators = settings.value('operators', [])
        settings.endGroup()
        self.ui.operatorListWidget.clear()
        self.ui.operatorListWidget.addItems(operators)

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('preferences')
        settings.setValue('operators', self.operators())
        settings.endGroup()

    def accept(self):
        self.saveSettings()
        super().accept()

    def operators(self):
        operators = []
        for row in range(self.ui.operatorListWidget.count()):
            operators.append(self.ui.operatorListWidget.item(row).text())
        return operators

    def addOperator(self):
        text, ok = QtWidgets.QInputDialog.getText(self,
                self.tr("Operator"),
                self.tr("Name:"),
                QtWidgets.QLineEdit.Normal
            )
        if ok and text:
            item = self.ui.operatorListWidget.addItem(text)
            self.ui.operatorListWidget.setCurrentItem(item)

    def editOperator(self):
        item = self.ui.operatorListWidget.currentItem()
        if item is not None:
            text, ok = QtWidgets.QInputDialog.getText(self,
                self.tr("Operator"),
                self.tr("Name:"),
                QtWidgets.QLineEdit.Normal,
                self.ui.operatorListWidget.currentItem().text()
            )
            if ok:
                self.ui.operatorListWidget.currentItem().setText(text)

    def removeOperator(self):
        row = self.ui.operatorListWidget.currentRow()
        if row is not None:
            self.ui.operatorListWidget.takeItem(row)

