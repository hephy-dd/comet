---
layout: default
title: Processes
nav_order: 5
---

# Processes
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

* TOC
{: toc}

## Start

Time consuming operations or measurements need to be decoupled into threads to
keep the user interface responsive and usable. COMET provides class `Process`
for convenient thread handling.

```python
import comet

def run(process):
    pass # perform some task

process = comet.Process(target=run)
process.start()
```

## Request stop

COMET processes can be stopped by calling method `stop()`. This will put the
process in _stop-requested_ mode. Use properties `running` or `stopping` to
terminate the running process gracefully.

```python
import comet

def run(process):
    while process.running:
        pass # perform some task

process = comet.Process(target=run)
process.start()
...
process.stop()
process.join() # wait for process to stop
```

## Event callbacks

Class `Process` provides the following built in callbacks to provide
communication between worker thread and main thread:
* `started` is called immediately after `start()`
* `failed` is called if an exception was thrown, providing the exception and
 traceback object.
* `finished` is called immediately after running process ended, also if an
exception occurred.

```python
def on_finished():
    comet.show_info(title="My Process", text="Process finished!")
def on_error(exc, tb):
    comet.show_exception(exc, tb)

def run(process):
    raise RuntimeError("Spam!")

process = comet.Process(
    target=run,
    started=lambda: print("started..."),
    failed=on_error,
    finished=on_finished
)
process.start()
```

**Note:** Do not reference the user interface from within a process method, use
custom event callbacks to propagate information to the user interface (main
thread).

```python
def run(process):
    while process.running:
        process.emit('voltage', 24.00)
        process.emit('current', 0.05)

process = comet.Process(target=run)
process.voltage = update_voltage
process.current = update_current
```

## Register

Register all processes so that they will be stopped properly on application
exit.

```python
process = comet.Process()
process.start()
app.processes.add("process", process)
# `stop()` and `join()` is called on application exit
```
