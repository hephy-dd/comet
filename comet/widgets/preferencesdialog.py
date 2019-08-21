import os
from PyQt5 import QtCore, QtWidgets, uic

from ..settings import Settings

Ui_PreferencesDialog, PreferencesDialogBase = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')

__all__ = ['PreferencesDialog']

class PreferencesDialog(PreferencesDialogBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.loadSettings()

    def loadSettings(self):
        # Load settings
        settings = Settings()

        self.ui.invertPlotsCheckBox.setChecked((settings.invertPlots()))

        self.ui.visaComboBox.setCurrentText(settings.visaLibrary())

        self.ui.operatorListWidget.clear()
        self.ui.operatorListWidget.addItems(settings.operators())

        self.ui.devicesTableWidget.clearContents()
        self.ui.devicesTableWidget.setRowCount(len(settings.devices()))
        for i, device in enumerate(settings.devices().items()):
            name, resource = device
            self.ui.devicesTableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.devicesTableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(format(resource)))
        self.ui.devicesTableWidget.resizeRowsToContents()
        self.ui.devicesTableWidget.resizeColumnsToContents()

        self.ui.operatorListWidget.itemSelectionChanged.connect(self.updateOperatorButtons)
        self.ui.devicesTableWidget.itemSelectionChanged.connect(self.updateDeviceButtons)

    def updateOperatorButtons(self):
        select = self.ui.operatorListWidget.selectionModel()
        self.ui.editOperatorPushButton.setEnabled(select.hasSelection())
        self.ui.removeOperatorPushButton.setEnabled(select.hasSelection())

    def updateDeviceButtons(self):
        select = self.ui.devicesTableWidget.selectionModel()
        self.ui.editDevicePushButton.setEnabled(select.hasSelection())

    def saveSettings(self):
        settings = Settings()
        settings.setInvertPlots(self.invertPlots())
        settings.setVisaLibrary(self.visaLibrary())
        settings.setOperators(self.operators())
        settings.setDevices(self.devices())

    def accept(self):
        self.saveSettings()
        QtWidgets.QMessageBox.information(self,
            self.tr("Preferences"),
            self.tr("Application restart required for changes to take effect.")
        )
        super().accept()

    def invertPlots(self):
        """Returns selected state of invert plot check box."""
        return self.ui.invertPlotsCheckBox.isChecked()

    def visaLibrary(self):
        """Returns selected state of VISA library combo box."""
        return self.ui.visaComboBox.currentText()

    def operators(self):
        """Returns current list of operators."""
        table = self.ui.operatorListWidget
        operators = []
        for row in range(table.count()):
            operators.append(table.item(row).text())
        return operators

    def devices(self):
        """Returns list of devices containing name and resource."""
        table = self.ui.devicesTableWidget
        devices = {}
        for row in range(table.rowCount()):
            name = table.item(row, 0).text()
            resource = table.item(row, 1).text()
            devices[name] =resource
        return devices

    def addOperator(self):
        """Add operator slot."""
        text, ok = QtWidgets.QInputDialog.getText(self,
                self.tr("Operator"),
                self.tr("Name:"),
                QtWidgets.QLineEdit.Normal
            )
        if ok and text:
            table = self.ui.operatorListWidget
            item = table.addItem(text)
            table.setCurrentItem(item)

    def editOperator(self):
        """Edit operator slot."""
        item = self.ui.operatorListWidget.currentItem()
        if item is not None:
            text, ok = QtWidgets.QInputDialog.getText(self,
                self.tr("Operator"),
                self.tr("Name:"),
                QtWidgets.QLineEdit.Normal,
                item.text()
            )
            if ok:
                item.setText(text)

    def removeOperator(self):
        """Remove operator slot."""
        table = self.ui.operatorListWidget
        row = table.currentRow()
        if row is not None:
            table.takeItem(row)

    def editDevice(self):
        """Edit device resource slot."""
        table = self.ui.devicesTableWidget
        row = table.currentRow()
        item = table.item(row, 1)
        if item is not None:
            text, ok = QtWidgets.QInputDialog.getText(self,
                self.tr("Device"),
                self.tr("Resource:"),
                QtWidgets.QLineEdit.Normal,
                item.text()
            )
            if ok:
                item.setText(text)
