from PyQt5 import QtCore, QtWidgets

from .core import Event
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

    def __init__(self, value=None, readonly=False, clearable=False, change=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.readonly = readonly
        self.clearable = clearable
        self.change = change
        self.qt.textChanged.connect(self.__change_handler)

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
    def change(self):
        return self.__change

    @change.setter
    def change(self, change):
        self.__change = change

    def __change_handler(self, text):
        if callable(self.change):
            self.change(Event(self, text=text))

class Number(Input):

    QtBaseClass = QtWidgets.QDoubleSpinBox

    prefix_format = "{} "
    suffix_format = " {}"

    def __init__(self, value=0, minimum=0, maximum=100, step=1, decimals=0, prefix=None, suffix=None, readonly=False, change=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.decimals = decimals
        self.prefix = prefix
        self.suffix = suffix
        self.readonly = readonly
        self.change = change
        self.qt.valueChanged.connect(self.__change_handler)

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
    def change(self):
        return self.__change

    @change.setter
    def change(self, change):
        self.__change = change

    def __change_handler(self, value):
        if callable(self.change):
            self.change(Event(self, value=value))

class Select(Input):

    QtBaseClass = QtWidgets.QComboBox

    def __init__(self, values=None, default=None, change=None, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        self.default = default
        self.change = change
        self.qt.currentIndexChanged.connect(self.__change_handler)

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
        self.qt.removeItem(self.qt.findData(default))

    @property
    def selected(self):
        return self.qt.itemData(self.qt.currentIndex())

    @property
    def default(self):
        return self.__default

    @default.setter
    def default(self, default):
        self.__default = default
        index = self.qt.findData(default)
        self.qt.setCurrentIndex(index)

    @property
    def change(self):
        return self.__change

    @change.setter
    def change(self, change):
        self.__change = change

    def __change_handler(self, index):
        if callable(self.change):
            value = self.values[index]
            self.change(Event(self, value=value, index=index))

class List(Input):

    QtBaseClass = QtWidgets.QListWidget

    def __init__(self, values=None, default=None, change=None, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        self.default = default
        self.change = change
        self.qt.currentRowChanged[int].connect(self.__change_handler)

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
        self.qt.removeItem(self.qt.findData(default))

    @property
    def change(self):
        return self.__change

    @change.setter
    def change(self, change):
        self.__change = change

    def __change_handler(self, index):
        if callable(self.change):
            value = self.values[index]
            self.change(Event(self, value=value, index=index))

class CheckBox(Input):

    QtBaseClass = QtWidgets.QCheckBox

    def __init__(self, text=None, checked=False, change=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.checked = checked
        self.change = change
        self.qt.stateChanged.connect(self.__change_handler)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, text):
        self.qt.setText("" if text is None else format(text))

    @property
    def checked(self):
        return self.qt.state() == QtCore.Qt.Checked

    @checked.setter
    def checked(self, checked):
        self.qt.setChecked(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)

    @property
    def change(self):
        return self.__change

    @change.setter
    def change(self, change):
        self.__change = change

    def __change_handler(self, state):
        if callable(self.change):
            self.change(Event(self, checked=state==QtCore.Qt.Checked))

class Button(Input):

    QtBaseClass = QtWidgets.QPushButton

    def __init__(self, text=None, checkable=False, checked=False, click=None, toggle=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setAutoDefault(False)
        self.qt.setDefault(False)
        self.text = text
        self.checkable = checkable
        self.checked = checked
        self.click = click
        self.toggle = toggle
        self.qt.clicked.connect(self.__click_handler)
        self.qt.toggled.connect(self.__toggle_handler)

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
    def click(self):
        return self.__click

    @click.setter
    def click(self, click):
        self.__click = click

    def __click_handler(self, checked):
        if callable(self.click):
            self.click(Event(self, checked=checked))

    @property
    def toggle(self):
        return self.__toggle

    @toggle.setter
    def toggle(self, toggle):
        self.__toggle = toggle

    def __toggle_handler(self, checked):
        if callable(self.toggle):
            self.toggle(Event(self, checked=checked))
