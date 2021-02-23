import time

from comet.driver import lock
from comet.driver import Driver

__all__ = ['TSP']

def opc_wait(function):
    """Decorator function, locks the resource and waits for `waitcomplete()`
    after function execution.
    """
    @lock
    def opc_wait(instance, *args, **kwargs):
        result = function(instance, *args, **kwargs)
        instance.resource.write('waitcomplete()')
        if not bool(instance.resource.query('print([[1]])')):
            raise RuntimeError("failed to wait for operation complete")
        return result
    return opc_wait

def opc_poll(function, interval=.250, retries=40):
    """Decorator function, locks the resource, writes `eventlog.clear()`,
    `status.clear()` and `opc()` before the function call and polls after
    function execution for `print(status.standard.event)` bit 0 to be set.
    """
    @lock
    def opc_poll(instance, *args, **kwargs):
        instance.resource.write('eventlog.clear()')
        instance.resource.write('status.clear()')
        instance.resource.write('opc()')
        result = function(instance, *args, **kwargs)
        for i in range(retries):
            if int(instance.resource.query('print(status.standard.event)')) & 0x1:
                return result
            time.sleep(interval)
        raise RuntimeError("failed to poll for event status")
    return opc_poll

class TSP(Driver):
    """TSP compatible intrument driver."""

    @property
    @lock
    def identification(self) -> str:
        """Returns instrument identification."""
        return ', '.join((
            self.resource.query('print(localnode.model)'),
            self.resource.query('print(localnode.serialno)'),
            self.resource.query('print(localnode.version)')
        )).strip()

    @property
    def event_status(self) -> int:
        """Returns event status."""
        return int(self.resource.query('print(status.standard.event)'))

    @property
    def event_status_enable(self) -> int:
        """Returns event status enable register."""
        return int(self.resource.query('print(status.standard.enable)'))

    @event_status_enable.setter
    def event_status_enable(self, value: int):
        """Set event status enable register."""
        self.resource.write(f'status.standard.enable = {value:d}')

    @property
    def status(self) -> int:
        """Returns status register."""
        return int(self.resource.query('print(status.condition)'))

    @property
    @lock
    def operation_complete(self) -> bool:
        """Retruns operation complete state."""
        self.resource.write('waitcomplete()')
        return bool(self.resource.query('print([[1]])'))

    def complete_operation(self):
        """Sets the operation complete bit of the event status register."""
        self.resource.write('opc()')

    @lock
    def clear(self):
        """Clears instrument status."""
        self.resource.write('eventlog.clear()')
        self.resource.write('status.clear()')

    def reset(self):
        """Performs an instrument reset."""
        self.resource.write('reset()')

    def test(self) -> int:
        """Runs internal self test, returns result value."""
        return int(self.resource.query('print([[0]])'))

    def wait_to_continue(self):
        """Prevents command execution until no operation flag is set."""
        self.resource.write('waitcomplete()')
