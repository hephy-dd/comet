from typing import List, Optional

from .generic import BeeperMixin
from .generic import ErrorQueueMixin
from .generic import RouteTerminalMixin
from .generic import Instrument, InstrumentError

__all__ = [
    'identify',
    'reset',
    'clear',
    'mute',
    'next_error',
    'route_terminal'
]


def identify(context: object) -> Optional[str]:
    """Return instrument identification if applicable, else return None."""
    if isinstance(context, Instrument):
        return context.identify()
    return None


def reset(context: object) -> bool:
    """Reset instrument if applicable, return True if applied."""
    if isinstance(context, Instrument):
        context.reset()
        return True
    return False


def clear(context: object) -> bool:
    """Clear instrument state if applicable, return True if applied."""
    if isinstance(context, Instrument):
        context.clear()
        return True
    return False


def mute(context: object) -> bool:
    """Mute beeper if applicable, return True if applied."""
    if isinstance(context, BeeperMixin):
        context.beeper = type(context).BEEPER_OFF
        return True
    return False


def next_error(context: object) -> Optional[InstrumentError]:
    """Return next error in error queue if applicable or None."""
    if isinstance(context, ErrorQueueMixin):
        return context.next_error()
    return None


def route_terminal(context: object, value: str) -> bool:
    """Set route terminal to front if applicable, return True if applied."""
    if isinstance(context, RouteTerminalMixin):
        context.route_terminal = value
        return True
    return False
