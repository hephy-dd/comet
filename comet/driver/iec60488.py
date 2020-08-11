import time

from comet.driver import lock, Driver, Property, Action

__all__ = ['IEC60488']

def opc_wait(function):
    """Decorator function, locks the resource and waits for `*OPC?` after
    function execution."""
    @lock
    def opc_wait(instance, *args, **kwargs):
        result = function(instance, *args, **kwargs)
        instance.resource.query('*OPC?')
        return result
    return opc_wait

def opc_poll(function, interval=.250, retries=40):
    """Decorator function, locks the resource, writes `*CLS` and `*OPC` before
    the function call and polls after function execution for `*ESR?` bit 0 to be
    set."""
    @lock
    def opc_poll(instance, *args, **kwargs):
        instance.resource.write('*CLS')
        instance.resource.write('*OPC')
        result = function(instance, *args, **kwargs)
        for i in range(retries):
            if 1 == int(instance.resource.query('*ESR?')) & 0x1:
                return result
            time.sleep(interval)
        raise RuntimeError("failed to poll for ESR")
    return opc_poll

class IEC60488(Driver):
    """IEC 60488-2 compatible intrument driver.

    The IEC 60488-2 describes a standard digital interface for programmable
    instrumentation. It is used by devices connected via the IEEE 488.1 bus,
    commonly known as GPIB. It is an adoption of the *IEEE std. 488.2-1992*
    standard.
    """

    @Property()
    def identification(self) -> str:
        """Returns instrument identification."""
        return self.resource.query('*IDN?')

    @Property()
    def event_status(self) -> int:
        """Returns event status."""
        return int(self.resource.query('*ESR?'))

    @Property()
    def event_status_enable(self) -> int:
        """Returns event status enable register."""
        return int(self.resource.query('*ESE?'))

    @event_status_enable.setter
    def event_status_enable(self, value: int):
        """Set event status enable register."""
        self.resource.write(f'*ESE {value:d}')

    @Property()
    def status(self) -> int:
        """Returns status register."""
        return int(self.resource.query('*STB?'))

    @Property()
    def operation_complete(self) -> bool:
        """Retruns operation complete state."""
        return bool(self.resource.query('*OPC?'))

    @Action()
    def complete_operation(self):
        """Sets the operation complete bit of the event status register."""
        self.resource.write('*OPC')

    @Action()
    def clear(self):
        """Clears instrument status."""
        self.resource.write('*CLS')

    @Action()
    def reset(self):
        """Performs an instrument reset."""
        self.resource.write('*RST')

    @Action()
    def test(self) -> int:
        """Runs internal self test, returns result value."""
        return int(self.resource.query('*TST?'))

    @Action()
    def wait_to_continue(self):
        """Prevents command execution until no operation flag is set."""
        self.resource.write('*WAI')
