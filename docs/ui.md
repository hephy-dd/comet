---
layout: default
title: UI
nav_order: 3
---

# UI elements
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

* TOC
{: toc}

## Inputs

### Button

A simple push button, inheriting class `Widget`.

```python
comet.Button(
  text="Click Me!",
  clicked=lambda: print("clicked!")
)
```

Properties:
* `text`: button text, default is empty
* `checkable`: button is a check button
* `checked`: button check state
* `icon`: button icon, default is empty

Callbacks:
* `clicked`: on button click
* `toggled`: on button toggle, passes argument `toggled`
* `pressed`: on button press
* `released`: on button release

### Number

A numeric input, inheriting class `Widget`.

```python
comet.Number(
  value=4.2,
  minimum=0.0,
  maximum=10.0,
  changed=lambda value: print("value changed:", value)
)
```

Properties:
* `value`: current value, default is `0`
* `minimum`: minimum value, default is `-inf`
* `maximum`: maximum value, default is `+inf`
* `step`: single step, default is `1.0`
* `decimals`: number of decimals, default is `0`
* `prefix`: prefix text, default is empty
* `suffix`: suffix text, default is empty
* `readonly`: read only number, default is `False`
* `adaptive`: adaptive steps depending on value, default is `False`
* `special_value`: special text shown instead lowest value, default is empty

Callbacks:
* `changed`: on value change, passes argument `value`
* `editing_finished`: on enter or changing focus

### Text

A single line text input, inheriting class `Widget`.

```python
comet.Text(
  value="Lorem ipsum"
  changed=lambda value: print("value changed:", value)
)
```

Properties:
* `value`: current value, default is an empty string
* `readonly`: read only text, default is `False`
* `clearable`: shows clear button, default is `False`

Callbacks:
* `changed`: on value change, passes argument `value`
* `editing_finished`: on enter or changing focus

### TextArea

A multi-line text input, inheriting class `Widget`.

```python
comet.TextArea(
  value="Lorem ipsum\net dolor."
  changed=lambda value: print("value changed:", value)
)
```

Properties:
* `value`: current value, default is an empty string
* `readonly`: read only text, default is `False`
* `richtext`: shows rich text content, default is `False`

Methods:
* `append(text)`: append text as paragraph to current value
* `insert(text)`: insert text at current cursor position
* `clear()`: clear contents


## List

A simple list widget, inheriting class `Widget`.

```python
comet.List(
  items=["spam", "ham"]
)
l.append("eggs")
l.insert(0, "apples")
for item in l:
    print(item.value)
```

## Tree

A simple tree widget, inheriting class `Widget`.

```python
tree = comet.Tree(
  header=["Key", "Value"]
)
tree.insert(0, ["spam", .42])
item = tree.append(["ham", 4.2])
item.append(["eggs", 42.])
for item in tree:
    print(item.value)
```

## Table

A simple table widget, inheriting class `Widget`.

```python
table = comet.Table(
  header=["Key", "Value"]
)
table.append(["spam", .42])
table.append(["ham", 4.2])
table.insert(0, ["eggs", 42.])
for row in table:
    for item in row:
      print(item.value)
```

## Layout

Create row and column layouts by assigning contents directly. This allows to
construct complex layouts with ease.

### Row

A horizontal layout, inheriting class `Widget`.

```python
comet.Row(
  element1, element2, element3,
  stretch=(1, 2, 3) # horizontal stretch ratio of elements
)
```

### Column

A vertical layout, inheriting class `Widget`.

```python
comet.Column(
  element1, element2, element3,
  stretch=(1, 2, 3) # vertical stretch ratio of elements
)
```

### Spacer

An expanding spacer element for stretching spaces, inheriting class `Widget`.

```python
comet.Column(
  top_element,
  comet.Spacer(),
  bottom_element
)
```
