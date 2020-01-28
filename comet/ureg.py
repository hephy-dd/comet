"""Provides a common unit registry instance."""

import pint

__all__ = ['ureg']

ureg = pint.UnitRegistry()
