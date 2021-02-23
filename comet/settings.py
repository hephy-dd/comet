"""Collection base class."""

import threading
from qutie.settings import Settings

__all__ = ['Settings', 'SettingsManager', 'SettingsMixin']

class SettingsManager:
    """Settings manager wrapping qutie.Settings."""

    lock = threading.RLock()

    def get(self, key, default=None):
        with self.lock:
            with Settings() as settings:
                return settings.get(key, default)

    def __getitem__(self, key):
        with self.lock:
            with Settings() as settings:
                return settings[key]

    def __setitem__(self, key, value):
        with self.lock:
            with Settings() as settings:
                settings[key] = value

    @property
    def filename(self):
        with self.lock:
            return Settings().filename

class SettingsMixin:
    """Mixin class to access global settings manager."""

    __settings = SettingsManager()

    @property
    def settings(self):
        return type(self).__settings
