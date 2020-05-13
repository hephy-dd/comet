from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .core import callback
from .widget import Widget

__all__ = [
    'Text',
    'Number',
    'Select',
    'List',
    'CheckBox',
    'Button'
]

class Input(Widget):

    pass

class Text(Input):

    QtBaseClass = QtWidgets.QLineEdit

    def __init__(self, value=None, readonly=False, clearable=False, changed=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.readonly = readonly
        self.clearable = clearable
        self.changed = changed
        self.qt.textChanged.connect(self.__changed_handler)

    @property
    def value(self):
        return self.qt.text()

    @value.setter
    def value(self, value):
        self.qt.setText("" if value is None else format(value))

    @property
    def readonly(self):
        return self.qt.isReadOnly()

    @value.setter
    def readonly(self, readonly):
        self.qt.setReadOnly(readonly)

    @property
    def clearable(self):
        return self.qt.clearButtonEnabled()

    @clearable.setter
    def clearable(self, clearable):
        self.qt.setClearButtonEnabled(clearable)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    @callback
    def __changed_handler(self, text):
        if callable(self.changed):
            self.changed(text)

class Number(Input):

    QtBaseClass = QtWidgets.QDoubleSpinBox

    prefix_format = "{} "
    suffix_format = " {}"

    def __init__(self, value=0, minimum=None, maximum=None, step=1, decimals=0, prefix=None, suffix=None, readonly=False, changed=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.minimum = -float('inf') if minimum is None else minimum
        self.maximum = float('inf') if maximum is None else maximum
        self.step = step
        self.decimals = decimals
        self.prefix = prefix
        self.suffix = suffix
        self.readonly = readonly
        self.changed = changed
        self.qt.valueChanged.connect(self.__changed_handler)

    @property
    def value(self):
        return self.qt.value()

    @value.setter
    def value(self, value):
        self.qt.setValue(value)

    @property
    def minimum(self):
        return self.qt.minimum()

    @minimum.setter
    def minimum(self, minimum):
        self.qt.setMinimum(minimum)

    @property
    def maximum(self):
        return self.qt.maximum()

    @maximum.setter
    def maximum(self, maximum):
        self.qt.setMaximum(maximum)

    @property
    def step(self):
        return self.qt.singleStep()

    @minimum.setter
    def step(self, step):
        self.qt.setSingleStep(step)

    @property
    def decimals(self):
        return self.qt.decimals()

    @decimals.setter
    def decimals(self, decimals):
        self.qt.setDecimals(decimals)

    @property
    def prefix(self):
        return self.qt.prefix().strip()

    @prefix.setter
    def prefix(self, prefix):
        if prefix is None:
            prefix = ""
        prefix = format(prefix).strip()
        if prefix:
            prefix = self.prefix_format.format(prefix)
        self.qt.setPrefix(prefix)

    @property
    def suffix(self):
        return self.qt.suffix().strip()

    @suffix.setter
    def suffix(self, suffix):
        if suffix is None:
            suffix = ""
        suffix = format(suffix).strip()
        if suffix:
            suffix = self.suffix_format.format(suffix)
        self.qt.setSuffix(suffix)

    @property
    def readonly(self):
        return self.qt.isReadOnly()

    @value.setter
    def readonly(self, readonly):
        self.qt.setReadOnly(readonly)
        if self.qt.isReadOnly():
            self.qt.setButtonSymbols(self.qt.NoButtons)
        else:
            self.qt.setButtonSymbols(self.qt.UpDownArrows)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    @callback
    def __changed_handler(self, value):
        if callable(self.changed):
            self.changed(value)

class Select(Input):

    QtBaseClass = QtWidgets.QComboBox

    def __init__(self, values=[], current=None, changed=None, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        if values and current is None:
            current = values[0]
        self.current = current
        self.changed = changed
        self.qt.currentIndexChanged.connect(self.__changed_handler)

    @property
    def values(self):
        return [self.qt.itemData(index) for index in range(self.qt.count())]

    @values.setter
    def values(self, values):
        self.clear()
        for value in values:
            self.append(value)

    def clear(self):
        self.qt.clear()

    def append(self, value):
        self.qt.addItem(format(value), value)

    def remove(self, value):
        self.qt.removeItem(self.qt.findData(value))

    @property
    def current(self):
        return self.qt.itemData(self.qt.currentIndex())

    @current.setter
    def current(self, value):
        index = self.qt.findData(value)
        self.qt.setCurrentIndex(index)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    @callback
    def __changed_handler(self, index):
        if callable(self.changed):
            value = self.values[index]
            self.changed(value)

class List(Input):

    QtBaseClass = QtWidgets.QListWidget

    def __init__(self, values=[], current=None, changed=None, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        if values and current is None:
            current = values[0]
        self.current = current
        self.changed = changed
        self.qt.currentRowChanged[int].connect(self.__changed_handler)

    @property
    def values(self):
        return [self.qt.item(index).data(QtCore.Qt.UserRole) for index in range(self.qt.count())]

    @values.setter
    def values(self, values):
        self.clear()
        for value in values:
            self.append(value)

    def clear(self):
        self.qt.clear()

    def append(self, value):
        item = QtWidgets.QListWidgetItem(format(value))
        item.setData(QtCore.Qt.UserRole, value)
        self.qt.addItem(item)

    def remove(self, value):
        for index, item in enumerate(self):
            if item == value:
                self.qt.takeItem(index)
                break

    @property
    def current(self):
        item = self.qt.item(self.qt.currentRow())
        if item:
            return item.data(QtCore.Qt.UserRole)

    @current.setter
    def current(self, value):
        self.qt.setCurrentRow(0)
        for index, item in enumerate(self):
            if value == item:
                self.qt.setCurrentRow(index)
                return

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    @callback
    def __changed_handler(self, index):
        if callable(self.changed):
            value = self.values[index]
            self.changed(value, index)

    def __getitem__(self, index):
        if index < 0:
            index += self.qt.count()
        item = self.qt.item(index)
        if item:
            return item.data(QtCore.Qt.UserRole)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        items = []
        for index in range(len(self)):
            items.append(self.qt.item(index).data(QtCore.Qt.UserRole))
        return iter(items)

class CheckBox(Input):

    QtBaseClass = QtWidgets.QCheckBox

    def __init__(self, text=None, checked=False, changed=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.checked = checked
        self.changed = changed
        self.qt.stateChanged.connect(self.__changed_handler)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, text):
        self.qt.setText("" if text is None else format(text))

    @property
    def checked(self):
        return self.qt.checkState() == QtCore.Qt.Checked

    @checked.setter
    def checked(self, checked):
        self.qt.setChecked(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    @callback
    def __changed_handler(self, state):
        if callable(self.changed):
            self.changed(state == QtCore.Qt.Checked)

class Button(Input):

    QtBaseClass = QtWidgets.QPushButton

    def __init__(self, text=None, checkable=False, checked=False, clicked=None, toggled=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setAutoDefault(False)
        self.qt.setDefault(False)
        self.text = text
        self.checkable = checkable
        self.checked = checked
        self.clicked = clicked
        self.toggled = toggled
        self.qt.clicked.connect(self.__clicked_handler)
        self.qt.toggled.connect(self.__toggled_handler)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, text):
        self.qt.setText("" if text is None else format(text))

    @property
    def checkable(self):
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, checkable):
        self.qt.setCheckable(bool(checkable))

    @property
    def checked(self):
        return self.qt.isChecked()

    @checked.setter
    def checked(self, checked):
        self.qt.setChecked(bool(checked))

    @property
    def clicked(self):
        return self.__clicked

    @clicked.setter
    def clicked(self, clicked):
        self.__clicked = clicked

    @callback
    def __clicked_handler(self, checked):
        if callable(self.clicked):
            self.clicked()

    @property
    def toggled(self):
        return self.__toggled

    @toggled.setter
    def toggled(self, toggled):
        self.__toggled = toggled

    @callback
    def __toggled_handler(self, checked):
        if callable(self.toggled):
            self.toggled(checked)
