import os
import json

from appdirs import user_config_dir

__all__ = ['Settings']

class Settings(object):
    """Settings context manager, storing persistent application settings on any
    platform.

    >>> with Settings('HEPHY', 'comet') as settings:
    ...    settings['operators'] = ['Monty', 'John']
    ...

    >>> with Settings('HEPHY', 'comet') as settings:
    ...    print(settings.get('operators'))
    ...
    ['Monty', 'John']

    Setting persistent to `False` prevents from writing settings to file.
    """

    default_filename = 'settings.json'
    """Filename used to store settings in JSON format."""

    def __init__(self, organization, application, persistent=True):
        self.__organization = organization
        self.__application = application
        self.__persistent = persistent
        path = user_config_dir(appname=application, appauthor=organization)
        self.__filename = os.path.join(path, self.default_filename)
        self.__settings = {}

    @property
    def organization(self):
        """Returns organization name."""
        return self.__organization

    @property
    def application(self):
        """Returns application name."""
        return self.__application

    @property
    def persistent(self):
        """Returns persistent option."""
        return self.__persistent

    @property
    def filename(self):
        """Returns settings path and filename."""
        return self.__filename

    def clear(self):
        """Clear settings file if exists."""
        if os.path.isfile(self.__filename):
            os.remove(self.__filename)

    def __enter__(self):
        """Read application settings from filesystem (if existing)."""
        if os.path.isfile(self.__filename):
            with open(self.__filename, 'r') as f:
                self.__settings = json.load(f)
        return self.__settings

    def __exit__(self, *exc):
        """Write application settings to filesystem."""
        if self.__persistent:
            path = os.path.dirname(self.__filename)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(self.__filename, 'w') as f:
                json.dump(self.__settings, f)
        return False
