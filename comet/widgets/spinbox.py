from PyQt5 import QtWidgets

from ..units import ureg

__all__ = ['SpinBox']

class SpinBox(QtWidgets.QDoubleSpinBox):
    """Double spin box widet with unit support using pint.

    At default value is unitless. Unit symbols show up as value suffixes.

    >>> box = SpinBox()
    >>> box.setUnit(ureg.kHz)
    >>> box.setValue(500 * ureg.Hz)
    >>> box.value()
    <Quantity(0.5, 'kilohertz')>
    """

    __unit = ureg.dimensionless

    def unit(self):
        return self.__unit

    def setUnit(self, unit):
        """Set unit eitehr by unit object or by string.

        >>> w = SpinBox()
        >>> w.setUnit('Hz') # use string
        >>> w.setUnit(ureg.kHz) # use object
        """

        if not isinstance(unit, ureg.Unit):
            unit = ureg.parse_expression(unit).u
        self.__unit = unit
        self.setSuffix(' {:~}'.format(unit))
        self.setToolTip('{}'.format(unit).capitalize())

    def setValue(self, value):
        """Set value or quantity.

        >>> box = SpinBox()
        >>> box.setUnit(ureg.kHz)
        >>> box.setValue(42)
        >>> box.value()
        <Quantity(42, 'kilohertz')>
        >>> box.setValue(500 * ureg.Hz)
        >>> box.value()
        <Quantity(0.5, 'kilohertz')>
        """
        if isinstance(value, ureg.Quantity):
            value = value.to(self.unit())
        else:
            value = ureg.Quantity(value, self.unit())
        super().setValue(value.m)

    def value(self):
        """Retrurns value as quantity."""
        return super().value() * self.unit()
