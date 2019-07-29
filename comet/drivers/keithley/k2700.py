from lantz.core import Action, Feat, DictFeat, ureg
from lantz.core.messagebased import MessageBasedDriver
from lantz.core.errors import InstrumentError

class K2700(SCPIDriver):
    """Lantz driver for interfacing with Keithley Model 2700 Digital Multimeter."""

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n',
        }
    }
