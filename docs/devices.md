---
layout: default
title: Devices
nav_order: 4
---

# Devices

## Quick start

Devices are class instances inheriting from `Driver` using a resource
instance `Resource` for VISA communication with compliant instruments.

COMET comes with a set of various instrument drivers in module `comet.driver`.

```python
# Create a bare VISA resource
>>> import comet
>>> resource = comet.Resource(
...   resource_name="GBIP::1::INSTR",
...   visa_library="@py",
...   read_termination="\n",
...   write_termination="\n")

>>> resource.query("*IDN?")
'Keithely, Model 2410, ...'

# Create a device using a resource
>>> from comet.driver.keithley import K2410
>>> device = K2410(resource)
>>> device.identification
'Keithely, Model 2410, ...'
>>> device.source.voltage = 5.00
>>> device.source.voltage
5.0
```

## Register

Registering devices brings following advantages:
* Devices can be accesses using the `devices` proeprty by any class inheriting
from class `DeviceMixin`.
* Persistent device settings can be edited using the main window's preferences
dialog.
* Stored settings can be applied to registered devices using `load_settings()`.

```python
# Register a device instance
>>> app.devices.add("name", device)
# Access a registerd device
>>> app.devices.get("name")
<Driver object at ...>
```

## Load settings

```python
app.devices.add("smu", K2410(comet.Resource("GBIP::1::INSTR")))
app.devices.add("multi", K2700(comet.Resource("GBIP::2::INSTR")))
app.devices.load_settings() # overwrite above resources with persistent settings
```

## Mixins

Inherit from class `DeviceMixin` to provide access to persistent application
settings from within custom classes.

```python
from comet.device import DeviceMixin

class Custard(DeviceMixin):
    @property
    def spam(self):
        return self.devices.get("spam")
```

List of classes that inherit `DeviceMixin`:
* [`Application`](application.md)
* [`Process`](processes.md)
