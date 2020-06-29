from typing import List

from comet.driver import lock, Driver

__all__ = ['ShuntBox']

class Relays(Driver):

    def __getitem__(self, index: int) -> bool:
        """Returns single/all channel relays enabled state.

        >>> instr.relays[1]
        True
        """
        if not 0 < index <= ShuntBox.channels:
            raise ValueError(f"invalid channel index: {index}")
        result = self.resource.query(f'GET:REL {index:d}').strip()
        return bool(int(result))

    def __setitem__(self, index: int, enabled: bool):
        """Enable or disable a single channel relais.

        >>> instr.relays[1] = True # switch on channel 1
        """
        if not 0 < index <= ShuntBox.channels:
            raise ValueError(f"invalid channel index: {index}")
        mode = 'ON' if enabled else 'OFF'
        result = self.resource.query(f'SET:REL_{mode} {index}').strip()
        if result != 'OK':
            raise RuntimeError(f"returned unexpected value: '{result}'")

    @property
    def all(self) -> List[bool]:
        """Returns all relays enabled states.

        >>> instr.relays.all
        [True, True, ..., False, False]
        """
        result = self.resource.query('GET:REL ALL').strip()
        return [bool(int(value)) for value in result.split(',') if value.strip()][:self.channels]

    @all.setter
    def all(self, enabled: bool):
        """Enable or disable all relays.

        >>> instr.relays.all = False # switch off all channels
        """
        result = self.resource.query('SET:REL_{} ALL'.format('ON' if enabled else 'OFF')).strip()
        if result != 'OK':
            raise RuntimeError(f"returned unexpected value: '{result}'")

    def __len__(self):
        return ShuntBox.channels

class ShuntBox(Driver):
    """HEPHY shunt box providing 10 channels of high voltage relays and PT100
    temperature sensors.
    """

    channels = 10
    """Number of instrument channels."""

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.relays = Relays(self.resource)

    @property
    def identification(self) -> str:
        """Returns instrument identification.

        >>> instr.identification
        'HEPHY ShuntBox v1.0'
        """
        return self.resource.query('*IDN?')

    @property
    def uptime(self) -> int:
        """Returns up time in seconds.

        >>> instr.uptime
        42
        """
        return int(self.resource.query('GET:UP ?'))

    @property
    def memory(self) -> int:
        """Returns current memory consumption in bytes.

        >>> instr.memory
        42
        """
        return int(self.resource.query('GET:RAM ?'))

    @property
    def temperature(self) -> List[float]:
        """Returns list of temperature readings from all channels. Unconnected
        channels return a float of special value NAN.

        >>> instr.temperature
        [24.05, NAN, ...]
        """
        result = self.resource.query('GET:TEMP ALL').strip()
        return [float(value) for value in result.split(',') if value.strip()][:self.channels] # avoid trailing commas
