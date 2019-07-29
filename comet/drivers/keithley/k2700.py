from lantz import Action, Feat, DictFeat, ureg
from lantz.messagebased import MessageBasedDriver
from lantz.errors import InstrumentError
from lantz.drivers.ieee4882 import IEEE4882Driver

__all__ = ['K2700']

class K2700(MessageBasedDriver, IEEE4882Driver):
    """Lantz driver for interfacing with Keithley Model 2700 Digital Multimeter."""

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n',
        }
    }

    @Action()
    def fetch(self):
        return self.query('FETCh?')
