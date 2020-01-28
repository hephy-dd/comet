from typing import List

from comet.driver import lock, Driver

__all__ = ['BrandBox']

class ShuntBox(Driver):
    """HEPHY "Brand" box providing switches and temperature sensors.
    """

    @property
    def identification(self) -> str:
        """Returns instrument identification.

        >>> instr.identification
        'HEPHY Brandbox v1.0'
        """
        return self.resource.query('*IDN?')
