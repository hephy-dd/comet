import time
import random

from . import ui

from .application import *
from .process import *
from .settings import *
from .driver import Driver, IEC60488, TSP
from .resource import *
from .functions import Range
from .ureg import *
from .utils import *
from .version import __version__

def app():
    """Returns reference to global application object."""
    return Application.instance()
