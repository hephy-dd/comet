"""TANGO emulator."""

from comet.emulator import Emulator, message
from comet.emulator import register_emulator

__all__ = ['TANGOEmulator']


@register_emulator('marzhauser.tango')
class TANGOEmulator(Emulator):
    """TANGO emulator."""

    ...
