from comet.devices import IEC60488

__all__ = ['E4980A']

class E4980A(IEC60488):
    """Keysignt E4980A Precision LCR Meter."""

    options = {
        'read_termination': '\n',
    }
