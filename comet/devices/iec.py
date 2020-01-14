from comet import Device

__all__ = ['IEC60488']

class IEC60488(Device):
    """IEC60488 compatible device."""

    def identification(self):
        """Returns IEC60488 device identification."""
        return self.resource.query('*IDN?')

    def clear(self):
        """Clear IEC60488 device status."""
        self.resource.write('*CLS')

    def reset(self):
        """Reset IEC60488 device."""
        self.resource.write('*RST')
