"""Module `comet.driver` provides class `Driver` to be inherited by custom
device driver classes.
"""

from .transport import Transport

__all__ = ['Driver']

class Driver(object):
    """Base class for custom device drivers.

    >>> class MyDriver(comet.Driver):
    ...     @property
    ...     def voltage(self):
    ...         return float(self.transport.query(':VOLT?'))
    ...     @voltage.setter
    ...     def voltage(self, value):
    ...         self.transport.query(':VOLT {:.3f}'.format(value))
    ...
    >>> with comet.Visa('GPIB::15') as transport:
    ...     driver = MyDriver(transport)
    ...     driver.voltage = 42
    ...     driver.voltage
    ...
    42.0
    """

    def __init__(self, transport):
        assert isinstance(transport, Transport)
        self.__transport = transport

    def transport(self):
        return self.__transport
