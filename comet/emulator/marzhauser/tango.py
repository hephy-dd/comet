"""TANGO emulator."""

from comet.emulator import Emulator, message, run

__all__ = ['TANGOEmulator']

class TANGOEmulator(Emulator):
    """TANGO emulator."""

    version = '3.61'

    version_string = 'TANGO-EMULATOR, Version 1.00, Mar 11 2022, 13:51:01'

    tango_serial_number = '123456789'

    # Controller informations

    @message(r'version')
    def get_version(self):
        return type(self).version

    @message(r'nversion')
    def get_nversion(self):
        return type(self).version

    @message(r'identity')
    def get_identity(self):
        return 'TANGO-EMULATOR 0 0 0 0'

    @message(r'tango')
    def get_tango(self):
        return [type(self).version_string, type(self).tango_serial_number]

    # System configuration

    @message(r'save')
    def action_save(self):
        ...

    @message(r'restore')
    def action_restore(self):
        ...

    @message(r'reset')
    def action_reset(self):
        ...



if __name__ == '__main__':
    run(TANGOEmulator())
