import os
from PyQt5 import QtCore, QtWidgets, uic

from ..mixins import UiLoaderMixin
from ..device import DeviceMixin

__all__ = ['PreferencesDialog']

class PreferencesDialog(QtWidgets.QDialog, UiLoaderMixin, DeviceMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loadUi()
        self.loadSettings()

    def loadSettings(self):
        # Load settings
        settings = QtCore.QSettings()

        visaLibrary = settings.value('visaLibrary', '@py')
        self.ui.visaComboBox.setCurrentText(visaLibrary)

        operators = settings.value('operators', []) or [] # HACK
        self.ui.operatorListWidget.clear()
        self.ui.operatorListWidget.addItems(operators)

        resources = settings.value('resources', {})
        resources.update(self.devices().resources())
        self.ui.resourcesTableWidget.clearContents()
        self.ui.resourcesTableWidget.setRowCount(len(resources))
        for i, resource in enumerate(resources.items()):
            name, resource = resource
            self.ui.resourcesTableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.resourcesTableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(resource))
        self.ui.resourcesTableWidget.resizeRowsToContents()
        self.ui.resourcesTableWidget.resizeColumnsToContents()

        self.ui.operatorListWidget.itemSelectionChanged.connect(self.updateOperatorButtons)
        self.ui.resourcesTableWidget.itemSelectionChanged.connect(self.updateResourceButtons)

    def updateOperatorButtons(self):
        select = self.ui.operatorListWidget.selectionModel()
        self.ui.editOperatorPushButton.setEnabled(select.hasSelection())
        self.ui.removeOperatorPushButton.setEnabled(select.hasSelection())

    def updateResourceButtons(self):
        select = self.ui.resourcesTableWidget.selectionModel()
        self.ui.editResourcePushButton.setEnabled(select.hasSelection())

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue('visaLibrary', self.visaLibrary())
        settings.setValue('operators', self.operators())
        settings.setValue('resources', self.resources())

    def accept(self):
        self.saveSettings()
        QtWidgets.QMessageBox.information(self,
            self.tr("Preferences"),
            self.tr("Application restart required for changes to take effect.")
        )
        super().accept()

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

    def resources(self):
        """Returns list of resources containing name and resource."""
        table = self.ui.resourcesTableWidget
        resources = {}
        for row in range(table.rowCount()):
            name = table.item(row, 0).text()
            resource = table.item(row, 1).text()
            resources[name] = resource
        return resources

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

    def editResource(self):
        """Edit device resource slot."""
        table = self.ui.resourcesTableWidget
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
