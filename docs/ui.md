---
layout: default
title: UI
nav_order: 3
---

# UI elements

## Layout

### Row

A horizontal layout

```python
comet.Row(
  element1, element2, element3,
  stretch=(1, 2, 3) # horizontal stretch ratio of elements
)
```

### Column

A vertical layout

```python
comet.Column(
  element1, element2, element3,
  stretch=(1, 2, 3) # vertical stretch ratio of elements
)
```

### Stretch

An expanding stretch element for spaces.

```python
comet.Column(
  top_element,
  comet.Stretch(),
  bottom_element
)
```

## Inputs

### Button

A simple push button.

```python
comet.Button(
  text="Click Me!",
  clicked=lambda: print("clicked!")
)
```

Callbacks:
* `clicked`: on button click
* `toggled`: on button toggle, passes argument `toggled`
