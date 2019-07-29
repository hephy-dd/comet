from lantz import Action, Feat, DictFeat, ureg
from lantz.drivers.scpi import SCPIDriver
from lantz.errors import InstrumentError

class K2700(SCPIDriver):
    """Lantz driver for interfacing with Keithley Model 2700 Digital Multimeter."""

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n',
        }
    }
