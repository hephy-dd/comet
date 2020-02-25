---
layout: default
title: Application
nav_order: 1
---

## Create application

The application object permits to register devices, processes and the main window layout.

```python
import comet

app = comet.Application()
app.version = "1.0"
app.title = "Example"
app.description = "An example application."

app.run()
```

## Layout

The application object provides a main window, use property `layout` to assign
[UI elements](ui.md).

```python
app.layout = comet.Column(
    comet.Text(value="Spam"),
    comet.Button(text="Click")
)
```