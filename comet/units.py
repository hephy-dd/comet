"""Units registry module.

Creating a global unit registry using pint.

Usage:

>>> from comet.units import ureg
>>> 42 * ureg.Hz
<Quantity(42, 'hertz')>
"""

from pint import UnitRegistry

__all__ = ['ureg']

ureg = UnitRegistry()
"""Global unit registry instance."""
