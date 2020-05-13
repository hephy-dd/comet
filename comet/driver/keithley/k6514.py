"""Keithley 6514 Electrometer.

Interface:

initiate()
abort()
fetch()
read()
calculate1.format
calculate1.format = 'MXB'|'PERC'
system.zcheck
system.zcheck = True/False
system.zcorrect.state
system.zcorrect.state = True|False
system.zcorrect.acquire()
system.preset()
system.lfrequency
system.lfrequency = 50|60
system.azero.state
system.azero.state = True|False
system.time
system.version
system.error.next
system.error.all
system.error.count
system.code.next
system.code.all
system.clear()

"""

from comet.driver import Driver, Action, Property
from comet.driver.iec60488 import IEC60488, opc_wait, opc_poll

__all__ = ['K6514']

class Calculate1(Driver):

    @Property(values=('MXB', 'PERC'))
    def format(self) -> str:
        return self.resource.query(':CALC:FORM?')

    @format.setter
    @opc_wait
    def format(self, value: str):
        self.resource.write(f':CALC:FORM {value:s}')

class System(Driver):

    def __init__(self, resource):
        super().__init__(resource)
        self.zcorrect = ZCorrect(resource)
        self.azero = AZero(resource)
        self.error = Error(resource)

    @Property(values={False: 0, True: 1})
    def zcheck(self) -> int:
        """Zero check."""
        return int(self.resource.query(':SYST:ZCH?'))

    @zcheck.setter
    @opc_wait
    def zcheck(self, value: int):
        self.resource.write(f':SYST:ZCH {value:d}')

    @Action()
    @opc_wait
    def preset(self):
        """Return to preset defaults."""
        self.resource.write(':SYST:PRES')

    @Property(values=(50, 60))
    def lfrequency(self) -> int:
        """Power line frequency."""
        return int(self.resource.query(':SYST:LFR?'))

    @lfrequency.setter
    @opc_wait
    def lfrequency(self, value: int):
        self.resource.write(f':SYST:LFR {value:d}')

    @Property(values=(50, 60))
    def lfrequency(self) -> int:
        """Power line frequency."""
        return int(self.resource.query(':SYST:LFR?'))

    @Property()
    def time(self) -> float:
        """Timestamp."""
        return float(self.resource.query(':SYST:TIME?'))

    @Property()
    def version(self) -> str:
        """SCPI revision level."""
        return self.resource.query(':SYST:VERS?')

class ZCorrect(Driver):

    @Property(values={False: 0, True: 1})
    def state(self) -> int:
        """Zero correct."""
        return int(self.resource.query(':SYST:ZCOR:STAT?'))

    @state.setter
    @opc_wait
    def state(self, value: int):
        self.resource.write(f':SYST:ZCOR:STAT {value:d}')

    @Action()
    @opc_wait
    def acquire(self):
        """Acquire a new zero correct value."""
        self.resource.write(':SYST:ZCOR:ACQ')

class AZero(Driver):

    @Property(values={False: 0, True: 1})
    def state(self) -> int:
        """Auto zero."""
        return int(self.resource.query(':SYST:AZER:STAT?'))

    @state.setter
    @opc_wait
    def state(self, value: int):
        self.resource.write(f':SYST:AZER:STAT {value:d}')

class Error(Driver):

    def __init__(self, resource):
        super().__init__(resource)
        self.code = Code(resource)

    @Property()
    def next(self) -> str:
        return self.resource.query(':SYST:ERR:NEXT?')

    @Property()
    def all(self) -> str:
        return self.resource.query(':SYST:ERR:ALL?')

    @Property()
    def count(self) -> int:
        return int(self.resource.query(':SYST:ERR:COUN?'))

    @Action()
    @opc_wait
    def clear(self):
        """Clear messages from error queue."""
        self.resource.write(':SYST:ERR:CLE')

class Code(Driver):

    @Property()
    def next(self) -> str:
        return self.resource.query(':SYST:ERR:CODE:NEXT?')

    @Property()
    def all(self) -> str:
        return self.resource.query(':SYST:ERR:CODE:ALL?')

class K6514(IEC60488):

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.calculate1 = Calculate1(resource)
        self.format = Format(resource)
        self.system = System(resource)

    @Action()
    @opc_wait
    def initiate(self):
        """Initiate one trigger cycle."""
        self.resource.write(':INIT')

    @Action()
    @opc_wait
    def abort(self):
        """Reset trigger system."""
        self.resource.write(':ABOR')

    @Action()
    def fetch(self):
        return self.resource.query(':FETC?')

    @Action()
    def read(self):
        return self.resource.query(':READ?')
