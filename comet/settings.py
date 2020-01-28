"""Collection base class."""

from PyQt5 import QtCore

__all__ = ['SettingsManager', 'SettingsMixin']

class SettingsManager:
    """Settings manager wrapping QSettings. To syncronize with changes to the
    organization/application name it creates a new instance on every access.
    """

    def get(self, key, default=None):
        settings = QtCore.QSettings(
            QtCore.QCoreApplication.organizationName(),
            QtCore.QCoreApplication.applicationName()
        )
        return settings.value(key, default)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        settings = QtCore.QSettings(
            QtCore.QCoreApplication.organizationName(),
            QtCore.QCoreApplication.applicationName()
        )
        settings.setValue(key, value)
        settings.sync()

class SettingsMixin:
    """Mixin class to access global settings manager."""

    __settings = SettingsManager()

    @property
    def settings(self):
        return self.__class__.__settings
