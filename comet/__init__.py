import time
import random

from .application import *
from .ui import *
from .process import *
from .driver import *
from .functions import Range
from .ureg import *
from .version import __version__

def app():
    """Returns reference to global application object."""
    return CoreApplication.app()
