"""Collection base class."""

from PyQt5 import QtCore

__all__ = ['Settings']

class Settings:
    """Application settings class."""

    def __init__(self, app):
        self.app = app

    def get(self, key, default=None):
        settings = QtCore.QSettings(self.app.organization_name, self.app.name)
        return settings.value(key, default)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        settings = QtCore.QSettings(self.app.organization_name, self.app.name)
        settings.setValue(key, value)
        settings.sync()
