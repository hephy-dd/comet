from ..device import Device

__all__ = ['SCPIDevice']

class SCPIDevice(Device):
    """Generic SCPI device."""

    def idn(self):
        return self.query('*IDN?')
