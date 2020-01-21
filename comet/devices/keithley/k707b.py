from comet.devices import IEC60488

__all__ = ['K707B']

class K707B(IEC60488):
    """Keithley Models 707B Switching Matrix."""

    options = {
        'encoding': 'latin1',
        'read_termination': '\r',
    }
