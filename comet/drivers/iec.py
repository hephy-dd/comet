from ..driver import Driver

__all__ = ['IEC60488']

class IEC60488(Driver):
    """IEC60488 compatible driver."""

    def identification(self):
        """Returns IEC60488 device identification."""
        return self.transport().query('*IDN?')

    def reset(self):
        """Reset IEC60488 device."""
        return self.transport().query('*RST')
