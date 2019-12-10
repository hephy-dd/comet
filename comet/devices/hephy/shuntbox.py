from typing import List
from comet import Device

__all__ = ['ShuntBox']

class ShuntBox(Device):
    """HEPHY shunt box providing 10 channels of high voltage relais and PT100
    temperature sensors.
    """

    options = {
        'read_termination': '\n',
    }

    channels = 10
    """Number of device channels."""

    def identification(self):
        """Returns IEC60488 device identification."""
        return self.resource().query('*IDN?')

    def temperature(self) -> List[float]:
        """Returns list of temperature readings from all channels. Unconnected
        channels return a float of special value NAN."""
        result = self.resource().query('GET:TEMP ALL').strip()
        return [float(value) for value in result.split(',') if value.strip()] # avoid trailing commas

    def enable(self, index: int, enabled: bool):
        """Enable or disable a single channel relais. Valid channel indices are
        between 1 and 10.
        >>> device.enable(1, True) # switch on channel 1
        """
        if not 0 < index <= self.channels:
            raise ValueError("invalid channel index: {}".format(index))
        result = self.resource().query('SET:REL_{} {}'.format('ON' if enabled else 'OFF', index)).strip()
        if result != 'OK':
            raise RuntimeError(result)

    def enableAll(self, enabled: bool):
        """Enable or disable all channel relais.
        >>> device.enableAll(False) # switch off all channels
        """
        result = self.resource().query('SET:REL_{} ALL'.format('ON' if enabled else 'OFF')).strip()
        if result != 'OK':
            raise RuntimeError(result)
