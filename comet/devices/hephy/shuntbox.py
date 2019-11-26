from typing import List
from comet import Device

__all__ = ['ShuntBox']

class ShuntBox(Device):
    """HEPHY shunt box providing 10 channels of high voltage relais and PT100
    temperature sensors.
    """

    channels = 10
    """Number of device channels."""

    def identification(self):
        """Returns IEC60488 device identification."""
        return self.resource().query('*IDN?')

    def temperature(self) -> List[float]:
        """Returns list of temperature readings from all sensors. Unconnected
        sensors return a float of value nan."""
        result = self.resource().query('GET:TEMP ALL')
        return [float(value) for value in result.split(',')]

    def enable(self, index: int, enabled: bool):
        """Enable or disable a single channel relais."""
        assert 0 < index < self.channels
        result = self.resource().query('SET:REL_{} {}'.format('ON' if enabled else 'OFF', index))
        assert result == 'OK'

    def enableAll(self, enabled: bool):
        """Enable or disable all channel relais."""
        result = self.resource().query('SET:REL_{} ALL'.format('ON' if enabled else 'OFF'))
        assert result == 'OK'
