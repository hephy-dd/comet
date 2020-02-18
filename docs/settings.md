---
layout: default
title: Settings
nav_order: 5
---

## Namespace

To be able to store persistent settings you have to set an application name.
This will create an application configuration file in an OS dependent location.

```python
app.name = "example" # stores settings in `HEPHY/example.conf` (location is OS depended)
```

## Access

Settings can be accessed using the applications `settings` property. Changes
will be stored automatically on application exit.

```python
>>> app.settings["spam"] = 42
>>> app.settings.get("spam")
42
```

## Mixins

Inherit from class `SettingsMixin` to provide access to persistent application
settings from within custom classes.

```python
from comet.settings import SettingsMixin

class Custard(SettingsMixin):
    @property
    def spam(self):
        return self.settings.get("spam")
    @spam.setter
    def spam(self, value):
        return self.settings["spam"] = value
```

List of classes that inherit `SettingsMixin`:
* [`Application`](application.md)
