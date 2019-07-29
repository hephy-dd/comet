from lantz import Action, Feat, DictFeat, ureg
from lantz.messagebased import MessageBasedDriver
from lantz.errors import InstrumentError
from lantz.drivers.ieee4882 import IEEE4882Driver

__all__ = ['K2410']

class K2410(MessageBasedDriver, IEEE4882Driver):
    """Lantz driver for interfacing with Keithley Model 2410 Source Meter."""

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n',
        }
    }
