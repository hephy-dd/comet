---
layout: default
title: Processes
nav_order: 5
---

# Processes

Time consuming operations or measurements need to be decoupled into threads to
keep the user interface responsive and usable. COMET provides class `Process`
for convenient thread handling.

```python
import comet

class MyProcess(comet.Process):
    def run(self):
        pass # perform some task

process = MyProcess()
process.start()
```

## Request stop

COMET processes can be stopped by calling method `stop()`. This will put the
process in _stop-requested_ mode. Use property `running` to terminate the
running process gracefully.

```python
import comet

class MyProcess(comet.Process):
    def run(self):
        while self.running:
          pass # perform some task

process = MyProcess()
process.start()
...
process.stop()
process.join() # wait for process to stop
```

## Callbacks

Class `Process` provides the following built in callbacks to provide
inter-thread  communication:
* `started` is called immediately after `start()`
* `failed` is called if an exception was thrown, providing the exception and
 traceback object.
* `finished` is called immediately after running process ended, also if an
exception occurred.

```python
class MyProcess(comet.Process):
    def run(self):
        raise RuntimeError("Spam!")

def on_finished():
    comet.show_info(title="My Process", text="Process finished!")
def on_error(exc, tb):
    comet.show_exception(exc, tb)

process = MyProcess(
  finished=on_finished,
  failed=on_error
)
process.start()
```

**Note:** Do not reference the UI from within method `run()`, use custom
callbacks to propagate information to the UI.

```python
class MyProcess(comet.Process):
    def run(self):
        while self.running:
            self.push("voltage", 24.00)
            self.push("current", 0.05)

process = MyProcess(
  voltage=update_voltage,
  current=update_current
)
```

## Register

Register all processes so that they will be stopped properly on application exit.

```python
process = MyProcess()
process.start()
app.processes.add("process", process)
# `stop()` and `join()` is called on exit
```
