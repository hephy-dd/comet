from lantz.core import Action, Feat, DictFeat, ureg
from lantz.core.messagebased import MessageBasedDriver
from lantz.core.errors import InstrumentError

class K2410(SCPIDriver):
    """Lantz driver for interfacing with Keithley Model 2410 Source Meter."""

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n',
        }
    }
