from comet.driver import Driver
from comet.driver import lock, opc_wait, opc_poll

__all__ = ['K2400']

class Beeper(Driver):
    @property
    def status(self):
        return int(self.resource.query(":SYST:BEEP:STAT?"))
    @status.setter
    @lock
    @opc_wait
    def status(self, value):
        self.resource.write(":SYST:BEEP:STAT {value:d}")

class System(Driver):
    beeper = Beeper()

class K2400(Driver):

    system = System()

    @lock
    @opc_poll
    def init(self):
        self.resource.write(":INIT")
