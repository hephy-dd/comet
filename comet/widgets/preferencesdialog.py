from PyQt5 import QtCore, QtWidgets

from comet.settings import SettingsMixin
from comet.device import DeviceMixin
from comet.utils import escape_string, unescape_string

class ResourcesTab(QtWidgets.QWidget):

    DefaultReadTermination = '\n'

    DefaultWriteTermination = '\n'

    DefaultVisaLibrary = '@py'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Resources"))
        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.headerItem().setText(0, self.tr("Resource"))
        self.treeWidget.headerItem().setText(1, self.tr("Value"))
        self.treeWidget.itemDoubleClicked.connect(lambda item, column: self.editResource())
        self.treeWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.editButton = QtWidgets.QPushButton(self.tr("&Edit"))
        self.editButton.setEnabled(False)
        self.editButton.clicked.connect(self.editResource)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.treeWidget, 0, 0, 2, 1)
        layout.addWidget(self.editButton, 0, 1)
        layout.addItem(QtWidgets.QSpacerItem(0, 0), 1, 1)
        self.setLayout(layout)

    def resources(self):
        """Returns dictionary of resource options."""
        root = self.treeWidget.topLevelItem(0)
        resources = {}
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            name = item.text(0)
            options = {}
            for j in range(item.childCount()):
                child = item.child(j)
                key = child.text(0)
                value = child.text(1)
                if key in ['read_termination', 'write_termination']:
                    value = unescape_string(value)
                options[key] = value
            resources[name] = options
        return resources

    def setResources(self, resources):
        """Set dictionary of resource options."""
        self.treeWidget.clear()
        items = []
        for name, options in resources.items():
            item = QtWidgets.QTreeWidgetItem([name])
            item.addChild(QtWidgets.QTreeWidgetItem([
                'resource_name',
                options.get('resource_name')
            ]))
            item.addChild(QtWidgets.QTreeWidgetItem([
                'read_termination',
                escape_string(options.get('read_termination', self.DefaultReadTermination))
            ]))
            item.addChild(QtWidgets.QTreeWidgetItem([
                'write_termination',
                escape_string(options.get('write_termination', self.DefaultWriteTermination))
            ]))
            item.addChild(QtWidgets.QTreeWidgetItem([
                'visa_library',
                options.get('visa_library', self.DefaultVisaLibrary)
            ]))
            self.treeWidget.insertTopLevelItem(0, item)
            self.treeWidget.expandItem(item)
        self.treeWidget.resizeColumnToContents(0)

    @QtCore.pyqtSlot()
    def editResource(self):
        item = self.treeWidget.currentItem()
        if item.parent():
            text, ok = QtWidgets.QInputDialog.getText(
                self,
                self.tr("Resource {}").format(item.parent().text(0)),
                item.text(0),
                QtWidgets.QLineEdit.Normal,
                item.text(1)
            )
            if ok and text:
                item.setText(1, text)

    @QtCore.pyqtSlot()
    def selectionChanged(self):
        item = self.treeWidget.currentItem()
        self.editButton.setEnabled(item.parent() is not None)

class OperatorsTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Operators"))
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.itemDoubleClicked.connect(self.editOperator)
        self.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.addButton = QtWidgets.QPushButton(self.tr("&Add"))
        self.addButton.clicked.connect(self.addOperator)
        self.editButton = QtWidgets.QPushButton(self.tr("&Edit"))
        self.editButton.setEnabled(False)
        self.editButton.clicked.connect(self.editOperator)
        self.removeButton = QtWidgets.QPushButton(self.tr("&Remove"))
        self.removeButton.setEnabled(False)
        self.removeButton.clicked.connect(self.removeOperator)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.listWidget, 0, 0, 4, 1)
        layout.addWidget(self.addButton, 0, 1)
        layout.addWidget(self.editButton, 1, 1)
        layout.addWidget(self.removeButton, 2, 1)
        layout.addItem(QtWidgets.QSpacerItem(0, 0), 3, 1)
        self.setLayout(layout)

    def operators(self):
        """Returns list of operators."""
        return [self.listWidget.item(i).text() for i in range(self.listWidget.count())]

    def setOperators(self, operators):
        """Set list of operators."""
        self.listWidget.clear()
        for text in operators:
            self.listWidget.addItem(text)

    @QtCore.pyqtSlot()
    def addOperator(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self,
            self.tr("Operator"),
            self.tr("Name"),
            QtWidgets.QLineEdit.Normal
        )
        if ok and text:
            item = self.listWidget.addItem(text)
            self.listWidget.setCurrentItem(item)

    @QtCore.pyqtSlot()
    def editOperator(self):
        item = self.listWidget.currentItem()
        text, ok = QtWidgets.QInputDialog.getText(
            self,
            self.tr("Operator"),
            self.tr("Name"),
            QtWidgets.QLineEdit.Normal,
            item.text()
        )
        if ok and text:
            item.setText(text)

    @QtCore.pyqtSlot()
    def removeOperator(self):
        item = self.listWidget.currentItem()
        if item is not None:
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)

    @QtCore.pyqtSlot()
    def selectionChanged(self):
        item = self.listWidget.currentItem()
        self.editButton.setEnabled(item is not None)
        self.removeButton.setEnabled(item is not None)

class PreferencesDialog(QtWidgets.QDialog, DeviceMixin, SettingsMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Preferences"))
        self.resize(480, 320)
        self.tabWidget = QtWidgets.QTabWidget()
        self.resourcesTab = ResourcesTab()
        self.tabWidget.addTab(self.resourcesTab, self.resourcesTab.windowTitle())
        self.operatorsTab = OperatorsTab()
        self.tabWidget.addTab(self.operatorsTab, self.operatorsTab.windowTitle())
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel |
            QtWidgets.QDialogButtonBox.Apply |
            QtWidgets.QDialogButtonBox.RestoreDefaults
        )
        self.buttonBox.clicked.connect(self.handleButton)
        self.buttonBox.rejected.connect(self.reject)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.loadSettings()

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def handleButton(self, button):
        button = self.buttonBox.standardButton(button)
        if button == QtWidgets.QDialogButtonBox.Apply:
            self.saveSettings()
            QtWidgets.QMessageBox.information(self,
                self.tr("Preferences"),
                self.tr("Application restart required for changes to take effect.")
            )
            self.accept()
        if button == QtWidgets.QDialogButtonBox.RestoreDefaults:
            self.resetSettings()

    def saveSettings(self):
        self.settings['operators'] = self.operatorsTab.operators()
        self.settings['resources'] = self.resourcesTab.resources()

    def loadSettings(self):
        resources = {}
        for name, device in self.devices.items():
            options = {}
            options['resource_name'] = device.resource.resource_name
            options['read_termination'] = device.resource.options.get('read_termination', '\n')
            options['write_termination'] = device.resource.options.get('write_termination', '\n')
            options['visa_library'] = device.resource.visa_library
            resources[name] = options
        # Update default resources with stored settings
        for name, options in (self.settings.get('resources', {}) or {}).items():
            # Migrate old style settings
            if isinstance(options, str):
                options = {'resource_name': options}
            if name in resources:
                for key, value in options.items():
                    resources[name][key] = value
        self.resourcesTab.setResources(resources)
        operators = self.settings.get('operators', []) or [] # HACK
        self.operatorsTab.setOperators(operators)

    def resetSettings(self):
        self.operatorsTab.setOperators([])
        self.resourcesTab.setResources({})
