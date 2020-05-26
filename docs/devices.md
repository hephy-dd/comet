---
layout: default
title: Devices
nav_order: 4
---

# Devices
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

* TOC
{: toc}

## Resources

VISA based instrument communication is handled by class `Resource` that is used
as context manager to guarantee releasing of instrument connections.

```python
# Create and open a bare resource
>>> with comet.Resource("GBIP::1::INSTR") as resource:
...     print(resource.query("*IDN?"))
...
'Keithley, Model 2410, ...'
```

Class `Resource` accepts VISA compatible arguments.

```python
# Create a bare VISA resource
>>> resource = comet.Resource(
...   resource_name="GBIP::1::INSTR",
...   visa_library="@py",
...   read_termination="\n",
...   write_termination="\n"
... )
```

## Drivers

Devices are instances inheriting from class `Driver` using a resource
instance `Resource` for VISA communication with compliant instruments.

COMET comes with a set of various instrument drivers in module `comet.driver`.

```python
# Create a device using a resource
>>> from comet.driver.keithley import K2410
>>> with K2410("GBIP::1::INSTR") as device:
...     device.source.voltage = 5.00
...     print(device.source.voltage)
...
5.0
```

Drivers can be constructed either by `Resource` instances or by arguments, that
will generate a `Resource` instance on the fly.

```python
>>> comet.Driver("GBIP::1::INSTR", read_termination="\n")
```

This is equivalent of the following statement.

```python
>>> resource = comet.Resource("GBIP::1::INSTR", read_termination="\n")
>>> comet.Driver(resource)
```

## Registering

Registering resources brings following advantages:
* Rssources can be accesses using the `resources` property by any class
inheriting from class `ResourceMixin`.
* Persistent resource settings can be edited using the main window's preferences
dialog.
* Stored settings can be applied to registered devices using `load_settings()`.

```python
# Register a device instance
>>> app.resources.add("name", device)
# Access a registerd device
>>> app.resources.get("name")
<Driver object at ...>
```

## Load settings

```python
app.resources.add("smu", comet.Resource("GBIP::1::INSTR"))
app.resources.add("multi", comet.Resource("GBIP::2::INSTR"))
app.resources.load_settings() # overwrite above resources with persistent settings
```

## Mixins

Inherit from class `ResourceMixin` to provide access to persistent application
settings from within custom classes.

```python
from comet.resource import ResourceMixin

class Custard(ResourceMixin):
    @property
    def spam(self):
        return self.resources.get("spam")
```

List of classes that inherit `ResourceMixin`:
* [`Application`](application.md)
* [`Process`](processes.md)
