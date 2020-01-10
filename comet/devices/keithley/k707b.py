from comet.devices import IEC60488

__all__ = ['K707B']

class K707B(IEC60488):

    options = {
        'encoding': 'latin1',
        'read_termination': '\r',
    }
