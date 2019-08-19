from PyQt5 import QtCore

__all__ = ['Settings']

class Settings(QtCore.QObject):
    """Settings handler class wrapping QSettings.

    >>> s = Settings()
    >>> s.operators()
    []
    >>> s.addOperator('Monty')
    >>> s.operators()
    ['Monty']
    >>> s.devices()
    {}
    >>> s.setDevice('smu', 'GPIB::16::INSTR')
    >>> s.devices()
    {'smu': 'GPIB::16::INSTR'}
    """

    PreferencesGroupKey = 'preferences'

    InvertPlotsKey = 'invertPlots'
    VisaLibraryKey = 'visaLibrary'
    OperatorsKey = 'operators'
    CurrentOperatorKey = 'currentOperator'
    DevicesKey = 'devices'

    DefaultInvertPlots = False
    DefaultVisaLibrary = '@py'

    def __init__(self, parent=None):
        super().__init__(parent)
        organization = QtCore.QCoreApplication.organizationName()
        application = QtCore.QCoreApplication.applicationName()
        self.__settings = QtCore.QSettings(organization, application)
        self.__settings.beginGroup(self.PreferencesGroupKey)

    def invertPlots(self):
        """Returns True if invert plots is set."""
        return self.__settings.value(self.InvertPlotsKey, self.DefaultInvertPlots, type=bool)

    def setInvertPlots(self, inverted):
        self.__settings.setValue(self.InvertPlotsKey, inverted)
        self.__settings.sync()

    def visaLibrary(self):
        """Retruns VISA library."""
        return self.__settings.value(self.VisaLibraryKey, self.DefaultVisaLibrary, type=str)

    def setVisaLibrary(self, library):
        """Set VISA library."""
        self.__settings.setValue(self.VisaLibraryKey, library)
        self.__settings.sync()

    def operators(self):
        """Returns list of operators."""
        return self.__settings.value(self.OperatorsKey, [], type=list)

    def setOperators(self, operators):
        self.__settings.setValue(self.OperatorsKey, operators)
        self.__settings.sync()

    def addOperator(self, name):
        operators = self.operators()
        operators.append(name)
        self.setOperators(operators)

    def removeOperator(self, name):
        operators = self.operators()
        operators.remove(name)
        self.setOperators(operators)

    def currentOperator(self):
        """Returns current operator index or zero if not set."""
        return self.__settings.value(self.CurrentOperatorKey, 0, type=int)

    def setCurrentOperator(self, index):
        return self.__settings.setValue(self.CurrentOperatorKey, index)

    def devices(self):
        """Retruns list of device configurations."""
        return self.__settings.value(self.DevicesKey, {}, type=dict)

    def setDevices(self, devices):
        self.__settings.setValue(self.DevicesKey, devices)
        self.__settings.sync()

    def setDevice(self, name, resource):
        """Set device resource by name."""
        devices = self.devices()
        devices[name] = resource
        self.setDevices(devices)

    def removeDevice(self, name):
        """Remove device by name."""
        devices = self.devices()
        devices.pop(name, None)
        self.setDevices(devices)
