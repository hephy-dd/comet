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
        invertPlots = settings.value('invertPlots', False, type=bool)
        operators = settings.value('operators', [], type=list)
        devices = settings.value('devices', [], type=list)
        settings.endGroup()
        self.ui.invertPlotsCheckBox.setChecked((invertPlots))
        self.ui.operatorListWidget.clear()
        self.ui.operatorListWidget.addItems(operators)
        self.ui.devicesTableWidget.clearContents()
        self.ui.devicesTableWidget.setRowCount(len(devices));
        for i, device in enumerate(devices):
            name, resource = device.split(';')
            self.ui.devicesTableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(device[0]))
            self.ui.devicesTableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(device[1]))

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('preferences')
        settings.setValue('invertPlots', self.invertPlots())
        settings.setValue('operators', self.operators())
        settings.setValue('devices', self.devices())
        settings.endGroup()

    def accept(self):
        self.saveSettings()
        super().accept()

    def invertPlots(self):
        """Returns selected state of invert plot check box."""
        return self.ui.invertPlotsCheckBox.isChecked()

    def operators(self):
        """Returns current list of operators."""
        operators = []
        for row in range(self.ui.operatorListWidget.count()):
            operators.append(self.ui.operatorListWidget.item(row).text())
        return operators

    def devices(self):
        """Returns list of devices containing name and resource."""
        return []

    def addOperator(self):
        """Add operator slot."""
        text, ok = QtWidgets.QInputDialog.getText(self,
                self.tr("Operator"),
                self.tr("Name:"),
                QtWidgets.QLineEdit.Normal
            )
        if ok and text:
            item = self.ui.operatorListWidget.addItem(text)
            self.ui.operatorListWidget.setCurrentItem(item)

    def editOperator(self):
        """Edit operator slot."""
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
        """Remove operator slot."""
        row = self.ui.operatorListWidget.currentRow()
        if row is not None:
            self.ui.operatorListWidget.takeItem(row)
